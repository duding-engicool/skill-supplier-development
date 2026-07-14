#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
供应商帮扶提升计划生成器
读入结构化帮扶 JSON，生成 Markdown + 网页版 HTML（主色 #C8102E）。

用法：
  python build_report.py --input dev.json --md-out 供应商帮扶计划.md --html-out 供应商帮扶计划.html
  python build_report.py                                  # 内置小样本，直接产出示意双版

输入 JSON 结构：
{
  "plan_title": "供应商帮扶提升计划",
  "supplier": "供应商名称",
  "background": "低绩效表现摘要",
  "current_level": "D级",
  "target_level": "B级",
  "issues": [{"area":"质量","problem":"...","evidence":"..."}],
  "actions": [
    {"no":"1","issue":"对应问题域","action":"提升措施","owner":"责任方","due":"期限","kpi":"衡量指标"},
    ...
  ],
  "milestones": [{"phase":"阶段","time":"时间","gate":"验证门禁"}],
  "tracking": "跟踪机制说明",
  "pending": ["待企业补充项"]
}
"""

import argparse
import json
import sys
import html
from datetime import datetime

PRIMARY = "#C8102E"


def esc(s):
    return html.escape(str(s), quote=True)


def load_dev(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_md(d):
    L = []
    L.append(f"# {d.get('plan_title','供应商帮扶提升计划')}\n")
    L.append("## 一、计划概览\n")
    L.append(f"- 供应商：{d.get('supplier','')}")
    L.append(f"- 当前等级：{d.get('current_level','')}  →  目标等级：{d.get('target_level','')}")
    L.append(f"- 生成日期：{datetime.now().strftime('%Y-%m-%d')}\n")
    L.append("## 二、背景与诊断\n")
    L.append(d.get("background", "（待企业补充）"))
    L.append("\n## 三、问题清单\n")
    L.append("| 问题域 | 表现 | 证据 |")
    L.append("|--------|------|------|")
    for it in d.get("issues", []) or []:
        L.append(f"| {it.get('area','')} | {it.get('problem','')} | {it.get('evidence','')} |")
    if not d.get("issues"):
        L.append("| （待企业补充） | | |")
    L.append("")
    L.append("## 四、提升措施\n")
    L.append("| 编号 | 对应问题 | 措施 | 责任方 | 期限 | 衡量KPI |")
    L.append("|------|----------|------|--------|------|----------|")
    for a in d.get("actions", []) or []:
        L.append(f"| {a.get('no','')} | {a.get('issue','')} | {a.get('action','')} | {a.get('owner','')} | {a.get('due','')} | {a.get('kpi','')} |")
    L.append("")
    L.append("## 五、里程碑与验证门禁\n")
    L.append("| 阶段 | 时间 | 验证门禁 |")
    L.append("|------|------|----------|")
    for m in d.get("milestones", []) or []:
        L.append(f"| {m.get('phase','')} | {m.get('time','')} | {m.get('gate','')} |")
    L.append("")
    L.append("## 六、跟踪机制\n")
    L.append(d.get("tracking", "（待企业补充）"))
    pend = d.get("pending", [])
    if pend:
        L.append("\n## 七、待企业补充项\n")
        for x in pend:
            L.append(f"- 〔待企业补充〕{x}")
    L.append(f"\n> 本报告由供应商发展/帮扶技能生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    return "\n".join(L)


CSS = f"""
:root{{--primary:{PRIMARY};--bg:#fafafa;--card:#ffffff;--ink:#1f2937;--muted:#6b7280;}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.75;padding:32px}}
.wrap{{max-width:1000px;margin:0 auto}}
header{{text-align:center;padding:26px 0 16px;border-bottom:3px solid var(--primary);margin-bottom:26px}}
header h1{{font-size:27px}}
header .meta{{color:var(--muted);font-size:14px;margin-top:10px}}
.sec{{background:var(--card);border-radius:14px;padding:22px 26px;box-shadow:0 4px 16px rgba(0,0,0,.05);margin-bottom:20px}}
.sec h2{{font-size:20px;margin-bottom:12px;border-left:5px solid var(--primary);padding-left:12px}}
.sec p{{font-size:15px;margin:6px 0}}
table{{width:100%;border-collapse:collapse;margin-top:10px;font-size:14px}}
th,td{{border:1px solid #e5e7eb;padding:9px 12px;text-align:left;vertical-align:top}}
th{{background:var(--primary);color:#fff}}
.pend{{background:#fff7f8;border:1px dashed var(--primary);border-radius:12px;padding:16px 22px}}
.pend h2{{color:var(--primary);border:none;padding:0;margin-bottom:8px}}
footer{{text-align:center;color:var(--muted);font-size:12px;margin-top:18px}}
"""


def build_html(d):
    issues_rows = "\n".join(
        f"<tr><td>{esc(it.get('area',''))}</td><td>{esc(it.get('problem',''))}</td><td>{esc(it.get('evidence',''))}</td></tr>"
        for it in (d.get("issues", []) or [{"area":"（待企业补充）", "problem": "", "evidence": ""}])
    )
    act_rows = "\n".join(
        f"<tr><td>{esc(a.get('no',''))}</td><td>{esc(a.get('issue',''))}</td><td>{esc(a.get('action',''))}</td>"
        f"<td>{esc(a.get('owner',''))}</td><td>{esc(a.get('due',''))}</td><td>{esc(a.get('kpi',''))}</td></tr>"
        for a in (d.get("actions", []) or [])
    )
    ms_rows = "\n".join(
        f"<tr><td>{esc(m.get('phase',''))}</td><td>{esc(m.get('time',''))}</td><td>{esc(m.get('gate',''))}</td></tr>"
        for m in (d.get("milestones", []) or [])
    )
    pend = d.get("pending", [])
    pend_html = ""
    if pend:
        items = "\n".join(f"<li>〔待企业补充〕{esc(x)}</li>" for x in pend)
        pend_html = f"<div class='pend'><h2>七、待企业补充项</h2><ul>{items}</ul></div>"
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(d.get('plan_title','供应商帮扶提升计划'))}</title>
<style>{CSS}</style></head>
<body><div class="wrap">
<header>
  <h1>{esc(d.get('plan_title','供应商帮扶提升计划'))}</h1>
  <div class="meta">供应商：{esc(d.get('supplier',''))} ｜ {esc(d.get('current_level',''))} → {esc(d.get('target_level',''))} ｜ 生成：{datetime.now().strftime('%Y-%m-%d')}</div>
</header>
<section class="sec"><h2>一、背景与诊断</h2><p>{esc(d.get('background','（待企业补充）'))}</p></section>
<section class="sec"><h2>二、问题清单</h2>
<table><thead><tr><th>问题域</th><th>表现</th><th>证据</th></tr></thead><tbody>{issues_rows}</tbody></table></section>
<section class="sec"><h2>三、提升措施</h2>
<table><thead><tr><th>编号</th><th>对应问题</th><th>措施</th><th>责任方</th><th>期限</th><th>衡量KPI</th></tr></thead><tbody>{act_rows}</tbody></table></section>
<section class="sec"><h2>四、里程碑与验证门禁</h2>
<table><thead><tr><th>阶段</th><th>时间</th><th>验证门禁</th></tr></thead><tbody>{ms_rows}</tbody></table></section>
<section class="sec"><h2>五、跟踪机制</h2><p>{esc(d.get('tracking','（待企业补充）'))}</p></section>
{pend_html}
<footer>本报告由供应商发展/帮扶技能生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}</footer>
</div></body></html>"""


SAMPLE_DEV = {
    "plan_title": "供应商帮扶提升计划（示意）",
    "supplier": "恒锐精密",
    "background": "近12个月批次合格率95.2%、PPM约580，8D回复平均12天且措施空泛，过程审核C级。综合判定为'能力不足型'低绩效供方，需限期帮扶。",
    "current_level": "C级",
    "target_level": "B级",
    "issues": [
        {"area": "质量", "problem": "PPM偏高(≈580)，尺寸超差与划伤为主", "evidence": "来料检验月报"},
        {"area": "改善意愿", "problem": "8D平均12天回复、措施空泛无证据", "evidence": "8D系统统计"},
        {"area": "体系", "problem": "过程审核C级，变更管理无书面流程", "evidence": "QPA审核报告"}
    ],
    "actions": [
        {"no": "1", "issue": "质量-PPM高", "action": "关键尺寸SPC管控+防错装置+进货加严检验", "owner": "供应商质量部/我方SQE支持", "due": "60天", "kpi": "PPM由580降至≤300"},
        {"no": "2", "issue": "改善意愿-8D空泛", "action": "8D模板培训+措施复核机制+5日回复考核", "owner": "供应商质量部", "due": "30天", "kpi": "8D回复≤5天、措施带量化目标"},
        {"no": "3", "issue": "体系-变更管理弱", "action": "建立4M1E变更通知流程并嵌入考核", "owner": "供应商体系工程师", "due": "45天", "kpi": "变更主动通知率100%"}
    ],
    "milestones": [
        {"phase": "M1", "time": "30天", "gate": "8D机制上线，回复时效达标"},
        {"phase": "M2", "time": "60天", "gate": "PPM降至目标，防错装置验证通过"},
        {"phase": "M3", "time": "90天", "gate": "过程审核复评≥B级，计划闭环"}
    ],
    "tracking": "SQE双周回顾进展，供应商月度提交改善数据；连续2次里程碑未达触发升级（驻厂辅导/减份额）。",
    "pending": [
        "PPM/合格率具体目标值（按企业实际填入）",
        "帮扶资源投入与考核奖惩细则",
        "未达标时的淘汰/替代触发条件"
    ]
}


def main():
    ap = argparse.ArgumentParser(description="供应商帮扶提升计划生成器")
    ap.add_argument("--input", help="结构化帮扶 JSON 路径（缺省使用内置小样本）")
    ap.add_argument("--md-out", default="供应商帮扶计划.md", help="输出 MD 路径")
    ap.add_argument("--html-out", default="供应商帮扶计划.html", help="输出 HTML 路径")
    args = ap.parse_args()

    try:
        dev = load_dev(args.input) if args.input else SAMPLE_DEV
    except Exception as e:
        sys.stderr.write(f"读取输入失败：{e}\n")
        sys.exit(1)

    with open(args.md_out, "w", encoding="utf-8") as f:
        f.write(build_md(dev))
    sys.stderr.write(f"MD 已生成：{args.md_out}\n")

    with open(args.html_out, "w", encoding="utf-8") as f:
        f.write(build_html(dev))
    sys.stderr.write(f"HTML 已生成：{args.html_out}\n")


if __name__ == "__main__":
    main()
