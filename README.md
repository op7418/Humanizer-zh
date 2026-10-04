# Humanizer-zh：中文文本润色 Skill

[![skills.sh](https://skills.sh/b/op7418/Humanizer-zh)](https://skills.sh/op7418/Humanizer-zh)

编辑已有文章、评论和文档中的空话、重复及模板化表达，保留事实、确定程度和作者声音。输入是一段文字或一个文件，默认输出最终改写稿；没有问题的句子可以不改。

这是一份由 Agent 读取执行的编辑指导，不是独立的检测程序。它不能证明文章由谁撰写，也不保证通过任何 AI 检测器。

> 繁體中文說明請見 [README.zh-TW.md](README.zh-TW.md)。

> 2026-09-24 更新：新增台湾繁体中文用语规则，以及 Codex、Hermes Agent、Pi、OpenClaw 等 Agent 的安装方式。
>
> 2026-09-23 更新：重写了规则和示例，明确保留事实、作者立场和文体。普通的排比、破折号和连接词不再一律修改。详见 [更新记录](CHANGELOG.md)。

## 安装

本 Skill 遵循 [Agent Skills](https://agentskills.io) 开放格式：一个 `SKILL.md` 加上 `references/` 参考文件。安装后的目录名必须是小写的 `humanizer-zh`，与 `SKILL.md` 中的 `name` 一致。`references/zh-tw.md` 需要随 Skill 一起安装，只下载单个 `SKILL.md` 会缺少台湾繁体规则。

### 方法一：npx 一键安装（推荐）

本 Skill 已收录于 [skills.sh](https://skills.sh/op7418/Humanizer-zh)，可用简写安装：

```bash
npx skills add op7418/Humanizer-zh
```

也可以指定安装范围和 Agent：

```bash
# 交互式选择要安装的 Agent
npx skills add https://github.com/op7418/Humanizer-zh -g

# 或直接指定 Agent
npx skills add https://github.com/op7418/Humanizer-zh -g -a claude-code codex hermes-agent pi openclaw
```

`-g` 安装到用户目录，所有项目可用；去掉 `-g` 则安装到当前项目。[skills CLI](https://github.com/vercel-labs/skills) 把文件放在 `~/.agents/skills/humanizer-zh`，再为需要的 Agent 建立符号链接。更新用 `npx skills update`。

| Agent | `-a` 参数 | 调用方式 | `-g` 安装位置 |
|---|---|---|---|
| Claude Code | `claude-code` | `/humanizer-zh` | `~/.claude/skills/`（链接） |
| OpenAI Codex | `codex` | `$humanizer-zh` 或 `/skills` | `~/.agents/skills/` |
| Hermes Agent | `hermes-agent` | `/humanizer-zh` | `~/.hermes/skills/`（链接） |
| Pi | `pi` | `/skill:humanizer-zh` | `~/.pi/agent/skills/`（链接） |
| OpenClaw | `openclaw` | `/skill humanizer-zh` | `~/.openclaw/skills/`（链接） |
| Gemini CLI | `gemini-cli` | 按描述自动启用 | `~/.agents/skills/` |
| OpenCode | `opencode` | 按描述自动启用 | `~/.agents/skills/` |
| GitHub Copilot | `github-copilot` | `/humanizer-zh` | `~/.agents/skills/` |
| Cursor | `cursor` | `/humanizer-zh` | `~/.agents/skills/` |

安装位置为 2026-09-24 以 skills CLI 实测的结果，CLI 改版后可能不同，以安装完成时的提示为准。所有 Agent 也都能按描述自动选用本 Skill。

### 方法二：Git 克隆到各 Agent

克隆时指定目录名 `humanizer-zh`。以后在该目录执行 `git pull` 即可更新。

**Claude Code**

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.claude/skills/humanizer-zh
```

在对话中输入 `/humanizer-zh`，或直接要求“用 humanizer-zh 润色”。

**OpenAI Codex**

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.agents/skills/humanizer-zh
```

用 `$humanizer-zh` 明确调用，或输入 `/skills` 选择；Codex 也会按描述自动选用。旧位置 `~/.codex/skills/` 仍会读取，但官方已不推荐。Skill 没出现时重启 Codex。

**Hermes Agent**

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.hermes/skills/humanizer-zh
```

在对话中输入 `/humanizer-zh`；已在运行的会话执行 `/reload-skills` 重新扫描。放在项目内的 `.hermes/skills/` 需要先执行 `hermes skills trust`。不要只用 `SKILL.md` 的原始网址安装，那样不会下载 `references/`。

**Pi**

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.pi/agent/skills/humanizer-zh
```

用 `/skill:humanizer-zh` 调用；修改或新增 Skill 后执行 `/reload`。Pi 也会读取 `~/.agents/skills/`。

**OpenClaw**

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.openclaw/skills/humanizer-zh
```

用 `/skill humanizer-zh` 调用；斜杠命令会把连字符换成下划线，也可以输入 `/humanizer_zh`。Skill 在会话开始时载入，新装的 Skill 在新会话中生效。

**Gemini CLI、OpenCode、GitHub Copilot、Cursor**

这些 Agent 都会读取跨工具目录 `~/.agents/skills/`：

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.agents/skills/humanizer-zh
```

### 多个 Agent 共用一份

`~/.agents/skills/` 可被 Codex、Pi、OpenClaw、Gemini CLI、OpenCode、GitHub Copilot 和 Cursor 读取。Claude Code 与 Hermes Agent 默认不读这个目录，可用符号链接共用同一份文件：

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.agents/skills/humanizer-zh
mkdir -p ~/.claude/skills ~/.hermes/skills
ln -s ~/.agents/skills/humanizer-zh ~/.claude/skills/humanizer-zh
ln -s ~/.agents/skills/humanizer-zh ~/.hermes/skills/humanizer-zh
```

同一个 Skill 不要在多个会被同一 Agent 读取的目录各放一份，否则可能重复载入或互相覆盖。

### Windows

路径中的 `~` 换成 `%USERPROFILE%`，例如 `%USERPROFILE%\.claude\skills\humanizer-zh`。建立链接可在管理员命令提示符中使用 `mklink /D`，或直接复制整个目录。

### 不支持 Skill 的 Agent

在项目的 `AGENTS.md`（或该工具的规则文件）中加入：

```markdown
编辑或润色中文文字时，先读取 <安装路径>/humanizer-zh/SKILL.md，按其中的规则执行。
```

## 使用

粘贴文本：

```text
请用 humanizer-zh 润色下面的文章，保留技术评论的语气：
[原文]
```

编辑文件：

```text
请用 humanizer-zh 润色 article.md 中的正文。
```

台湾繁体文本：

```text
請用 humanizer-zh 潤飾這篇文章，改成台灣用語，保留原本的語氣：
[原文]
```

输入是繁体中文时，Skill 会读取 [references/zh-tw.md](references/zh-tw.md)，处理对岸用语、简转繁错字、「」标点和翻译腔；港澳繁体保留原地区用语，不擅自做简繁转换。

只审阅时说明“给出建议，不修改文件”。有作者样本时可一并提供，Skill 会借鉴表达习惯，但不会把样本中的经历、数据或观点搬入原文。

## 改写示例

以下均为教学用输入，没有未展示的补充材料。

**产品介绍，缺少数据：**

> 原文：该方案稳定可靠、快速响应、易于维护。
>
> 改写：这套方案运行稳定、响应快，也方便维护。

没有补写上线时间、响应速度或维护成本。原文缺少证据，可以向作者索取，不能用润色补出数据。

**故障反馈，有不确定性：**

> 原文：该问题被社区多次报告，被认为可能与内存泄漏有关，但原因尚未确认。
>
> 改写：社区多次报告这个问题。它被认为可能与内存泄漏有关，但原因尚未确认。

保留“可能有关”和“尚未确认”，不把推测改成因果结论，也不把原因判断擅自归给社区。

**更新说明，有真实的三项功能：**

> 原文：这次更新彰显了团队对创新的追求。它新增导出、搜索和批量重命名。离线编辑计划在下一版推出，目前尚未完成测试。
>
> 改写：这次更新新增导出、搜索和批量重命名。离线编辑计划在下一版推出，目前尚未完成测试。

保留三个功能，不为避开三段式删项或凑项；计划和测试状态保持原意。

**已经清楚的文字：**

> 原文：先保存文件，再关闭窗口。未保存的修改会丢失。
>
> 改写：先保存文件，再关闭窗口。未保存的修改会丢失。

不要求每次调用都产生修改。

## 编辑原则

约束优先级是：保留信息和确定程度，遵守用户范围与文体，匹配作者声音，再处理具体表达问题。模式命中不能覆盖这些要求。

- 不编造功能、数据、来源、人物身份或第一人称经历。
- 保留否定、条件、归因、范围、时间和完成状态；“可能”不变成“确定”，“计划”不变成“已经”。
- 三项列表、四字格、被动句、破折号和连接词按作用判断，不机械删除。
- 随笔可以保留个性，学术和商务文本保留正式程度；不把所有文章改成同一种口语。
- 文件编辑默认保留代码、命令、路径、链接目标、YAML、数据、标题和锚点。改标题或结构需要检查引用。
- 默认只交付最终稿，不要求展示中间草稿、命中清单或自评分。

## 模式目录

共 39 个检查点：1–31 沿用 PR #39 的 A–F 分类；32–39 为 G 组，来自 [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) 的语料实测（629 篇、约 283 万字，五个模型对照人类写作）。这是编辑问题清单，不是作者身份检测标准。

| 分类 | 检查点 |
|---|---|
| A：铺垫代替陈述（1–5） | 假对比、戏剧性碎片、伪深度、起跑式铺垫、无对象的辩护 |
| B：公式化节奏（6–11） | 强凑三段式、重复开头、万能破折号、限定堆叠、生造复合词、被动与缺主语 |
| C：拔高与借权威（12–18） | 空泛高频词、意义拔高、模糊关联、句尾拔高、宣传语、权威背书、复杂系动词 |
| D：公式化排版（19–21） | 无效粗体、装饰性标题、引号和标点 |
| E：聊天与草稿残留（22–25） | 客服腔、重复免责与猜测填充、首句复读标题、编辑过程残留 |
| F：中文补充检查（26–31） | 长定语、“进行＋动词”、被字句堆叠、四字词排比、万能背景、套话收尾 |
| G：语料实测特征（32–39） | 段首零回指评论、冒号滥用、序数词小标题、拟人化喻体、概括盖掉已有数据、顿号罗列、相邻句同构、四种译文句式 |

同一份实测也显示，比喻、正文问句、句内排比、正文里的“首先……其次”、句长参差等在人类文本中同样常见甚至更多。`SKILL.md` 把它们列为“实测不构成修改理由”，避免越改越不像人写的。

`SKILL.md` 中每条只保留一行修改条件与保留边界；前后示例和保留示例在 [references/patterns.md](references/patterns.md)，Agent 不确定时再读取。

## 验证

[测试说明](tests/README.md)包含 32 个短文本案例（其中 7 个为繁体、7 个针对 G 组）、一个 Markdown 文件样例、结构检查脚本和台湾繁体用语检查脚本。本次更新还做了旧版与修订版的长文对照，检查数字、条件、归因、作者态度和文件结构。单次、有限样例不能代表所有模型和文体；不能用字数下降或模型自评分证明效果。

## 来源与许可

- [blader/humanizer v3.0.0](https://github.com/blader/humanizer/blob/v3.0.0/SKILL.md)：原项目及 A–E 分类、声音校准、文件模式的来源。
- [Humanizer-zh PR #39](https://github.com/op7418/Humanizer-zh/pull/39)：本次修订的结构基础与中文检查点来源。
- [Humanizer-zh PR #34](https://github.com/op7418/Humanizer-zh/pull/34)：示例保真修复的对照参考。本修订没有直接合并该分支。
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)：简洁表达与编辑检查的参考来源。
- [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)（MIT）：G 组检查点、“实测不构成修改理由”及倍数数据的来源，许可见 [licenses/](licenses/lieflat-less-ai-tone.txt)。
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)：原项目的观察来源。

遵循仓库中的 [MIT License](LICENSE)。
