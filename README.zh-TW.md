# Humanizer-zh：中文文字潤飾 Skill

[![skills.sh](https://skills.sh/b/op7418/Humanizer-zh)](https://skills.sh/op7418/Humanizer-zh)

編修既有文章、評論和文件裡的空話、重複與模板化表達，保留事實、確定程度和作者的聲音。支援簡體中文與台灣繁體中文。輸入是一段文字或一個檔案，預設輸出最終改寫稿；沒有問題的句子可以不改。

這是一份讓 Agent 讀取後執行的編修指引，不是獨立的偵測程式。它不能證明文章由誰撰寫，也不保證通過任何 AI 偵測器。

> 简体中文说明请见 [README.md](README.md)。

## 台灣繁體中文

輸入是繁體中文（或指定台灣讀者、台灣用語、zh-TW）時，Skill 會讀取 [references/zh-tw.md](references/zh-tw.md)，另外檢查：

- **對岸用語**：軟件→軟體、視頻→影片、默認→預設、數據庫→資料庫等。「支持」「質量」「項目」這類詞標示「看語境」，只在指該義項時才換。
- **簡轉繁錯字**：「髮布」「后台」「爲」「着」「説」等機器轉換或混用字形的錯誤。
- **兩岸同詞異義**：台灣的「土豆」是花生，「窩心」是溫暖貼心，按作者所在地區理解，不「修正」。
- **標點**：以「」『』為引號，中文正文用全形標點。
- **翻譯腔與公關腔**：「作為一個……」「對於……來說」「進行一個……」「攜手共創雙贏」等。

以下內容不做用語替換：專有名詞、官方譯名、法規與機關名稱、引語和程式碼。港澳繁體保留原本的地區用語（「電郵」「打印」），也不擅自做簡繁轉換。公文的「業已」「惟」與挪抬空格照原文保留。

## 安裝

本 Skill 採用 [Agent Skills](https://agentskills.io) 開放格式，由 `SKILL.md` 和 `references/` 參考檔組成。安裝後的資料夾名稱必須是小寫的 `humanizer-zh`，與 `SKILL.md` 中的 `name` 一致。`references/zh-tw.md` 要跟著 Skill 一起安裝；只下載單一 `SKILL.md` 會缺少台灣繁體規則。

### 方法一：npx 一鍵安裝（建議）

本 Skill 已收錄於 [skills.sh](https://skills.sh/op7418/Humanizer-zh)，可用簡寫安裝：

```bash
npx skills add op7418/Humanizer-zh
```

也可以指定安裝範圍和 Agent：

```bash
# 互動式選擇要安裝的 Agent
npx skills add https://github.com/op7418/Humanizer-zh -g

# 或直接指定 Agent
npx skills add https://github.com/op7418/Humanizer-zh -g -a claude-code codex hermes-agent pi openclaw
```

`-g` 會安裝到使用者目錄，所有專案都能用；拿掉 `-g` 則只安裝到目前的專案。[skills CLI](https://github.com/vercel-labs/skills) 把檔案放在 `~/.agents/skills/humanizer-zh`，再替需要的 Agent 建立符號連結。更新時執行 `npx skills update`。

| Agent | `-a` 參數 | 呼叫方式 | `-g` 安裝位置 |
|---|---|---|---|
| Claude Code | `claude-code` | `/humanizer-zh` | `~/.claude/skills/`（連結） |
| OpenAI Codex | `codex` | `$humanizer-zh` 或 `/skills` | `~/.agents/skills/` |
| Hermes Agent | `hermes-agent` | `/humanizer-zh` | `~/.hermes/skills/`（連結） |
| Pi | `pi` | `/skill:humanizer-zh` | `~/.pi/agent/skills/`（連結） |
| OpenClaw | `openclaw` | `/skill humanizer-zh` | `~/.openclaw/skills/`（連結） |
| Gemini CLI | `gemini-cli` | 依描述自動啟用 | `~/.agents/skills/` |
| OpenCode | `opencode` | 依描述自動啟用 | `~/.agents/skills/` |
| GitHub Copilot | `github-copilot` | `/humanizer-zh` | `~/.agents/skills/` |
| Cursor | `cursor` | `/humanizer-zh` | `~/.agents/skills/` |

安裝位置是 2026-09-24 用 skills CLI 實測的結果。CLI 改版後可能不同，請以安裝完成時的提示為準。所有 Agent 也都能依描述自動選用本 Skill。

### 方法二：用 Git 複製到各 Agent

複製時指定資料夾名稱 `humanizer-zh`。之後在該資料夾執行 `git pull` 就能更新。

**Claude Code**

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.claude/skills/humanizer-zh
```

在對話中輸入 `/humanizer-zh`，或直接說「用 humanizer-zh 潤飾」。

**OpenAI Codex**

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.agents/skills/humanizer-zh
```

用 `$humanizer-zh` 明確呼叫，或輸入 `/skills` 選擇；Codex 也會依描述自動選用。舊位置 `~/.codex/skills/` 仍會讀取，但官方已不建議使用。Skill 沒出現時請重新啟動 Codex。

**Hermes Agent**

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.hermes/skills/humanizer-zh
```

在對話中輸入 `/humanizer-zh`；執行中的工作階段可用 `/reload-skills` 重新掃描。放在專案內 `.hermes/skills/` 的 Skill，要先執行 `hermes skills trust` 才會載入。請不要只用 `SKILL.md` 的原始網址安裝，那樣不會下載 `references/`。

**Pi**

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.pi/agent/skills/humanizer-zh
```

用 `/skill:humanizer-zh` 呼叫；新增或修改 Skill 後執行 `/reload`。Pi 也會讀取 `~/.agents/skills/`。

**OpenClaw**

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.openclaw/skills/humanizer-zh
```

用 `/skill humanizer-zh` 呼叫。斜線指令會把連字號換成底線，所以也可以輸入 `/humanizer_zh`。Skill 在工作階段開始時載入，新裝的 Skill 要在新的工作階段才會生效。

**Gemini CLI、OpenCode、GitHub Copilot、Cursor**

這些 Agent 都會讀取跨工具目錄 `~/.agents/skills/`：

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.agents/skills/humanizer-zh
```

### 多個 Agent 共用一份

`~/.agents/skills/` 可供 Codex、Pi、OpenClaw、Gemini CLI、OpenCode、GitHub Copilot 和 Cursor 讀取。Claude Code 與 Hermes Agent 預設不讀這個目錄，可以用符號連結共用同一份檔案：

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.agents/skills/humanizer-zh
mkdir -p ~/.claude/skills ~/.hermes/skills
ln -s ~/.agents/skills/humanizer-zh ~/.claude/skills/humanizer-zh
ln -s ~/.agents/skills/humanizer-zh ~/.hermes/skills/humanizer-zh
```

同一個 Skill 不要在同一個 Agent 會讀取的多個目錄各放一份，否則可能重複載入或互相覆蓋。

### Windows

把路徑中的 `~` 換成 `%USERPROFILE%`，例如 `%USERPROFILE%\.claude\skills\humanizer-zh`。建立連結可在系統管理員命令提示字元中使用 `mklink /D`，或直接複製整個資料夾。

### 不支援 Skill 的 Agent

在專案的 `AGENTS.md`（或該工具的規則檔）中加入：

```markdown
編修或潤飾中文文字時，先讀取 <安裝路徑>/humanizer-zh/SKILL.md，依其中的規則執行。
```

## 使用

貼上文字：

```text
請用 humanizer-zh 潤飾這篇文章，改成台灣用語，保留原本的語氣：
[原文]
```

編修檔案：

```text
請用 humanizer-zh 潤飾 article.md 的正文。
```

只要審閱時，請說明「給建議，不修改檔案」。有作者樣本時可以一起提供，Skill 會參考表達習慣，但不會把樣本中的經歷、數字或觀點搬進原文。

## 改寫範例

以下都是教學用的輸入，沒有未列出的補充資料。

**產品說明，對岸用語與空泛讚美：**

> 原文：這款軟件在默認設置下支持視頻導出，質量非常高，充分彰顯了團隊對用戶體驗的極致追求。
>
> 改寫：這款軟體在預設設定下支援匯出影片，品質很高。

刪除沒有資訊的讚美，「品質很高」保留為評價，不補畫質參數。

**簡轉繁錯字：**

> 原文：新版本已髮布，修復了后台的若干問題，其中也包含着新的設置選項，預計下週一上線。
>
> 改寫：新版本已發布，修復了後台的若干問題，也包含新的設定選項，預計下週一上線。

「預計」仍是預計，不改成已上線。

**翻譯腔：**

> 原文：作為一個開發者，對於這個問題來說，我們需要進行一個全面的評估，然後再決定是否在下個版本中進行修復。
>
> 改寫：身為開發者，我們需要先全面評估這個問題，再決定是否在下個版本修復。

保留「是否」，不把還沒決定的事改成已決定修復。

**已經清楚的文字：**

> 原文：這家店的土豆麵筋很窩心，老闆說湯頭每天早上現熬，不過我只吃過一次，不確定是不是每次都一樣。
>
> 改寫：（不修改）

「土豆」「窩心」按台灣詞義理解，「老闆說」的歸因和作者的不確定都要保留。不要求每次呼叫都產生修改。

## 編修原則

限制的優先順序是：保留資訊和確定程度，遵守使用者指定的範圍與文體，貼近作者的聲音，最後才處理個別表達問題。命中檢查項目不能凌駕這些要求。

- 不編造功能、數字、來源、人物身分或第一人稱經歷。
- 保留否定、條件、歸因、範圍、時間和完成狀態；「可能」不變成「確定」，「計畫」不變成「已經」。
- 三項列舉、四字格、被動句、破折號和連接詞依作用判斷，不機械刪除。
- 隨筆可以保留個性，學術和商務文字保留正式程度；不把所有文章改成同一種口語。
- 編修檔案時，預設保留程式碼、指令、路徑、連結目標、YAML、資料、標題和錨點。
- 預設只交付最終稿，不附中間草稿、命中清單或自評分數。

39 項檢查的條件列在 [SKILL.md](SKILL.md)，改寫前後與應保留的範例在 [references/patterns.md](references/patterns.md)。第 1–31 項沿用上游的 A–F 分類；第 32–39 項（G 組）來自 [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) 的語料實測（629 篇、約 283 萬字），例如段首零回指評論（4.4 倍）、空轉句引出清單的冒號（9.4 倍）、拿理想化職業人格當喻體（7.3 倍）。

同一份實測也顯示，比喻、正文問句、句內排比、正文裡的「首先……其次」和句長參差，人類用得不比 AI 少，有些還更多。`SKILL.md` 把這些列為「實測不構成修改理由」，免得越改越不像人寫的。

## 驗證

[測試說明](tests/README.md)包含 32 個短文案例（其中 7 個是繁體、7 個針對 G 組）、一個 Markdown 檔案範例、結構檢查腳本，以及台灣繁體用語檢查腳本：

```bash
python3 tests/check_zh_tw.py 改寫後的檔案.md
```

腳本讀取 `references/zh-tw.md` 的詞表，列出對岸用語、簡轉繁錯字、混入的簡體字，以及「台／臺」「計畫／計劃」等並存寫法的混用，會跳過程式碼與連結。每個 PR 都會由 GitHub Actions 執行單元測試與 Agent Skills 格式驗證。它只做字串比對，標示「看語境」的結果要由人判斷，不能取代人工核對語意。單次、有限的樣本也不能代表所有模型和文體。

## 來源與授權

- [blader/humanizer v3.0.0](https://github.com/blader/humanizer/blob/v3.0.0/SKILL.md)：原始專案，以及 A–E 分類、聲音校準、檔案模式的來源。
- [Humanizer-zh PR #39](https://github.com/op7418/Humanizer-zh/pull/39)：本次修訂的結構基礎與中文檢查項目來源。
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)：簡潔表達與編修檢查的參考來源。
- [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)（MIT）：G 組檢查、「實測不構成修改理由」與倍數資料的來源，授權見 [licenses/](licenses/lieflat-less-ai-tone.txt)。
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)：原始專案的觀察來源。

採用本儲存庫的 [MIT License](LICENSE)。
