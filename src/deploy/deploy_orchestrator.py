#!/usr/bin/env python3
# deploy_orchestrator.py
"""
Comprehensive AI Deployment/Execution Orchestrator (Production-Oriented)
綜合 AI 部署/執行編排器（面向生產環境）
综合 AI 部署/执行编排器（面向生产环境）

Features / 功能 / 功能:
- Structured JSON logs (stdout + optional file)
  結構化 JSON 日誌（標準輸出 + 可選檔案）
- Notifications: Slack + SMTP email + generic SMS webhook (pluggable)
  通知：Slack + SMTP 電子郵件 + 通用 SMS webhook（可插拔）
- Resource monitoring with state-change alerts + cooldown/dedup
  資源監控，含狀態變更告警 + 冷卻/去重
- Deterministic safety checks (HTTP health probes + optional custom commands)
  確定性安全檢查（HTTP 健康探測 + 可選自訂命令）
- Deploy/verify/promote/rollback per target
  每個目標的部署/驗證/升級/回滾
- Scheduled maintenance actions (backup/restore/integrity checks)
  排程維護操作（備份/還原/完整性檢查）
- Safe subprocess execution (no shell), timeouts, retries, backoff
  安全子程序執行（無 shell），逾時、重試、退避
- Parallel deployment (optional)
  並行部署（可選）

Config / 設定 / 设置:
- TOML file (Python 3.11+ includes tomllib)
  TOML 檔案（Python 3.11+ 內建 tomllib）
- Env overrides supported (e.g., SLACK_WEBHOOK_URL)
  支援環境變數覆蓋

Author: Donnie Chen (donniechen92@gmail.com)
"""

from __future__ import annotations

import argparse
import email.message
import json
import logging
import os
import signal
import smtplib
import subprocess
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import psutil  # pip install psutil

try:
    import tomllib  # py3.11+
except Exception:  # pragma: no cover
    tomllib = None


# =============================================================================
# Utilities / 工具函式 / 工具函数
# =============================================================================

def now_utc_iso() -> str:
    """Current UTC timestamp in ISO format / 當前 UTC 時間戳（ISO 格式）"""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sleep_with_jitter(base_s: float, jitter_ratio: float = 0.15) -> None:
    """Sleep with deterministic jitter / 帶確定性抖動的睡眠"""
    time.sleep(base_s + (base_s * jitter_ratio * (os.getpid() % 10) / 10.0))


def clamp(v: float, lo: float, hi: float) -> float:
    """Clamp value to range / 將值限制在範圍內 / 将值限制在范围内"""
    return max(lo, min(hi, v))


# =============================================================================
# Structured JSON Logging / 結構化 JSON 日誌 / 结构化 JSON 日志
# =============================================================================

class JsonFormatter(logging.Formatter):
    """JSON log formatter / JSON 日誌格式化器"""

    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "ts": now_utc_iso(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        for key in ("event", "run_id", "target", "severity", "details"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(log_file: Optional[str] = None) -> logging.Logger:
    """
    Initialize structured logger.
    初始化結構化日誌記錄器。
    初始化结构化日志记录器。
    """
    logger = logging.getLogger("orchestrator")
    logger.setLevel(logging.INFO)
    logger.handlers = []
    logger.propagate = False

    sh = logging.StreamHandler()
    sh.setFormatter(JsonFormatter())
    logger.addHandler(sh)

    if log_file:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(JsonFormatter())
        logger.addHandler(fh)

    return logger


# =============================================================================
# Notifiers / 通知器 / 通知器
# =============================================================================

@dataclass(frozen=True)
class Alert:
    """
    Alert payload / 告警載荷 / 告警载荷

    Attributes:
        severity: INFO/WARN/CRIT / 嚴重程度
        title: Alert title / 告警標題
        details: Alert details / 告警詳情
        run_id: Run identifier / 執行識別碼
        target: Target name (optional) / 目標名稱（可選）
    """
    severity: str
    title: str
    details: str
    run_id: str
    target: Optional[str] = None


class Notifier:
    """Base notifier interface / 基礎通知器介面 / 基础通知器接口"""

    def send(self, alert: Alert) -> None:
        raise NotImplementedError


class SlackWebhookNotifier(Notifier):
    """Slack webhook notifier / Slack webhook 通知器"""

    def __init__(self, webhook_url: str, timeout_s: int = 8):
        self.webhook_url = webhook_url
        self.timeout_s = timeout_s

    def send(self, alert: Alert) -> None:
        payload = {
            "text": (
                f"[{alert.severity}] {alert.title}\n"
                f"run_id={alert.run_id}"
                + (f" target={alert.target}" if alert.target else "")
                + f"\n{alert.details}"
            )
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
            _ = resp.read()


class SmtpEmailNotifier(Notifier):
    """SMTP email notifier / SMTP 電子郵件通知器 / SMTP 电子邮件通知器"""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        from_addr: str,
        to_addrs: List[str],
        use_tls: bool = True,
        timeout_s: int = 10,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.use_tls = use_tls
        self.timeout_s = timeout_s

    def send(self, alert: Alert) -> None:
        msg = email.message.EmailMessage()
        msg["Subject"] = f"[{alert.severity}] {alert.title}"
        msg["From"] = self.from_addr
        msg["To"] = ", ".join(self.to_addrs)
        body = (
            f"run_id={alert.run_id}\n"
            + (f"target={alert.target}\n" if alert.target else "")
            + f"\n{alert.details}\n"
        )
        msg.set_content(body)

        with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=self.timeout_s) as s:
            if self.use_tls:
                s.starttls()
            if self.username:
                s.login(self.username, self.password)
            s.send_message(msg)


class GenericSmsWebhookNotifier(Notifier):
    """
    Generic SMS provider webhook notifier.
    通用 SMS 提供者 webhook 通知器。

    Sends JSON: {"to": "...", "message": "..."}
    """

    def __init__(self, endpoint_url: str, to_number: str, timeout_s: int = 8):
        self.endpoint_url = endpoint_url
        self.to_number = to_number
        self.timeout_s = timeout_s

    def send(self, alert: Alert) -> None:
        payload = {
            "to": self.to_number,
            "message": f"[{alert.severity}] {alert.title} (run_id={alert.run_id})",
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
            _ = resp.read()


class CompositeNotifier(Notifier):
    """
    Fan-out notifier: sends alerts to all registered notifiers.
    扇出通知器：將告警傳送到所有已註冊的通知器。
    扇出通知器：将告警发送到所有已注册的通知器。
    """

    def __init__(self, notifiers: List[Notifier], logger: logging.Logger, run_id: str):
        self.notifiers = notifiers
        self.logger = logger
        self.run_id = run_id

    def send(self, alert: Alert) -> None:
        for n in self.notifiers:
            try:
                n.send(alert)
            except Exception as e:
                self.logger.info(
                    "Notifier failed",
                    extra={"event": "notify_error", "run_id": self.run_id, "details": str(e)},
                )


# =============================================================================
# Command Execution / 命令執行 / 命令执行
# =============================================================================

@dataclass(frozen=True)
class CmdResult:
    """Command execution result / 命令執行結果 / 命令执行结果"""
    rc: int             # Return code / 回傳碼
    stdout: str         # Standard output / 標準輸出
    stderr: str         # Standard error / 標準錯誤
    duration_s: float   # Execution duration / 執行時長


def run_cmd(
    cmd: List[str],
    timeout_s: int,
    logger: logging.Logger,
    run_id: str,
    event: str,
    target: str,
) -> CmdResult:
    """
    Execute command safely (no shell) with timeout.
    安全執行命令（無 shell）並設定逾時。
    安全执行命令（无 shell）并设置超时。
    """
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s)
    dur = time.time() - t0
    logger.info(
        "Command executed",
        extra={
            "event": event,
            "run_id": run_id,
            "target": target,
            "details": {"cmd": cmd, "rc": p.returncode, "duration_s": round(dur, 3)},
        },
    )
    return CmdResult(p.returncode, p.stdout, p.stderr, dur)


# =============================================================================
# Health Checks / 健康檢查 / 健康检查
# =============================================================================

def http_get_ok(url: str, timeout_s: int = 6) -> bool:
    """HTTP GET health probe / HTTP GET 健康探測"""
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            return 200 <= resp.status < 300
    except Exception:
        return False


def health_check_with_retries(
    url: str,
    retries: int,
    base_backoff_s: float,
    logger: logging.Logger,
    run_id: str,
    target: str,
) -> bool:
    """
    Health check with exponential backoff retries.
    帶指數退避重試的健康檢查。
    带指数退避重试的健康检查。
    """
    for i in range(retries + 1):
        ok = http_get_ok(url)
        logger.info(
            "Health probe",
            extra={
                "event": "health_probe",
                "run_id": run_id,
                "target": target,
                "details": {"url": url, "ok": ok, "attempt": i},
            },
        )
        if ok:
            return True
        if i < retries:
            sleep_with_jitter(base_backoff_s * (2**i))
    return False


# =============================================================================
# Resource Monitoring / 資源監控 / 资源监控
# State-change alerts with cooldown/dedup
# 狀態變更告警，含冷卻/去重
# =============================================================================

@dataclass(frozen=True)
class ResourceThresholds:
    """
    Resource alert thresholds / 資源告警閾值 / 资源告警阈值

    Attributes:
        cpu_warn/crit: CPU usage % / CPU 使用率 %
        mem_warn/crit: Memory usage % / 記憶體使用率 %
        disk_warn/crit: Disk usage % / 磁碟使用率 %
    """
    cpu_warn: float = 75.0
    cpu_crit: float = 90.0
    mem_warn: float = 80.0
    mem_crit: float = 92.0
    disk_warn: float = 85.0
    disk_crit: float = 95.0


def resource_state(value: float, warn: float, crit: float) -> str:
    """Determine resource state from thresholds / 從閾值判定資源狀態"""
    if value >= crit:
        return "CRIT"
    if value >= warn:
        return "WARN"
    return "OK"


class ResourceMonitor(threading.Thread):
    """
    Background resource monitor with state-change alerting.
    背景資源監控器，含狀態變更告警。
    后台资源监控器，含状态变更告警。
    """

    def __init__(
        self,
        logger: logging.Logger,
        notifier: Optional[Notifier],
        run_id: str,
        thresholds: ResourceThresholds,
        poll_s: float = 2.0,
        cooldown_s: int = 120,
    ):
        super().__init__(daemon=True)
        self.logger = logger
        self.notifier = notifier
        self.run_id = run_id
        self.thresholds = thresholds
        self.poll_s = poll_s
        self.cooldown_s = cooldown_s
        self.stop_event = threading.Event()
        self.last_state = {"cpu": "OK", "mem": "OK", "disk": "OK"}
        self.last_sent_ts = {"cpu": 0.0, "mem": 0.0, "disk": 0.0}

    def stop(self) -> None:
        """Signal monitor to stop / 通知監控器停止"""
        self.stop_event.set()

    def run(self) -> None:
        self.logger.info(
            "Resource monitor started",
            extra={"event": "monitor_start", "run_id": self.run_id},
        )
        while not self.stop_event.is_set():
            cpu = psutil.cpu_percent(interval=0.2)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent

            self.logger.info(
                "Resource sample",
                extra={
                    "event": "resource_sample",
                    "run_id": self.run_id,
                    "details": {"cpu": cpu, "mem": mem, "disk": disk},
                },
            )

            self._check("cpu", cpu, self.thresholds.cpu_warn, self.thresholds.cpu_crit)
            self._check("mem", mem, self.thresholds.mem_warn, self.thresholds.mem_crit)
            self._check("disk", disk, self.thresholds.disk_warn, self.thresholds.disk_crit)

            self.stop_event.wait(self.poll_s)

        self.logger.info(
            "Resource monitor stopped",
            extra={"event": "monitor_stop", "run_id": self.run_id},
        )

    def _check(self, key: str, value: float, warn: float, crit: float) -> None:
        st = resource_state(value, warn, crit)
        prev = self.last_state[key]
        if st == prev:
            return

        self.last_state[key] = st
        now = time.time()

        # Throttle non-CRIT state alerts / 限流非 CRIT 狀態告警
        if st != "CRIT" and (now - self.last_sent_ts[key]) < self.cooldown_s:
            return

        self.last_sent_ts[key] = now
        if self.notifier:
            self.notifier.send(
                Alert(
                    severity=st,
                    title=f"{key.upper()} state changed {prev} → {st}",
                    details=f"{key}={value:.1f}% (warn={warn}%, crit={crit}%)",
                    run_id=self.run_id,
                )
            )


# =============================================================================
# Deployment Models / 部署模型 / 部署模型
# =============================================================================

@dataclass(frozen=True)
class Target:
    """
    Deployment target configuration.
    部署目標配置。
    部署目标配置。
    """
    name: str
    deploy_cmd: List[str]
    rollback_cmd: Optional[List[str]] = None
    promote_cmd: Optional[List[str]] = None

    health_url: Optional[str] = None
    readiness_url: Optional[str] = None

    deploy_timeout_s: int = 600
    rollback_timeout_s: int = 600
    promote_timeout_s: int = 600

    health_retries: int = 5
    health_backoff_s: float = 1.5

    post_deploy_check_cmd: Optional[List[str]] = None
    post_deploy_check_timeout_s: int = 120


@dataclass(frozen=True)
class GlobalChecks:
    """Global safety checks / 全域安全檢查 / 全局安全检查"""
    system_integrity_cmd: Optional[List[str]] = None
    network_stability_cmd: Optional[List[str]] = None
    integrity_timeout_s: int = 120
    network_timeout_s: int = 120


@dataclass(frozen=True)
class OrchestratorConfig:
    """
    Full orchestrator configuration.
    完整編排器配置。
    完整编排器配置。
    """
    run_id: str
    log_file: Optional[str]
    parallelism: int

    thresholds: ResourceThresholds
    targets: List[Target]
    global_checks: GlobalChecks

    slack_webhook_url: Optional[str]
    smtp: Optional[Dict[str, Any]]
    sms: Optional[Dict[str, Any]]


@dataclass
class OrchestratorResult:
    """Orchestration run result / 編排執行結果 / 编排执行结果"""
    ok: bool
    failed_targets: List[str]


# =============================================================================
# Orchestrator / 編排器 / 编排器
# =============================================================================

class Orchestrator:
    """
    Production deployment orchestrator.
    生產環境部署編排器。
    生产环境部署编排器。

    Lifecycle / 生命週期 / 生命周期:
    1. Deploy all targets (sequential or parallel)
       部署所有目標（順序或並行）
    2. Run global safety checks
       執行全域安全檢查
    3. Optionally promote targets
       可選升級目標
    4. On failure: rollback failed targets
       失敗時：回滾失敗的目標
    """

    def __init__(
        self,
        cfg: OrchestratorConfig,
        logger: logging.Logger,
        notifier: Optional[Notifier],
    ):
        self.cfg = cfg
        self.logger = logger
        self.notifier = notifier
        self.monitor = ResourceMonitor(
            logger=self.logger,
            notifier=self.notifier,
            run_id=self.cfg.run_id,
            thresholds=self.cfg.thresholds,
        )
        self._stop = threading.Event()

    def stop(self) -> None:
        """Graceful stop / 優雅停止 / 优雅停止"""
        self._stop.set()
        self.monitor.stop()

    def execute(self, promote: bool = False) -> OrchestratorResult:
        """
        Execute full deployment pipeline.
        執行完整部署管線。
        执行完整部署管线。
        """
        self.logger.info(
            "Run started",
            extra={"event": "run_start", "run_id": self.cfg.run_id},
        )
        self.monitor.start()

        failed: List[str] = []
        try:
            # Phase 1: Deploy / 階段1：部署
            self._deploy_all(failed)

            if failed:
                raise RuntimeError(f"Deployment failed for targets: {failed}")

            # Phase 2: Global safety gates / 階段2：全域安全閘門
            if not self._global_safety_checks():
                raise RuntimeError("Global safety checks failed")

            # Phase 3: Promote (optional) / 階段3：升級（可選）
            if promote:
                self._promote_all(failed)
                if failed:
                    raise RuntimeError(f"Promotion failed for targets: {failed}")

            self.logger.info(
                "Run succeeded",
                extra={"event": "run_ok", "run_id": self.cfg.run_id},
            )
            if self.notifier:
                self.notifier.send(
                    Alert("INFO", "Deployment run succeeded", "All targets deployed and verified.", self.cfg.run_id)
                )

            return OrchestratorResult(ok=True, failed_targets=[])

        except Exception as e:
            self.logger.error(
                "Run failed",
                extra={"event": "run_error", "run_id": self.cfg.run_id, "details": str(e)},
            )
            if self.notifier:
                self.notifier.send(
                    Alert("CRIT", "Deployment run failed", str(e), self.cfg.run_id)
                )

            # Rollback failed targets / 回滾失敗的目標
            self._rollback_failed(failed)

            return OrchestratorResult(ok=False, failed_targets=failed)

        finally:
            self.monitor.stop()
            self.monitor.join(timeout=5)
            self.logger.info(
                "Run completed",
                extra={"event": "run_done", "run_id": self.cfg.run_id},
            )

    # --- Internal: Deploy / 內部：部署 ---

    def _deploy_all(self, failed: List[str]) -> None:
        targets = self.cfg.targets
        par = max(1, self.cfg.parallelism)

        if par == 1:
            for t in targets:
                if self._stop.is_set():
                    failed.append(t.name)
                    continue
                if not self._deploy_one(t):
                    failed.append(t.name)
            return

        with ThreadPoolExecutor(max_workers=par) as ex:
            futs = {ex.submit(self._deploy_one, t): t for t in targets}
            for fut in as_completed(futs):
                t = futs[fut]
                try:
                    ok = fut.result()
                except Exception:
                    ok = False
                if not ok:
                    failed.append(t.name)

    def _deploy_one(self, t: Target) -> bool:
        self.logger.info(
            "Deploy target",
            extra={"event": "deploy_start", "run_id": self.cfg.run_id, "target": t.name},
        )
        if self.notifier:
            self.notifier.send(
                Alert("INFO", f"Deploy started: {t.name}", "Starting deployment.", self.cfg.run_id, t.name)
            )

        # Execute deploy command / 執行部署命令
        r = run_cmd(t.deploy_cmd, t.deploy_timeout_s, self.logger, self.cfg.run_id, "deploy_cmd", t.name)
        if r.rc != 0:
            self.logger.error(
                "Deploy command failed",
                extra={"event": "deploy_failed", "run_id": self.cfg.run_id, "target": t.name, "details": r.stderr[:2000]},
            )
            if self.notifier:
                self.notifier.send(
                    Alert("CRIT", f"Deploy failed: {t.name}", r.stderr[:2000], self.cfg.run_id, t.name)
                )
            return False

        # Readiness gate / 就緒閘門
        if t.readiness_url:
            ok = health_check_with_retries(
                t.readiness_url, t.health_retries, t.health_backoff_s,
                self.logger, self.cfg.run_id, t.name,
            )
            if not ok:
                self.logger.error(
                    "Readiness failed",
                    extra={"event": "readiness_failed", "run_id": self.cfg.run_id, "target": t.name},
                )
                return False

        # Health gate / 健康閘門
        if t.health_url:
            ok = health_check_with_retries(
                t.health_url, t.health_retries, t.health_backoff_s,
                self.logger, self.cfg.run_id, t.name,
            )
            if not ok:
                self.logger.error(
                    "Health failed",
                    extra={"event": "health_failed", "run_id": self.cfg.run_id, "target": t.name},
                )
                return False

        # Post-deploy custom check / 部署後自訂檢查
        if t.post_deploy_check_cmd:
            c = run_cmd(
                t.post_deploy_check_cmd, t.post_deploy_check_timeout_s,
                self.logger, self.cfg.run_id, "post_deploy_check", t.name,
            )
            if c.rc != 0:
                self.logger.error(
                    "Post-deploy check failed",
                    extra={"event": "post_deploy_check_failed", "run_id": self.cfg.run_id, "target": t.name},
                )
                return False

        self.logger.info(
            "Deploy target OK",
            extra={"event": "deploy_ok", "run_id": self.cfg.run_id, "target": t.name},
        )
        if self.notifier:
            self.notifier.send(
                Alert("INFO", f"Deploy OK: {t.name}", "Deployment and checks passed.", self.cfg.run_id, t.name)
            )
        return True

    # --- Internal: Promote / 內部：升級 ---

    def _promote_all(self, failed: List[str]) -> None:
        for t in self.cfg.targets:
            if not t.promote_cmd:
                continue
            self.logger.info(
                "Promote target",
                extra={"event": "promote_start", "run_id": self.cfg.run_id, "target": t.name},
            )
            r = run_cmd(t.promote_cmd, t.promote_timeout_s, self.logger, self.cfg.run_id, "promote_cmd", t.name)
            if r.rc != 0:
                self.logger.error(
                    "Promote failed",
                    extra={"event": "promote_failed", "run_id": self.cfg.run_id, "target": t.name},
                )
                failed.append(t.name)

    # --- Internal: Rollback / 內部：回滾 ---

    def _rollback_failed(self, failed: List[str]) -> None:
        if not failed:
            return
        for t in self.cfg.targets:
            if t.name not in failed:
                continue
            if not t.rollback_cmd:
                continue
            self.logger.info(
                "Rollback target",
                extra={"event": "rollback_start", "run_id": self.cfg.run_id, "target": t.name},
            )
            r = run_cmd(t.rollback_cmd, t.rollback_timeout_s, self.logger, self.cfg.run_id, "rollback_cmd", t.name)
            if r.rc != 0:
                self.logger.error(
                    "Rollback failed",
                    extra={"event": "rollback_failed", "run_id": self.cfg.run_id, "target": t.name},
                )
            else:
                self.logger.info(
                    "Rollback OK",
                    extra={"event": "rollback_ok", "run_id": self.cfg.run_id, "target": t.name},
                )

    # --- Internal: Global checks / 內部：全域檢查 ---

    def _global_safety_checks(self) -> bool:
        gc = self.cfg.global_checks
        ok = True

        if gc.system_integrity_cmd:
            r = run_cmd(
                gc.system_integrity_cmd, gc.integrity_timeout_s,
                self.logger, self.cfg.run_id, "system_integrity", "GLOBAL",
            )
            ok = ok and (r.rc == 0)

        if gc.network_stability_cmd:
            r = run_cmd(
                gc.network_stability_cmd, gc.network_timeout_s,
                self.logger, self.cfg.run_id, "network_stability", "GLOBAL",
            )
            ok = ok and (r.rc == 0)

        self.logger.info(
            "Global checks",
            extra={"event": "global_checks", "run_id": self.cfg.run_id, "details": {"ok": ok}},
        )
        return ok


# =============================================================================
# Maintenance Mode / 維護模式 / 维护模式
# Scheduled backup/restore/integrity (cron / K8s CronJob)
# =============================================================================

def run_maintenance(
    logger: logging.Logger,
    run_id: str,
    notifier: Optional[Notifier],
    backup_cmd: Optional[List[str]],
    restore_verify_cmd: Optional[List[str]],
    timeout_s: int = 1800,
) -> bool:
    """
    Run maintenance tasks (backup, restore verification).
    執行維護任務（備份、還原驗證）。
    执行维护任务（备份、还原验证）。
    """
    logger.info("Maintenance started", extra={"event": "maintenance_start", "run_id": run_id})
    try:
        if backup_cmd:
            r = run_cmd(backup_cmd, timeout_s, logger, run_id, "backup_cmd", "MAINT")
            if r.rc != 0:
                raise RuntimeError(f"Backup failed: {r.stderr[:2000]}")
        if restore_verify_cmd:
            r = run_cmd(restore_verify_cmd, timeout_s, logger, run_id, "restore_verify_cmd", "MAINT")
            if r.rc != 0:
                raise RuntimeError(f"Restore verify failed: {r.stderr[:2000]}")
        logger.info("Maintenance OK", extra={"event": "maintenance_ok", "run_id": run_id})
        if notifier:
            notifier.send(Alert("INFO", "Maintenance OK", "Backup/restore checks passed.", run_id))
        return True
    except Exception as e:
        logger.error("Maintenance failed", extra={"event": "maintenance_failed", "run_id": run_id, "details": str(e)})
        if notifier:
            notifier.send(Alert("CRIT", "Maintenance failed", str(e), run_id))
        return False
    finally:
        logger.info("Maintenance done", extra={"event": "maintenance_done", "run_id": run_id})


# =============================================================================
# Config Loading / 配置載入 / 配置加载
# TOML + environment variable overrides
# =============================================================================

def load_toml(path: str) -> Dict[str, Any]:
    """Load TOML config file / 載入 TOML 配置檔案"""
    if tomllib is None:
        raise RuntimeError("Python 3.11+ required for tomllib.")
    with open(path, "rb") as f:
        return tomllib.load(f)


def env_str(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get env var or default / 取得環境變數或預設值"""
    v = os.getenv(key)
    if v is None or v.strip() == "":
        return default
    return v.strip()


def build_notifier_from_cfg(
    cfg: Dict[str, Any],
    logger: logging.Logger,
    run_id: str,
) -> Optional[Notifier]:
    """Build composite notifier from config / 從配置構建複合通知器"""
    notifiers: List[Notifier] = []

    slack_url = env_str("SLACK_WEBHOOK_URL") or cfg.get("notifications", {}).get("slack_webhook_url")
    if slack_url:
        notifiers.append(SlackWebhookNotifier(slack_url))

    smtp_cfg = cfg.get("notifications", {}).get("smtp")
    if smtp_cfg and smtp_cfg.get("host"):
        notifiers.append(
            SmtpEmailNotifier(
                smtp_host=smtp_cfg["host"],
                smtp_port=int(smtp_cfg.get("port", 587)),
                username=smtp_cfg.get("username", ""),
                password=smtp_cfg.get("password", ""),
                from_addr=smtp_cfg.get("from", ""),
                to_addrs=[x.strip() for x in smtp_cfg.get("to", "").split(",") if x.strip()],
                use_tls=bool(smtp_cfg.get("use_tls", True)),
            )
        )

    sms_cfg = cfg.get("notifications", {}).get("sms")
    if sms_cfg and sms_cfg.get("endpoint_url") and sms_cfg.get("to"):
        notifiers.append(GenericSmsWebhookNotifier(sms_cfg["endpoint_url"], sms_cfg["to"]))

    if not notifiers:
        return None
    return CompositeNotifier(notifiers, logger=logger, run_id=run_id)


def parse_thresholds(cfg: Dict[str, Any]) -> ResourceThresholds:
    t = cfg.get("thresholds", {})
    return ResourceThresholds(
        cpu_warn=float(t.get("cpu_warn", 75)),
        cpu_crit=float(t.get("cpu_crit", 90)),
        mem_warn=float(t.get("mem_warn", 80)),
        mem_crit=float(t.get("mem_crit", 92)),
        disk_warn=float(t.get("disk_warn", 85)),
        disk_crit=float(t.get("disk_crit", 95)),
    )


def parse_targets(cfg: Dict[str, Any]) -> List[Target]:
    out: List[Target] = []
    for x in cfg.get("targets", []):
        out.append(
            Target(
                name=x["name"],
                deploy_cmd=list(x["deploy_cmd"]),
                rollback_cmd=list(x["rollback_cmd"]) if x.get("rollback_cmd") else None,
                promote_cmd=list(x["promote_cmd"]) if x.get("promote_cmd") else None,
                health_url=x.get("health_url"),
                readiness_url=x.get("readiness_url"),
                deploy_timeout_s=int(x.get("deploy_timeout_s", 600)),
                rollback_timeout_s=int(x.get("rollback_timeout_s", 600)),
                promote_timeout_s=int(x.get("promote_timeout_s", 600)),
                health_retries=int(x.get("health_retries", 5)),
                health_backoff_s=float(x.get("health_backoff_s", 1.5)),
                post_deploy_check_cmd=list(x["post_deploy_check_cmd"]) if x.get("post_deploy_check_cmd") else None,
                post_deploy_check_timeout_s=int(x.get("post_deploy_check_timeout_s", 120)),
            )
        )
    return out


def parse_global_checks(cfg: Dict[str, Any]) -> GlobalChecks:
    g = cfg.get("global_checks", {})
    return GlobalChecks(
        system_integrity_cmd=list(g["system_integrity_cmd"]) if g.get("system_integrity_cmd") else None,
        network_stability_cmd=list(g["network_stability_cmd"]) if g.get("network_stability_cmd") else None,
        integrity_timeout_s=int(g.get("integrity_timeout_s", 120)),
        network_timeout_s=int(g.get("network_timeout_s", 120)),
    )


def build_orchestrator_config(raw: Dict[str, Any], run_id: str) -> OrchestratorConfig:
    """Build OrchestratorConfig from raw TOML dict / 從原始 TOML 字典構建配置"""
    orch = raw.get("orchestrator", {})
    log_file = orch.get("log_file")
    parallelism = int(clamp(int(orch.get("parallelism", 1)), 1, 64))

    notif = raw.get("notifications", {})
    slack_webhook_url = env_str("SLACK_WEBHOOK_URL") or notif.get("slack_webhook_url")

    return OrchestratorConfig(
        run_id=run_id,
        log_file=log_file,
        parallelism=parallelism,
        thresholds=parse_thresholds(raw),
        targets=parse_targets(raw),
        global_checks=parse_global_checks(raw),
        slack_webhook_url=slack_webhook_url,
        smtp=notif.get("smtp"),
        sms=notif.get("sms"),
    )


# =============================================================================
# CLI Entry Point / CLI 進入點 / CLI 入口点
# =============================================================================

def install_signal_handlers(on_stop) -> None:
    """Install SIGINT/SIGTERM handlers / 安裝信號處理器"""
    def handler(signum, frame):
        on_stop()
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="AI Deployment Orchestrator / AI 部署編排器"
    )
    ap.add_argument("--config", required=True, help="Path to config.toml / 配置檔案路徑")
    ap.add_argument("--run-id", default=f"run-{int(time.time())}", help="Run identifier / 執行識別碼")
    ap.add_argument("--promote", action="store_true", help="Run promote step / 執行升級步驟")
    ap.add_argument("--maintenance", action="store_true", help="Run maintenance tasks / 執行維護任務")
    args = ap.parse_args()

    raw = load_toml(args.config)
    cfg = build_orchestrator_config(raw, run_id=args.run_id)

    logger = setup_logging(cfg.log_file)
    notifier = build_notifier_from_cfg(raw, logger, cfg.run_id)

    orch = Orchestrator(cfg, logger, notifier)
    install_signal_handlers(orch.stop)

    if args.maintenance:
        maint = raw.get("maintenance", {})
        backup_cmd = list(maint["backup_cmd"]) if maint.get("backup_cmd") else None
        restore_verify_cmd = list(maint["restore_verify_cmd"]) if maint.get("restore_verify_cmd") else None
        timeout_s = int(maint.get("timeout_s", 1800))
        ok = run_maintenance(logger, cfg.run_id, notifier, backup_cmd, restore_verify_cmd, timeout_s)
        return 0 if ok else 2

    result = orch.execute(promote=args.promote)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
