# CTS｜Claude 第一次執行任務（免費版）

本文件已存入 GitHub，請在 Claude 建立專案 `CTS｜AI Trading Review` 後，將同一 GitHub Repo 的 `integration/cts-collab-v1` 分支加入專案知識，至少選取本檔、`collab/START_HERE.md`、`collab/CLAUDE_REVIEW_PROMPT.md`、`collab/STATUS.json`、`tools/validate_public_research.py` 和 `latest.json`。

## 直接貼入 Claude 的第一輪任務

請擔任 CTS 的獨立程式與風控審查者。先讀本專案 GitHub 中的 START_HERE.md、CLAUDE_REVIEW_PROMPT.md、STATUS.json、validate_public_research.py、latest.json，按正式審查規範執行**第一次公開研究資料與 CI 安全審查**。

本輪只使用 GitHub 已選取且實際可讀的公開資料；不要猜測或宣稱已讀取我的私人 Notion CTS V5.2、玉山券商庫存、交易憑證或 Windows 正式 ZIP。請檢查：
1. 研究資料的 2,168 股票名錄與 68 成功評估是什麼風險？研究排名可否觸發買單？
2. `validate_public_research.py` 的欄位、時區、股票代碼、去識別化與失敗關閉檢查是否有 P0/P1 錯誤？
3. GitHub Actions 設定是否具備可執行性，是否會洩漏私密內容或意外下單？
4. 建議以最小必要修改補強哪些可重現的資料品質／回歸測試？
5. 提供文件名稱／檢查依據／錯誤嚴重度／修正建議／可以重現的測試步驟。

輸出 `Verdict`、`P0/P1`、`P2/P3`、`Regression tests`、`Missing evidence`、`Recommendations`，並明確標註：`LIVE_TRADING=DISABLED`、`BROKER_ACCESS=UNVERIFIED`。

不要產生真實交易指令、不要請我傳送 API Key 或券商帳號。請用繁體中文。

## Claude 完成後
將 Claude 審查結論提供給 GPT，由 GPT 與 GitHub 的原始資料比較後處理，不要直接將 Claude 的意見升格為正式 CTS V5.2 策略或交易授權。

## 無法授權時的備援
如果 Claude 專案無法選取此分支，直接打開本檔、CLAUDE_REVIEW_PROMPT.md 和 GitHub latest.json，複製內容貼到 Claude Free。此方法可完成第一輪公開資料審查，但**不等於帳戶間的自動同步**。
