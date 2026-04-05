#!/usr/bin/env python3
"""ニュースダイジェスト 静的サイトビルダー"""
import glob
import shutil
from pathlib import Path
import markdown

SITE = Path("_site")
SITE_NEWS = SITE / "news"
SITE.mkdir(exist_ok=True)
SITE_NEWS.mkdir(exist_ok=True)

# static/ 以下をそのまま _site/ にコピー
shutil.copytree("static", SITE, dirs_exist_ok=True)

LAYOUT = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{css_path}">
</head>
<body>
{body}
</body>
</html>"""


def page(title, body, depth=0):
    css_path = "../" * depth + "style.css"
    return LAYOUT.format(title=title, css_path=css_path, body=body)


news_files = sorted(glob.glob("news/*.md"), reverse=True)

# 個別ページ生成
for filepath in news_files:
    date = Path(filepath).stem
    text = Path(filepath).read_text(encoding="utf-8")
    html = markdown.markdown(text, extensions=["extra"])
    body = (
        '<div class="nav"><a href="../">← 最新へ</a> · <a href="../archive.html">📋 一覧</a></div>\n'
        + html
        + '\n<div class="footer">⚠️ 本ダイジェストはAI（Claude）による自動要約です。内容の正確性・完全性を保証するものではありません。</div>'
    )
    (SITE_NEWS / f"{date}.html").write_text(
        page(f"ニュースダイジェスト {date}", body, depth=1), encoding="utf-8"
    )

# 過去一覧ページ生成
items = "\n".join(
    f'<li><a href="news/{Path(f).stem}.html">{Path(f).stem}</a>'
    f'<span class="badge">#{i + 1}</span></li>'
    for i, f in enumerate(news_files)
)
archive_body = (
    '<div class="nav"><a href="./">← 最新へ戻る</a></div>\n'
    "<h1>📰 過去のニュース一覧</h1>\n"
    f"<ul class=\"date-list\">\n{items}\n</ul>\n"
    '<div class="footer">⚠️ 本サイトはAI（Claude）による自動要約です。内容の正確性を保証するものではありません。</div>'
)
(SITE / "archive.html").write_text(page("過去のニュース一覧", archive_body), encoding="utf-8")

# インデックスページ = 最新のニュース
if news_files:
    latest_date = Path(news_files[0]).stem
    latest_text = Path(news_files[0]).read_text(encoding="utf-8")
    latest_html = markdown.markdown(latest_text, extensions=["extra"])
    body = (
        '<div class="nav"><a href="archive.html">📋 過去のニュース一覧</a></div>\n'
        + latest_html
        + '\n<div class="footer">⚠️ 本ダイジェストはAI（Claude）による自動要約です。内容の正確性・完全性を保証するものではありません。</div>'
    )
    (SITE / "index.html").write_text(page(f"ニュースダイジェスト {latest_date}", body), encoding="utf-8")
else:
    (SITE / "index.html").write_text(page("ニュースダイジェスト", "<p>まだニュースがありません。</p>"), encoding="utf-8")

print(f"Built {len(news_files)} pages → _site/")
