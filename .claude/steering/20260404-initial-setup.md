# 初期セットアップの意思決定記録

日付: 2026-04-04

---

## スケジューラー: launchd → Claudeリモートトリガー

**検討したオプション:** launchd（Mac）、Claude CCR
**決定:** Claude CCR（`trig_01VwQ44uL4Ug3XFazzDThkpp`）

**背景:**
- launchdはplistファイルの記述が必要でセットアップが煩雑
- Macの電源が落ちていても動くことを優先
- launchd用ファイルは削除済み

---

## 公開先: GitHub Pages

**検討したオプション:** GitHub Pages、Cloudflare Tunnel + ローカルサーバー、LINE通知のみ
**決定:** GitHub Pages（GitHub Actions経由、`gh-pages`ブランチなし）

**背景:**
- Cloudflare TunnelはMacの常時起動が前提で運用負荷が高い
- GitHub Pagesはリポジトリがpublicならコストゼロ
- エンジニアとしてのポートフォリオ・発信目的でpublicは好都合
- `actions/deploy-pages` を使うことでブランチ管理不要

---

## Claudeへのgit push権限

**懸念:** Claudeにpush権限を渡すセキュリティリスク
**決定:** 許可する

**背景:**
- リポジトリの中身はMarkdownのみ、機密情報なし
- 最悪のケースは「変な要約が公開される」程度
- プロンプトインジェクション対策としてAI自動生成の免責フッターを追加
- `.env`等の機密ファイルは存在しない

---

## ニュース収集ロジックの置き場所

**検討したオプション:** ブラウザのClaudeに直書き、リポジトリのdaily-news.md
**決定:** `.claude/commands/daily-news.md` で管理

**背景:**
- gitで変更履歴が残る
- 将来Pythonスクリプトへの移行など拡張しやすい
- エンジニアとしての開発体験・手応えを重視（ブラウザ完結では面白みがない）

---

## ドキュメント構成

**決定:** `README.md`（公開向け） / `CLAUDE.md`（開発ルール） / `.claude/steering/`（意思決定記録）

**背景:**
- 意思決定の背景は将来の自分やClaudeが参照できるよう別ファイルに分離
- READMEは外部公開向けに最小限に保つ
