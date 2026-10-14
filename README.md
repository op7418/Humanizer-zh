# Humanizer-zh：中文文本润色 Skill

编辑已有文章、评论和文档中的空话、重复及模板化表达，保留事实、确定程度和作者声音。输入是一段文字或一个文件，默认输出最终改写稿；没有问题的句子可以不改。

这是一份由 Agent 读取执行的编辑指导，不是独立的检测程序。它不能证明文章由谁撰写，也不保证通过任何 AI 检测器。

> 2026-09-23 更新：重写了规则和示例，明确保留事实、作者立场和文体。普通的排比、破折号和连接词不再一律修改。详见 [更新记录](CHANGELOG.md)。

## 安装

本仓库只有根目录的一份 `SKILL.md`。Codex 和 Claude Code 通过各自的 marketplace 安装插件，Gemini CLI 直接安装 Skill；不需要 MCP 服务或额外的运行依赖。请使用支持下述命令的客户端版本。

### Codex（桌面端 / CLI）

该单文件插件布局已在 Codex CLI **0.162.1** 验证。旧版（例如 0.142.5）会忽略指向根目录的技能路径，即使显示安装成功也无法加载技能；此时升级客户端，或使用下方的独立 Skill 安装方式。桌面端也需要其内置 Codex 支持该布局。

在支持的 Codex 桌面端的插件页面选择 **Add marketplace（添加市场）**，输入 `https://github.com/op7418/Humanizer-zh`，然后安装并启用 `humanizer-zh`。市场标识为 `humanizer-zh-marketplace`。

也可在终端执行：

```bash
codex plugin marketplace add op7418/Humanizer-zh
codex plugin add humanizer-zh@humanizer-zh-marketplace
```

CLI 和桌面端需要使用同一用户及 Codex 配置目录。在 WSL 或另一台机器上注册的市场不会自动出现在 Windows 桌面端。

安装后新建会话，输入：

```text
请用 $humanizer-zh:humanizer-zh 润色下面的中文文本：
[原文]
```

可用 `codex plugin list --marketplace humanizer-zh-marketplace --json` 检查插件是否已安装、启用。桌面端未发现技能时，重启应用后新建会话。

旧版 Codex 或不使用插件时，可在会话中让内置安装器安装独立 Skill：

```text
使用 $skill-installer 安装 https://github.com/op7418/Humanizer-zh 根目录的 humanizer-zh 技能。
```

独立 Skill 安装后重启 Codex，使用 `$humanizer-zh` 调用。

### Claude Code

在终端执行：

```bash
claude plugin marketplace add op7418/Humanizer-zh
claude plugin install humanizer-zh@humanizer-zh-marketplace
```

也可在 Claude Code 会话中依次执行 `/plugin marketplace add op7418/Humanizer-zh` 和 `/plugin install humanizer-zh@humanizer-zh-marketplace`。

重启会话后，用插件的带命名空间命令调用：

```text
/humanizer-zh:humanizer-zh 请润色下面的中文文本：
[原文]
```

可用 `claude plugin list` 检查安装状态。作为独立 Skill 安装时，调用命令仍为 `/humanizer-zh`。

### Gemini CLI

使用原生 Skill 安装命令：

```bash
gemini skills install https://github.com/op7418/Humanizer-zh.git
```

默认安装到用户目录；仅供当前项目使用时加上 `--scope workspace`。按客户端提示确认安装，在已有会话中执行 `/skills reload`，再用 `/skills list` 检查是否出现 `humanizer-zh`。

调用时直接说明“请用 humanizer-zh 润色下面的中文文本”，然后粘贴原文。

### 通用 Skill 安装（保留已有方式）

```bash
npx skills add https://github.com/op7418/Humanizer-zh.git
```

按安装器提示选择客户端。也可下载 ZIP 或克隆仓库，将根目录的 `SKILL.md` 单独复制到对应客户端的用户 Skill 目录：

| 客户端 | 文件位置（macOS / Linux） | 文件位置（Windows） |
|---|---|---|
| Codex | `~/.agents/skills/humanizer-zh/SKILL.md` | `%USERPROFILE%\.agents\skills\humanizer-zh\SKILL.md` |
| Claude Code | `~/.claude/skills/humanizer-zh/SKILL.md` | `%USERPROFILE%\.claude\skills\humanizer-zh\SKILL.md` |
| Gemini CLI | `~/.gemini/skills/humanizer-zh/SKILL.md` | `%USERPROFILE%\.gemini\skills\humanizer-zh\SKILL.md` |

复制后重启客户端会话或重新加载技能。选择一种安装方式即可，避免同时安装插件和同名独立 Skill。

### 更新与卸载

以下命令对应上面的原生安装方式：

| 客户端 | 更新 | 卸载 |
|---|---|---|
| Codex | `codex plugin marketplace upgrade humanizer-zh-marketplace`，再执行 `codex plugin add humanizer-zh@humanizer-zh-marketplace` | `codex plugin remove humanizer-zh@humanizer-zh-marketplace` |
| Claude Code | `claude plugin marketplace update humanizer-zh-marketplace`，再执行 `claude plugin update humanizer-zh@humanizer-zh-marketplace` | `claude plugin uninstall humanizer-zh@humanizer-zh-marketplace` |
| Gemini CLI | 再次执行 `gemini skills install https://github.com/op7418/Humanizer-zh.git`，按提示确认覆盖 | `gemini skills uninstall humanizer-zh` |

更新后重启会话或重新加载技能。Gemini 使用 `--scope workspace` 安装时，更新和卸载也使用相同作用域；手动安装则替换或删除对应的 `humanizer-zh` 目录。

安装机制参考：[Codex 插件与 marketplace](https://developers.openai.com/plugins/build/plugins)、[Claude Code 插件发布](https://code.claude.com/docs/en/plugins/publish)、[Gemini CLI Skills](https://geminicli.com/docs/cli/skills/)。

### 插件结构

```text
Humanizer-zh/
├── SKILL.md                        # 唯一的技能定义
├── .agents/plugins/marketplace.json # Codex 市场
├── .codex-plugin/plugin.json        # skills: "./."，指向根目录
└── .claude-plugin/
    ├── marketplace.json            # Claude Code 市场
    └── plugin.json                 # skills: "./"，指向根目录
```

Gemini CLI 直接读取根目录技能，无需扩展清单。修改技能时只编辑 `SKILL.md`；发布插件更新时同步修改两份插件清单和 Claude Code 市场条目中的 `version`。

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

保留 31 个检查点，沿用 PR #39 的 A–F 分类，便于对照。这是编辑问题清单，不是作者身份检测标准。

| 分类 | 检查点 |
|---|---|
| A：铺垫代替陈述（1–5） | 假对比、戏剧性碎片、伪深度、起跑式铺垫、无对象的辩护 |
| B：公式化节奏（6–11） | 强凑三段式、重复开头、万能破折号、限定堆叠、生造复合词、被动与缺主语 |
| C：拔高与借权威（12–18） | 空泛高频词、意义拔高、模糊关联、句尾拔高、宣传语、权威背书、复杂系动词 |
| D：公式化排版（19–21） | 无效粗体、装饰性标题、引号和标点 |
| E：聊天与草稿残留（22–25） | 客服腔、重复免责与猜测填充、首句复读标题、编辑过程残留 |
| F：中文补充检查（26–31） | 长定语、“进行＋动词”、被字句堆叠、四字词排比、万能背景、套话收尾 |

每条包括修改条件、前后示例和保留边界，详见 [SKILL.md](SKILL.md)。

## 验证

[测试说明](tests/README.md)包含 18 个短文本案例、一个 Markdown 文件样例和结构检查脚本。本次更新还做了旧版与修订版的长文对照，检查数字、条件、归因、作者态度和文件结构。单次、有限样例不能代表所有模型和文体；不能用字数下降或模型自评分证明效果。

## 来源与许可

- [blader/humanizer v3.0.0](https://github.com/blader/humanizer/blob/v3.0.0/SKILL.md)：原项目及 A–E 分类、声音校准、文件模式的来源。
- [Humanizer-zh PR #39](https://github.com/op7418/Humanizer-zh/pull/39)：本次修订的结构基础与中文检查点来源。
- [Humanizer-zh PR #34](https://github.com/op7418/Humanizer-zh/pull/34)：示例保真修复的对照参考。本修订没有直接合并该分支。
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)：简洁表达与编辑检查的参考来源。
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)：原项目的观察来源。

遵循仓库中的 [MIT License](LICENSE)。
