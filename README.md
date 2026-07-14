# 供应商发展 / 帮扶计划技能（supplier-development）

> 范式：交互引导式（纯文字版 .txt + Markdown .md）
> 面向 SQE 与供应商质量经理的低绩效供应商帮扶提升计划生成工具。

## 一句话说明
以"诊断-措施-跟踪-验证"闭环，把低绩效供应商的整改从空话变为可落地、可跟踪、可验证的帮扶计划文档（txt+md）。

## 适用角色
- SQE（供应商质量工程师）
- 供应商质量经理（SQM）

## 使用场景
- C/D 级供应商限期整改提升
- 重大客诉后专项帮扶
- 新供应商首批磨合辅导
- 战略供应商能力共建

## 帮扶闭环五步
1. 诊断（现状-差距）
2. 根因（5Why / 鱼骨图，可联动 root-cause-reasoning）
3. 措施（问题→措施+责任+期限+KPI）
4. 跟踪（里程碑门禁 30/60/90 天）
5. 验证（前后数据对比，达标闭环）

## 文件清单
- `SKILL.md`：技能主文件
- `README.md`：本说明
- `scripts/build_report.py`：帮扶 JSON → 纯文字版 .txt + Markdown .md 生成器

## 使用方法
```bash
# 内置小样本直接跑通，产出示意 txt+md 双件
python scripts/build_report.py

# 用自有数据
python scripts/build_report.py --input dev.json --out-dir ./输出
```

## 联动技能
- supplier-assessment（D/C 级自动建议转入帮扶）
- supplier-management-plan（方案第8段帮扶机制）
- supplier-quality-agreement（帮扶期特殊质量目标）
- root-cause-reasoning（本仓库，帮扶前根因分析）

## 注意事项
- 供应商真实绩效须来自用户提供；改善目标阈值标「待企业补充」；
- 本技能不替企业拍板"是否淘汰"，仅提供帮扶与升级路径；
- 不编造根因结论与真实数据。
