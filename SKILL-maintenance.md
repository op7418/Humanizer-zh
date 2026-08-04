---
name: humanizer-zh-maintenance
description: |
  维护更新 Humanizer-zh 仓库：同步上游 blader/humanizer 与 hardikpandya/stop-slop 的更新，
  用中文重写规则并标注中英差异，生成 README 示例，自举审阅后发布 PR。
  触发词：同步上游、更新规则、维护 humanizer-zh。
metadata:
  trigger: 维护 Humanizer-zh 仓库、同步上游规则
---

# Humanizer-zh 仓库维护

本技能指导维护更新 Humanizer-zh：获取上游更新、按中文语境重写、生成并审查示例、发布 PR。

## 上游基线

- **blader/humanizer**：`SKILL.md` 核心模式的来源（基于维基百科 Signs of AI writing）
- **hardikpandya/stop-slop**：核心规则速查、快速检查清单、质量评分的灵感来源

每次维护先确认上次同步的上游版本：在克隆的上游仓库中用 `git log --before="<上次同步日期>"` 定位引入时点版本，再用 `git log <引入版本>..HEAD` 列出其后所有更新。

## 流程

1. **获取上游更新**：对比上次同步版本与上游最新版，提取新增模式、新增章节、规则强化点，以及上游对旧内容的改写
2. **中文重写**：按项目现有中文风格重写
3. **标注中英差异**：英文特有的表达保留原文，其余在条目下加"注（中文适配）"说明中文对应表现
4. **生成 README 示例**：用更新后的技能真实执行改写（识别 → 草稿 → 审计 → 定稿）
5. **Review 并调整**：用技能规则审查技能文档与示例，发现问题先调整技能，再重新生成 README 示例
6. **自举审阅**：用技能审阅整个仓库（README、SKILL.md 自身），修复后重审，直到没有新的问题

## 验收标准

- 模式编号连续；新增内容用中文重写，英文特有的 AI 表达保留原文，不强行翻译成中文
- README 示例与所有技能规则都不冲突
- 不做没有实际意义的改动。确保修改内容最小且聚焦，方便审阅
