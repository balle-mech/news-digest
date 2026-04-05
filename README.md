# 📰 ニュースダイジェスト

AIが毎朝自動収集・要約するニュースダイジェスト。セキュリティ・IT・政治・経済をカバー。

## パイプライン全体像

```
毎朝6:00 JST
  │
  ▼ Claudeスケジュールタスク（Anthropicクラウド）
    https://claude.ai/code/scheduled
  │  GitHubリポジトリをclone
  │  .claude/commands/daily-news.md の手順を実行
  │  WebSearch / WebFetch でニュース収集
  │  news/YYYY-MM-DD.md を生成・push
  │
  ▼ GitHub Actions（.github/workflows/deploy.yml）
    news/ への push をトリガーに自動起動
  │  scripts/build_site.py で Markdown → HTML 変換
  │
  ▼ GitHub Pages デプロイ
    https://balle-mech.github.io/news-digest/
```

## ディレクトリ構成

```
news-digest/
├── .claude/
│   ├── commands/
│   │   └── daily-news.md       # ニュース収集プロンプト
│   └── settings.local.json     # ツール権限設定
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions（Pages自動デプロイ）
├── scripts/
│   └── build_site.py           # Markdown → HTML変換スクリプト
├── news/                       # 生成されたMarkdown（YYYY-MM-DD.md）
└── README.md
```

---

## セットアップ手順

### 1. GitHubリポジトリと紐づける

GitHubで `news-digest` リポジトリ（public）を作成後：

```bash
cd ~/news-digest
git remote add origin https://github.com/balle-mech/news-digest.git
git add .
git commit -m "initial commit"
git push -u origin main
```

### 2. GitHub Pagesを有効化

GitHub リポジトリの **Settings → Pages** で：

- Source: `GitHub Actions` を選択

### 3. Claudeスケジュールタスクの確認

毎朝6:00 JSTに自動実行されるトリガーが登録済みです。

- 管理画面: https://claude.ai/code/scheduled
- トリガーID: `trig_01VwQ44uL4Ug3XFazzDThkpp`

---

## 手動実行

```bash
# ローカルで即時実行
claude -p "$(cat .claude/commands/daily-news.md)" \
  --allowedTools WebSearch,WebFetch,Write,Edit,Read
```

---

## 注意事項

> ⚠️ 本サイトはAI（Claude）による自動要約です。内容の正確性・完全性を保証するものではありません。各ニュースの詳細は元のソースをご確認ください。
