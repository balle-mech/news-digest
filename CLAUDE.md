# CLAUDE.md

Claude Codeがこのリポジトリで作業する際の指針。意思決定の背景は `.claude/steering/` を参照。

---

## アーキテクチャ

| 役割                   | 実装                                                        |
| ---------------------- | ----------------------------------------------------------- |
| スケジューラー         | Claude CCR（毎朝6:00 JST、`trig_01VwQ44uL4Ug3XFazzDThkpp`） |
| ニュース収集プロンプト | `.claude/commands/daily-news.md`                            |
| 静的サイト生成         | `scripts/build_site.py`                                     |
| デプロイ               | GitHub Actions → GitHub Pages（mainブランチ）               |

---

## 開発ルール

- **収集ロジックの変更** → `.claude/commands/daily-news.md` を編集
- **サイトデザインの変更** → `scripts/build_site.py` を編集
- **新しい取得元の追加** → `scripts/` にスクリプトを追加し `daily-news.md` から呼び出す
- **不要なファイルは作らない**
- **意思決定を行ったら背景を** `.claude/steering/YYYYMMDD-{task-title}.md` に記録する

---

## ドキュメント管理

### ファイル構成

| ファイル                         | 記載内容                                             |
| -------------------------------- | ---------------------------------------------------- |
| `README.md`                      | パイプライン全体像・セットアップ手順（外部公開向け） |
| `CLAUDE.md`                      | アーキテクチャ・開発ルール（結果のみ）               |
| `.claude/steering/`              | 意思決定の背景・検討経緯                             |
| `.claude/commands/daily-news.md` | ニュース収集プロンプト本体                           |

### メンテナンス負荷を抑える

- **ソースコードを読めばわかることは書かない**
  - 例: 関数の実装詳細、具体的なコード例
  - 理由: コードとドキュメントの乖離が発生する

- **他のドキュメントと重複しない**
  - 同じ情報を複数箇所に書かない
  - 必要な場合はリンクで参照する

---

## コミットメッセージ

```
feat: add news digest for YYYY-MM-DD   # ニュース自動生成
```

---

## 将来の拡張候補

- Pythonスクリプトでニュース取得（RSS, API利用など）
- LINE NotifyでGitHub PagesのURLを毎朝通知
