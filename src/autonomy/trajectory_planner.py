"""
Trajectory Planner for Tesla FSD / Tesla FSD 軌跡規劃器 / Tesla FSD 轨迹规划器
==============================================================================
Hohmann transfer analog for road path optimization, with safety constraints
(radiation belt-like hazard avoidance for space-linked autonomy).

霍曼轉移類比用於道路路徑最佳化，含安全約束（類似輻射帶的危險迴避用於太空連結自駕）。
霍曼转移类比用于道路路径优化，含安全约束（类似辐射带的危险回避用于太空连接自驾）。

Mathematical Foundation / 數學基礎 / 数学基础:
- Orbital mechanics: v = sqrt(μ/r) / 軌道力學
- Hohmann transfer: Δv₁ = sqrt(μ/r₁) × (sqrt(2r₂/(r₁+r₂)) - 1)
- Transfer time: T = π × sqrt(a³/μ) where a = (r₁+r₂)/2
  轉移時間 / 转移时间
- Safe altitude check: avoid radiation belt analogs
  安全高度檢查：迴避輻射帶類比區域

Integration / 整合:
- Maps orbital maneuvers to road trajectory optimization
  將軌道機動映射到道路軌跡最佳化
- Hazard zones = radiation belts = road danger areas
  危險區域 = 輻射帶 = 道路危險區域

Author: Donnie Chen (donniechen92@gmail.com)
"""

import math
from dataclasses import dataclass


# Constants / 常數 / 常数
MU_EARTH = 3.986e14        # Earth gravitational parameter (m³/s²) / 地球重力參數
R_EARTH = 6371e3           # Earth radius (m) / 地球半徑


@dataclass
class TransferResult:
    """Trajectory transfer result / 軌跡轉移結果 / 轨迹转移结果"""
    delta_v1: float            # First burn Δv (m/s) / 第一次燃燒 Δv
    delta_v2: float            # Second burn Δv (m/s) / 第二次燃燒 Δv
    total_delta_v: float       # Total Δv (m/s) / 總 Δv
    transfer_time_hours: float # Transfer time (hours) / 轉移時間（小時）
    safe_departure: bool       # Departure altitude safe / 出發高度安全
    safe_arrival: bool         # Arrival altitude safe / 到達高度安全


def orbital_velocity(r: float, mu: float = MU_EARTH) -> float:
    """
    Circular orbital velocity / 圓軌道速度 / 圆轨道速度

    v = sqrt(μ / r)

    Args:
        r: Orbital radius (m) / 軌道半徑
        mu: Gravitational parameter / 重力參數
    """
    return math.sqrt(mu / r)


def hohmann_transfer(
    alt1_km: float = 400.0,
    alt2_km: float = 2000.0,
    mu: float = MU_EARTH,
) -> TransferResult:
    """
    Calculate Hohmann transfer trajectory.
    計算霍曼轉移軌跡。
    计算霍曼转移轨迹。

    Args:
        alt1_km: Departure altitude (km) / 出發高度（公里）
        alt2_km: Arrival altitude (km) / 到達高度（公里）
        mu: Gravitational parameter / 重力參數

    Returns:
        TransferResult with Δv and timing / 包含 Δv 和時序的結果

    Equations / 方程式:
        Δv₁ = sqrt(μ/r₁) × (sqrt(2r₂/(r₁+r₂)) - 1)
        Δv₂ = sqrt(μ/r₂) - sqrt(μ × (2/r₂ - 1/a))
        T = π × sqrt(a³/μ), a = (r₁+r₂)/2
    """
    r1 = R_EARTH + alt1_km * 1e3  # Convert km to m / 公里轉公尺
    r2 = R_EARTH + alt2_km * 1e3

    # Semi-major axis of transfer orbit / 轉移軌道半長軸
    a_transfer = (r1 + r2) / 2.0

    # First burn: departure / 第一次燃燒：出發
    v1_circular = math.sqrt(mu / r1)
    v1_transfer = math.sqrt(mu * (2.0 / r1 - 1.0 / a_transfer))
    delta_v1 = abs(v1_transfer - v1_circular)

    # Second burn: arrival / 第二次燃燒：到達
    v2_circular = math.sqrt(mu / r2)
    v2_transfer = math.sqrt(mu * (2.0 / r2 - 1.0 / a_transfer))
    delta_v2 = abs(v2_circular - v2_transfer)

    # Transfer time / 轉移時間
    transfer_time_s = math.pi * math.sqrt(a_transfer**3 / mu)
    transfer_time_h = transfer_time_s / 3600.0

    # Safety check: radiation belt avoidance / 安全檢查：輻射帶迴避
    # Inner Van Allen belt: 400-1000 km, Outer: 13000-60000 km
    # 內范艾倫帶：400-1000 km，外帶：13000-60000 km
    safe1 = safe_altitude(alt1_km)
    safe2 = safe_altitude(alt2_km)

    return TransferResult(
        delta_v1=round(delta_v1, 2),
        delta_v2=round(delta_v2, 2),
        total_delta_v=round(delta_v1 + delta_v2, 2),
        transfer_time_hours=round(transfer_time_h, 2),
        safe_departure=safe1,
        safe_arrival=safe2,
    )


def safe_altitude(alt_km: float) -> bool:
    """
    Check if altitude avoids radiation belts.
    檢查高度是否迴避輻射帶。
    检查高度是否回避辐射带。

    Safe zones / 安全區域:
    - Below 400 km (LEO, beneath inner belt) / 低於 400 km（低地軌道）
    - 1000-13000 km (gap between belts) / 1000-13000 km（帶間間隙）
    - Above 60000 km (beyond outer belt) / 高於 60000 km（超出外帶）

    Hazard zones / 危險區域:
    - 400-1000 km (inner Van Allen belt) / 內范艾倫帶
    - 13000-60000 km (outer Van Allen belt) / 外范艾倫帶
    """
    if alt_km < 400:
        return True       # Below inner belt / 低於內帶
    if 1000 < alt_km < 13000:
        return True       # Between belts / 帶間
    if alt_km > 60000:
        return True       # Above outer belt / 高於外帶
    return False          # Inside a belt / 在帶內


def road_trajectory_analog(
    start_speed_kmh: float,
    target_speed_kmh: float,
    distance_km: float,
) -> dict[str, float]:
    """
    Road trajectory optimization (analog to orbital transfer).
    道路軌跡最佳化（軌道轉移類比）。
    道路轨迹优化（轨道转移类比）。

    Maps orbital mechanics concepts to road driving:
    將軌道力學概念映射到道路駕駛：
    - Δv → acceleration/deceleration needed / 所需加速/減速
    - Transfer time → travel time / 行程時間
    - Safe altitude → safe speed range / 安全速度範圍

    Args:
        start_speed_kmh: Current speed (km/h) / 當前速度
        target_speed_kmh: Target speed (km/h) / 目標速度
        distance_km: Distance to cover (km) / 需行駛距離
    """
    # Convert to m/s / 轉換為 m/s
    v1 = start_speed_kmh / 3.6
    v2 = target_speed_kmh / 3.6
    d = distance_km * 1000

    delta_v = abs(v2 - v1)

    # Estimated time using average speed / 使用平均速度估算時間
    avg_speed = (v1 + v2) / 2.0
    travel_time_s = d / avg_speed if avg_speed > 0 else float("inf")

    # Required acceleration / 所需加速度
    acceleration = delta_v / travel_time_s if travel_time_s > 0 else 0

    # Safety: speed within limits / 安全：速度在限制範圍內
    safe_speed = 30 <= target_speed_kmh <= 120  # km/h

    return {
        "delta_v_ms": round(delta_v, 2),
        "travel_time_min": round(travel_time_s / 60, 2),
        "acceleration_ms2": round(acceleration, 4),
        "safe_speed": safe_speed,
        "energy_kj": round(0.5 * 1500 * delta_v**2 / 1000, 2),  # KE for ~1500kg car
    }


# --- Demo / 示範 / 示范 ---
if __name__ == "__main__":
    # Orbital trajectory / 軌道軌跡
    print("=== Hohmann Transfer / 霍曼轉移 ===")
    result = hohmann_transfer(alt1_km=400, alt2_km=2000)
    print(f"Delta V1 / 第一次Δv: {result.delta_v1} m/s")
    print(f"Delta V2 / 第二次Δv: {result.delta_v2} m/s")
    print(f"Total Delta V / 總Δv: {result.total_delta_v} m/s")
    print(f"Transfer time / 轉移時間: {result.transfer_time_hours} hours")
    print(f"Safe departure / 安全出發: {result.safe_departure}")
    print(f"Safe arrival / 安全到達: {result.safe_arrival}")

    # Road analog / 道路類比
    print("\n=== Road Trajectory / 道路軌跡 ===")
    road = road_trajectory_analog(
        start_speed_kmh=60,
        target_speed_kmh=100,
        distance_km=5,
    )
    print(f"Speed change / 速度變化: {road['delta_v_ms']} m/s")
    print(f"Travel time / 行程時間: {road['travel_time_min']} min")
    print(f"Acceleration / 加速度: {road['acceleration_ms2']} m/s²")
    print(f"Safe speed / 安全速度: {road['safe_speed']}")
    print(f"Energy / 能量: {road['energy_kj']} kJ")
