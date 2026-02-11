# 文件: render_convention.py
# 作用：把 YAML 版公约草案转成 Markdown（便于提交/评审）
# 依赖：pyyaml（如无，可替换为任意YAML解析器）
import yaml

def render_md(doc: dict) -> str:
  c = doc["un_ai_global_governance_convention"]
  lines = []
  lines.append(f"# {c['meta']['title_zh']}")
  lines.append("")
  lines.append(f"- ID: {c['meta']['id']}")
  lines.append(f"- 版本: {c['meta']['version']}")
  lines.append(f"- 状态: {c['meta']['status']}")
  lines.append(f"- 日期: {c['meta']['date']}")
  lines.append("")
  lines.append("## 序言")
  lines.append(c.get("preamble","").strip())
  lines.append("")
  lines.append("## 基本原则")
  for p in c.get("principles", []):
    lines.append(f"### {p['id']} {p['name']}")
    lines.append(p["norm"])
    lines.append("")
  lines.append("## 章节与条款")
  for ch in c.get("chapters", []):
    lines.append(f"## {ch['id']} {ch['title']}")
    for a in ch.get("articles", []):
      lines.append(f"### {a['id']} {a['title']}")
      # 只渲染常见字段，更多字段可按需扩展
      for key in ["objective","commitments","rules","rights","obligations","prohibitions","requirements","norms"]:
        if key in a:
          lines.append(f"**{key}**")
          val = a[key]
          if isinstance(val, list):
            for item in val:
              lines.append(f"- {item}")
          elif isinstance(val, dict):
            for k2, v2 in val.items():
              lines.append(f"- {k2}: {v2}")
          else:
            lines.append(str(val))
          lines.append("")
  return "\n".join(lines)

if __name__ == "__main__":
  with open("UN_AI_Global_Governance_Convention.zh.yaml", "r", encoding="utf-8") as f:
    doc = yaml.safe_load(f)
  md = render_md(doc)
  with open("UN_AI_Global_Governance_Convention.md", "w", encoding="utf-8") as f:
    f.write(md)
  print("OK -> UN_AI_Global_Governance_Convention.md")
