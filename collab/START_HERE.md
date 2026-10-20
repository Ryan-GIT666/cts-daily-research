# CTS｜GPT × Claude × Notion × GitHub 協作入口（2026-10-20）

> 此分支是**公開、安全、唯讀研究資料的協作示範**；不代表程式交易已啟用。正式 CTS 策略、個人風控數值與庫存資訊只保留私人 Notion 與 Windows 本機，不移到公開 GitHub。

## 資料權威（先讀）
1. CTS V5.2 唯一策略權威（Notion）：https://app.notion.com/p/3c943d9c613e8127aa28f3b0c9818bc1
2. CTS 最新盤中分析（Notion）：https://app.notion.com/p/3ca43d9c613e81428724ce3cdd7ae6e0
3. 既有公開研究站（gh-pages）：https://ryan-git666.github.io/cts-daily-research/
4. 公開機讀研究：gh-pages/latest.json（research_only=true）
5. 此分支協作檔：collab/STATUS.json、CLAUDE_REVIEW_PROMPT.md、REVIEW_TEMPLATE.md。
6. Windows 正式 Decision Desk 為 V2.1.3 STABLE；V2.2 Candidate 不得未經驗收升級。

## 分工
- **GitHub Actions**：在此分支 push 更新時驗證公開 latest.json 格式、時間戳、覆蓋率與 research_only；輸出 JSON 檢查報告。這是**資料合約測試，不是交易回測**。
- **GPT**：閱讀 Notion 與 GitHub、審核風控／程式設計、建立修正分支、執行可重現測試與整理交接；不自動獲得券商權限。
- **Claude Free**：使用 CLAUDE_REVIEW_PROMPT.md，手動讀取公開研究資料與去識別化變更，返回結構化審查；**免費網頁不能由 GitHub Actions 無憑證呼叫**。
- **Windows 本機執行器**：未來才串接官方玉山證券 API；金鑰、委託、庫存、成交、費率及可用資金不得離開本機。
- **Notion**：記錄 CTS V5.2 交易規則、風控授權、開發狀態與驗收 Gate。公開 GitHub 不存投資帳務、真實庫存或個人資訊。

## 現行 Gate
1. 研究分數只可用於候補，不等於 Setup / Trigger / Invalidation / 淨 R/R 或可買進訊號。
2. 有效資料必須同日、正確時區／交易日、涵蓋所需股票、來源可靠且有時間戳。
3. 先歷史回測（避免未來函數及樣本內過擬合）→ 樣本外 → 至少20交易日 Shadow Test → 玉山模擬環境測試委託狀態 → 小額人工核准實盤 → 經明確授權之限額策略。
4. 買進需新鮮行情、券商庫存及未成交委託對帳、額度與單筆風險核對、有效交易時段、價格帶與流動性驗證；任何缺口 fail-closed。
5. 真實下單須以本機獨立固定規則的風控引擎執行，GPT/Claude 無送單權；不可用 GitHub 公開工作流程直接保存交易憑證。
6. 賣單發送不等於成交；要有原生回報、部分成交、撤單、重連、冪等性與停機處理。
7. 此 Repo 的交易狀態固定為 **DISABLED**，除非日後由使用者在自己的 Windows 上獨立設置權限並通過驗收。


## 2026-10-20｜新的周期研究與正式API唯讀Gate
- CTS V5.2 周期波動延展／5–15交易日複核／Shadow與實單安全門檻：[CTS_CYCLE_WAVE_AND_API_GATES_20261020.md](./CTS_CYCLE_WAVE_AND_API_GATES_20261020.md)。
- Claude Free 可直接人工送審的獨立審查任務：[CLAUDE_CYCLE_REVIEW_20261020.md](./CLAUDE_CYCLE_REVIEW_20261020.md)。
- Windows 本機已實測玉山模擬委託被接受、正式API登入和餘額/庫存唯讀。**尚未完成正式委託/成交對帳、撤單/部分成交/斷線防重送、20交易日Shadow；實盤AUTO_LIVE維持DISABLED。**
- GitHub協作STATUS.json為機讀進度；公開研究只能作候選，真實券商持股、資金及下單資料完全不進GitHub/Claude。

## 下一輪接任
先查 git 目前 branch/commit → Notion CTS V5.2 → collab/STATUS.json → GitHub Actions 最近結果 → 如需程式修正取得 Windows 正式完整 ZIP 的原始 bytes 並核對 SHA → 修改非正式 candidate → 回歸 → 審查 → 交付。不要以此協作分支覆蓋 gh-pages 研究網站。
