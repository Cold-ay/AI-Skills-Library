# AI Skills Library

精選、可追溯的 AI skills 導覽與安全安裝工具。涵蓋網站／UI、影片、coding、token／context、研究／自動化、skill engineering。Python 3.10+；工具本身只用標準函式庫，不需付費 API。

## 快速開始

```sh
git clone https://github.com/Cold-ay/AI-Skills-Library.git
cd AI-Skills-Library
python3 skills.py list
python3 skills.py list --category video
python3 skills.py list --query context
python3 skills.py show react-best-practices
```

[瀏覽 12 個精選項目](docs/CATALOG.md) · [每週報告](reports/) · [證據及審查準則](docs/CURATION.md)

先看 `show` 的來源、固定版本、相容性、依賴與授權；閱讀所選 skill 的完整資料夾。確認後才安裝到你的工作專案：

```sh
python3 skills.py install react-best-practices --dest /path/to/your-project/.agents/skills --reviewed
python3 skills.py call react-best-practices 'Review this React project for performance issues'
```

`call` 只輸出可貼進 Codex 的 `$技能名稱 任務`，不會呼叫模型。安裝後開啟該專案的新 Codex session；在技能選單確認已載入再貼上。若要使用個人技能目錄，明確傳入 `--dest ~/.agents/skills`。現有 skill 不會被覆蓋，更新要先審查新版本並手動保留舊版。

直接讀 README 也能使用這個 library：選擇類別 → 看來源／要求 → 安裝 → 用輸出的名稱呼叫。不需一次載入全部 skills。需要完整插件、跨技能依賴或已停用的來源不開放此工具安裝，請依 `show` 所列上游文件處理。

## 推薦怎樣選

| 需求 | 起點 | 限制 |
|---|---|---|
| React 網站效能 | react-best-practices | 規則須符合專案版本 |
| UI／無障礙檢查 | web-design-guidelines | 使用時會讀取外部指南 |
| 視覺設計 | frontend-design | Codex 相容性未知，先試小任務 |
| 程式化剪片／動畫 | remotion-best-practices | 要有 Remotion／Node.js，非時間軸剪輯器 |
| Debugging | systematic-debugging | 完整流程須使用上游 Superpowers 插件 |
| 長對話整理 | context-compression | 沒有保證節省百分比 |
| Token 策略 | context-optimization | 部分技巧需要 runtime 控制 |
| 論文／引用 | zotero | Zotero Desktop 與完整插件 |
| 建立技能／插件 | plugin-creator | 官方 repo 路徑與腳本依賴 |

`openai/skills` 在本次查核時已標示 deprecated；其中 3 個項目保留為歷史／遷移參考，不是目前首選。現在的官方範例來源是 [openai/plugins](https://github.com/openai/plugins)。星數不等於安全性、技能品質或 Codex 支援。

## 每週更新

**啟用狀態：workflow 範本已完成；目前 GitHub 憑證缺少 `workflow` 寫入權限，尚未啟用排程。** 將 `docs/workflows/` 兩個檔案放入 `.github/workflows/` 並合併到 default branch 後，即可啟用。

GitHub Actions 設計為每星期一香港時間 **09:17**（UTC 01:17，排程可能延遲）執行唯讀搜尋，保存 `reports/YYYY-MM-DD.md` 與 JSON 證據，再建立 PR。也可在 Actions → Weekly skills discovery → Run workflow 手動執行。

- 正式排程需要 workflow 在 repo 的 default branch，並啟用 Actions。
- Repository Settings → Actions → General → Workflow permissions 必須允許 GitHub Actions 建立 pull requests；組織政策亦可能限制它。
- 每次只追蹤精選 repo 及三組搜尋各前 8 名；新增候選永遠先標記 Codex `unknown`。
- 比較前一份已合併日期的星數；首份顯示 baseline unavailable，不捏造增長率。
- API 錯誤或截斷樹會使 run 失敗、保留 artifact，不建立貌似完整的 PR。
- PR 只更新報告，不自動改清單、不安裝技能、不合併 PR。

本機產生同樣報告：`python3 report.py`。可選擇提供 `GH_TOKEN` 提高 GitHub API 配額；不要把 token 寫進 repo。未認證 API 配額較低，失敗詳情會記在報告。

## 驗證

```sh
python3 -m unittest discover -s tests -v
python3 skills.py validate
```

測試覆蓋分類、固定版本、重複項目、路徑穿越、符號連結、完整性失敗回滾、離線回滾、不覆蓋、安裝確認、候選去重、星數變化及 API 錯誤。CI 不需網路 API、憑證或第三方技能執行。

參考：[官方技能文件](https://learn.chatgpt.com/docs/build-skills)、[官方插件範例](https://github.com/openai/plugins)。第三方來源各自保有其授權；本 repo 儲存原創描述及來源 manifest，沒有整包轉載第三方 skills。
