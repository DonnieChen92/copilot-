# 文件: un_ai_convention_policy.rego
# 用 OPA/Rego 做“公约合规检查”的示例（policy-as-code）
package un_ai_gov

default allow := false

# ---- 参数约定 ----
# input.manifest = ai_system_compliance_manifest.json
# input.use_case  = { "domain": "...", "lethal": false, "mass_surveillance": false, ... }

prohibited_reasons[reason] {
  input.use_case.lethal == true
  input.use_case.human_effective_control == false
  reason := "禁止：致命武力决策缺乏人类有效控制（A10/A11）"
}

prohibited_reasons[reason] {
  input.use_case.social_scoring == true
  input.use_case.due_process == false
  reason := "禁止：缺乏正当程序的普遍性社会评分与惩罚（A10）"
}

prohibited_reasons[reason] {
  input.use_case.mass_surveillance == true
  input.use_case.purpose == "rights_suppression"
  reason := "禁止：以压制基本权利为目的的大规模监控（A10）"
}

high_risk_required[req] {
  input.manifest.risk.level == "high"
  req := "要求：高风险系统必须登记 + 事前评估 + 独立审计 + 持续监测（A7）"
}

deny[msg] {
  count(prohibited_reasons) > 0
  msg := prohibited_reasons[_]
}

deny[msg] {
  input.manifest.risk.level == "high"
  not input.manifest.audit.third_party_audit.performed
  msg := "拒绝：高风险系统缺少独立第三方审计（A7）"
}

deny[msg] {
  input.manifest.risk.high_consequence_decision == true
  not input.manifest.transparency.explainability.available
  msg := "拒绝：高后果决策缺乏可解释与人工复核通道（A6/A12）"
}

deny[msg] {
  input.manifest.data_governance.cross_border_transfer.enabled == true
  not input.manifest.data_governance.cross_border_transfer.equivalent_protection_assessment
  msg := "拒绝：跨境数据流动缺少等效保护评估（A9）"
}

allow {
  count(deny) == 0
}
