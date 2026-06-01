# Humanizer-zh: AI 写作去痕工具（中文版）

> **声明：**
> - 本项目的核心文件翻译自 [blader/humanizer](https://github.com/blader/humanizer/tree/main)
> - 实用工具部分（核心规则、快速检查清单、质量评分）参考了 [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)
> - 原项目基于维基百科的 [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) 指南

---

## 项目简介

Humanizer-zh 是一个用于去除文本中 AI 生成痕迹的 Agent Skill，帮助你将 AI 生成的内容改写得更自然、更像人类书写的文本。

本项目适用于：
- 编辑和审阅 AI 生成的内容
- 提升文章的人性化程度
- 学习识别 AI 写作的常见模式

## 安装

### 方法一：通过 npx 一键安装（推荐）

```bash
npx skills add https://github.com/op7418/Humanizer-zh.git
```

这是最简单的安装方式，会自动将技能安装到正确的目录。

### 方法二：通过 Git 克隆

```bash
# 克隆到 Claude Code 的 skills 目录
git clone https://github.com/op7418/Humanizer-zh.git ~/.claude/skills/humanizer-zh
```

### 方法三：手动安装

1. 下载本项目的 ZIP 文件或克隆到本地
2. 将 `Humanizer-zh` 文件夹复制到 Claude Code 的 skills 目录：
   - **macOS/Linux**: `~/.claude/skills/`
   - **Windows**: `%USERPROFILE%\.claude\skills\`

3. 确保文件夹结构如下：
   ```
   ~/.claude/skills/humanizer-zh/
   ├── SKILL.md                        # 主文件（核心规则 + 流程）
   ├── README.md                       # 说明文档
   └── references/                     # 按需加载的参考文件
       ├── content-patterns.md         # 模式 1-6：内容层面
       ├── language-patterns.md        # 模式 7-12：语言/语法层面
       ├── style-patterns.md           # 模式 13-18：风格/排版层面
       ├── communication-patterns.md   # 模式 19-24：交流/填充层面
       └── scoring.md                  # 质量评分 + 示例
   ```

## 使用方法

### 方式一：直接描述需求

在对话中直接说：

```
帮我检查一下这段文字有没有 AI 味
```

或者：

```
请把下面这段话改得更自然一些
```

### 方式二：明确引用技能

如果你明确想调用此技能，可以这样说：

```
使用 humanizer-zh 技能帮我处理这段文本
```

## 技能说明

当激活此技能时，Claude 会：

1. **识别 AI 模式** - 扫描文本中 24 种常见的 AI 写作痕迹
2. **重写问题片段** - 用自然的替代方案替换 AI 痕迹
3. **保留含义** - 保持核心信息完整
4. **维持语调** - 匹配预期的语气（正式、随意、技术等）
5. **注入个性** - 不仅去除不良模式，还注入真实的个性

### 覆盖的 24 种模式

| 类别 | 模式 |
|------|------|
| **内容层面** | 夸大象征意义、知名度强调、肤浅分析、宣传语言、模糊归因、公式化挑战章节 |
| **语言层面** | AI 词汇、系动词回避、否定排比、三段式法则、同义词循环、虚假范围 |
| **风格层面** | 破折号滥用、粗体滥用、内联标题列表、表情符号、弯引号 |
| **交流层面** | 对话痕迹、截止日期免责声明、谄媚语气、填充短语、过度限定、空洞结论 |

## 质量评分

处理完成后，技能会从 5 个维度（各 10 分，总分 50）评估改写质量：

| 维度 | 评估标准 |
|------|----------|
| **直接性** | 直接陈述事实还是绕圈宣告？ |
| **节奏** | 句子长度是否变化？ |
| **信任度** | 是否尊重读者智慧？ |
| **真实性** | 听起来像真人说话吗？ |
| **精炼度** | 还有可删减的内容吗？ |

- 45-50 分：优秀，已去除 AI 痕迹
- 35-44 分：良好，仍有改进空间
- 低于 35 分：需要重新修订

## 示例

### 改写前（AI 味道）：

> 新的软件更新作为公司致力于创新的证明。此外，它提供了无缝、直观和强大的用户体验——确保用户能够高效地完成目标。这不仅仅是一次更新，而是我们思考生产力方式的革命。行业专家认为这将对整个行业产生持久影响，彰显了公司在不断演变的技术格局中的关键作用。

### 改写后（人性化）：

> 软件更新添加了批处理、键盘快捷键和离线模式。来自测试用户的早期反馈是积极的，大多数报告任务完成速度更快。

## 相关项目

- [blader/humanizer](https://github.com/blader/humanizer) - 原版 Humanizer（英文）
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) - 参考的实用工具
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) - 理论基础

## 许可证

MIT License
