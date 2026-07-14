#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
供应商帮扶提升计划生成器
读入结构化帮扶 JSON，生成纯文字版 (.txt) + Markdown (.md) 双件文档。

用法：
  python build_report.py --input dev.json --out-dir ./输出
  python build_report.py                                  # 内置小样本，直接产出示意双件

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
import os
import sys
from datetime import datetime


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


def build_txt(d):
    sep = "=" * 48
    sub = "-" * 48
    L = []
    L.append(sep)
    L.append(d.get("plan_title", "供应商帮扶提升计划"))
    L.append(sep)
    L.append(f"供应商：{d.get('supplier','')}")
    L.append(f"当前等级：{d.get('current_level','')}  →  目标等级：{d.get('target_level','')}")
    L.append(f"生成日期：{datetime.now().strftime('%Y-%m-%d')}")
    L.append("")
    L.append("一、背景与诊断")
    L.append(sub)
    L.append(d.get("background", "（待企业补充）"))
    L.append("")
    L.append("二、问题清单")
    L.append(sub)
    for it in d.get("issues", []) or []:
        L.append(f"问题域：{it.get('area','')}")
        L.append(f"  表现：{it.get('problem','')}")
        L.append(f"  证据：{it.get('evidence','')}")
    if not d.get("issues"):
        L.append("（待企业补充）")
    L.append("")
    L.append("三、提升措施")
    L.append(sub)
    for a in d.get("actions", []) or []:
        L.append(f"{a.get('no','')} 〔对应问题：{a.get('issue','')}〕")
        L.append(f"  措施：{a.get('action','')}")
        L.append(f"  责任方：{a.get('owner','')} ｜ 期限：{a.get('due','')} ｜ 衡量KPI：{a.get('kpi','')}")
    L.append("")
    L.append("四、里程碑与验证门禁")
    L.append(sub)
    for m in d.get("milestones", []) or []:
        L.append(f"{m.get('phase','')} ｜ 时间：{m.get('time','')} ｜ 验证门禁：{m.get('gate','')}")
    L.append("")
    L.append("五、跟踪机制")
    L.append(sub)
    L.append(d.get("tracking", "（待企业补充）"))
    pend = d.get("pending", [])
    if pend:
        L.append("")
        L.append("六、待企业补充项")
        L.append(sub)
        for x in pend:
            L.append(f"  - 〔待企业补充〕{x}")
    L.append("")
    L.append(f"本报告由供应商发展/帮扶技能生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    return "\n".join(L)


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
    ap = argparse.ArgumentParser(description="供应商帮扶提升计划生成器（txt+md）")
    ap.add_argument("--input", help="结构化帮扶 JSON 路径（缺省使用内置小样本）")
    ap.add_argument("--out-dir", default=os.getcwd(), help="输出目录（默认当前工作目录）")
    ap.add_argument("--format", choices=["txt", "md", "all"], default="all", help="输出格式，默认 all（txt+md）")
    args = ap.parse_args()

    try:
        dev = load_dev(args.input) if args.input else SAMPLE_DEV
    except Exception as e:
        sys.stderr.write(f"读取输入失败：{e}\n")
        sys.exit(1)

    os.makedirs(args.out_dir, exist_ok=True)
    date_tag = datetime.now().strftime("%Y%m%d")
    base = f"供应商帮扶计划_{date_tag}"

    if args.format in ("md", "all"):
        md_path = os.path.join(args.out_dir, base + ".md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(build_md(dev))
        sys.stderr.write(f"MD 已生成：{md_path}\n")
    if args.format in ("txt", "all"):
        txt_path = os.path.join(args.out_dir, base + ".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(build_txt(dev))
        sys.stderr.write(f"TXT 已生成：{txt_path}\n")


if __name__ == "__main__":
    main()
