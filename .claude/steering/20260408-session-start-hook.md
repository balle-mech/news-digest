# SessionStart フックでリモート同期を自動化

## 背景

CCR（Claude Code Remote）は毎セッション、リモートの設定だけが入った空のローカルリポジトリを用意する。
`git fetch` と `git checkout` が行われていないため、`.claude/commands/daily-news.md` などのファイルが存在しない状態でセッションが始まることがあった。

## 決定

`.claude/settings.json` に `SessionStart` フックを追加し、セッション開始時に自動で `git fetch origin && checkout/merge origin/main` を実行する。

## フック動作

- `main` ブランチが既に存在する場合 → `git checkout main && git merge --ff-only origin/main`
- `main` ブランチが存在しない場合 → `git checkout -b main --track origin/main`
- エラーは `2>/dev/null || true` で握り潰し、フック失敗でセッションがブロックされないようにする

## 代替案

- CLAUDE.md にセットアップ手順を記載する（→ 手動対応が必要なため不採用）
- `git clone` をやり直す（→ CCR の仕組み上不可）
