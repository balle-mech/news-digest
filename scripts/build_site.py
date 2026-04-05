#!/usr/bin/env python3
"""ニュースダイジェスト 静的サイトビルダー"""
import glob
from pathlib import Path
import markdown

SITE = Path("_site")
SITE_NEWS = SITE / "news"
SITE.mkdir(exist_ok=True)
SITE_NEWS.mkdir(exist_ok=True)

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 1.2rem;
  color: #1a1a1a;
  line-height: 1.7;
}
h1 { font-size: 1.4rem; margin-bottom: 1.2rem; }
h2 { font-size: 1.15rem; margin: 2rem 0 0.6rem; border-bottom: 1px solid #eee; padding-bottom: 0.3rem; }
h3 { font-size: 1rem; margin: 1.2rem 0 0.3rem; }
p { margin-bottom: 0.8rem; }
a { color: #0066cc; text-decoration: none; }
a:hover { text-decoration: underline; }
blockquote {
  border-left: 3px solid #ccc;
  padding-left: 1rem;
  color: #555;
  margin: 1rem 0;
}
hr { border: none; border-top: 1px solid #eee; margin: 1.2rem 0; }
strong { font-weight: 600; }
.nav { margin-bottom: 1.5rem; font-size: 0.9rem; }
.date-list { list-style: none; }
.date-list li {
  padding: 0.6rem 0;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.date-list li a { font-size: 1rem; }
.badge {
  font-size: 0.75rem;
  background: #f0f0f0;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  color: #666;
}
.footer {
  margin-top: 3rem;
  font-size: 0.8rem;
  color: #999;
  border-top: 1px solid #eee;
  padding-top: 1rem;
}
@media (prefers-color-scheme: dark) {
  body { background: #111; color: #ddd; }
  h2 { border-color: #333; }
  a { color: #6ab0ff; }
  blockquote { color: #aaa; border-color: #444; }
  hr { border-color: #333; }
  .date-list li { border-color: #2a2a2a; }
  .badge { background: #2a2a2a; color: #aaa; }
  .footer { color: #666; border-color: #2a2a2a; }
}
"""

LAYOUT = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>"""


def page(title, body):
    return LAYOUT.format(title=title, css=CSS, body=body)


news_files = sorted(glob.glob("news/*.md"), reverse=True)

# 個別ページ生成
for filepath in news_files:
    date = Path(filepath).stem
    text = Path(filepath).read_text(encoding="utf-8")
    html = markdown.markdown(text, extensions=["extra"])
    body = (
        '<div class="nav"><a href="../">← 一覧へ戻る</a></div>\n'
        + html
        + '\n<div class="footer">⚠️ 本ダイジェストはAI（Claude）による自動要約です。内容の正確性・完全性を保証するものではありません。</div>'
    )
    (SITE_NEWS / f"{date}.html").write_text(
        page(f"ニュースダイジェスト {date}", body), encoding="utf-8"
    )

# インデックスページ生成
items = "\n".join(
    f'<li><a href="news/{Path(f).stem}.html">{Path(f).stem}</a>'
    f'<span class="badge">#{i + 1}</span></li>'
    for i, f in enumerate(news_files)
)
body = (
    "<h1>📰 ニュースダイジェスト</h1>\n"
    f"<ul class=\"date-list\">\n{items}\n</ul>\n"
    '<div class="footer">⚠️ 本サイトはAI（Claude）による自動要約です。内容の正確性を保証するものではありません。</div>'
)
(SITE / "index.html").write_text(page("ニュースダイジェスト", body), encoding="utf-8")

print(f"Built {len(news_files)} pages → _site/")
