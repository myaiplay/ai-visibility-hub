#!/usr/bin/env python3
"""Static site generator for the AI Visibility Hub.

Reads markdown from content/, renders docs/ (GitHub Pages source).
No external services required. Deps: markdown, pyyaml.
"""
import json
import re
import sys
from pathlib import Path

try:
    import markdown
    import yaml
except ImportError:
    sys.exit("Missing deps. Run: pip install -r requirements.txt")

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
DOCS = ROOT / "docs"
TEMPLATE = (ROOT / "templates" / "page.html").read_text()
CSS = (ROOT / "assets" / "style.css").read_text()

BASE_URL = "https://myaiplay.github.io/ai-visibility-hub"
SITE_NAME = "AI Visibility Index"
MAIN_SITE = "https://aicantfindme.com"

ORG_JSONLD = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": SITE_NAME,
    "url": BASE_URL,
    "sameAs": [MAIN_SITE],
    "description": "Independent data hub measuring how AI search engines recommend local businesses.",
}


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)), m.group(2)


def extract_faqs(html):
    """Pull <h2>/<h3> Q&A pairs from rendered HTML for FAQPage schema."""
    pairs = re.findall(
        r"<h[23][^>]*>(.*?)</h[23]>\s*<p>(.*?)</p>", html, re.S
    )
    faqs = []
    for q, a in pairs:
        q_clean = re.sub(r"<[^>]+>", "", q).strip()
        a_clean = re.sub(r"<[^>]+>", "", a).strip()
        if q_clean.endswith("?") and a_clean:
            faqs.append({
                "@type": "Question",
                "name": q_clean,
                "acceptedAnswer": {"@type": "Answer", "text": a_clean},
            })
    return faqs


def render(src: Path, out_rel: str):
    meta, body = parse_frontmatter(src.read_text())
    html_body = markdown.markdown(body, extensions=["fenced_code", "tables", "toc"])

    title = meta.get("title", SITE_NAME)
    desc = meta.get("description", "")
    url = f"{BASE_URL}/{out_rel}".rstrip("/") or BASE_URL
    utm = meta.get("utm", "article")

    cta_html = ""
    if meta.get("type") == "article":
        cta_html = f'''
<div class="cta">
  <h3>See who AI names instead of you</h3>
  <p>One report across ChatGPT, Google AI, and Perplexity. Top 3 blockers with evidence. A 12-step fix plan. No subscription.</p>
  <a class="btn" href="{MAIN_SITE}?utm_source=hub&amp;utm_medium={utm}&amp;utm_campaign=hub_cta">Get My Report — $97</a>
</div>'''

    jsonld = [ORG_JSONLD]
    if meta.get("type") == "article":
        jsonld.append({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": desc,
            "datePublished": str(meta.get("date", "")),
            "author": {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL},
            "publisher": {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL},
            "mainEntityOfPage": url,
        })
        faqs = extract_faqs(html_body)
        if faqs:
            jsonld.append({
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": faqs,
            })

    jsonld_html = "\n".join(
        f'<script type="application/ld+json">{json.dumps(b)}</script>' for b in jsonld
    )

    page = (
        TEMPLATE.replace("{{title}}", title)
        .replace("{{description}}", desc)
        .replace("{{canonical}}", url)
        .replace("{{base}}", BASE_URL)
        .replace("{{css}}", CSS)
        .replace("{{content}}", html_body + cta_html)
        .replace("{{jsonld}}", jsonld_html)
        .replace("{{year}}", "2026")
    )

    out_path = DOCS / out_rel / "index.html" if out_rel else DOCS / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page)
    return {"url": url, "title": title, "date": str(meta.get("date", ""))}


def main():
    if DOCS.exists():
        for f in DOCS.rglob("*"):
            if f.is_file():
                f.unlink()
    DOCS.mkdir(exist_ok=True)

    pages = []
    pages.append(render(CONTENT / "index.md", ""))
    for md in sorted(CONTENT.rglob("*.md")):
        if md.name == "index.md":
            continue
        rel = md.relative_to(CONTENT).with_suffix("")
        pages.append(render(md, str(rel)))

    # sitemap
    urls = "\n".join(
        f"  <url><loc>{p['url']}</loc><lastmod>{p['date'] or '2026-08-16'}</lastmod></url>"
        for p in pages
    )
    (DOCS / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'
    )

    # robots.txt - explicitly welcome AI crawlers (we practice what we preach)
    (DOCS / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        "User-agent: GPTBot\nAllow: /\n\n"
        "User-agent: OAI-SearchBot\nAllow: /\n\n"
        "User-agent: ChatGPT-User\nAllow: /\n\n"
        "User-agent: ClaudeBot\nAllow: /\n\n"
        "User-agent: PerplexityBot\nAllow: /\n\n"
        "User-agent: Google-Extended\nAllow: /\n\n"
        f"Sitemap: {BASE_URL}/sitemap.xml\n"
    )

    # llms.txt
    articles = [p for p in pages if "/articles/" in p["url"]]
    llms = [f"# {SITE_NAME}", "",
            "> Independent data hub measuring how AI search engines recommend local businesses. Free research by the makers of aicantfindme.com.", "",
            f"- Site: {BASE_URL}",
            f"- Main service: {MAIN_SITE}",
            "", "## Articles"]
    llms += [f"- [{a['title']}]({a['url']})" for a in articles]
    (DOCS / "llms.txt").write_text("\n".join(llms) + "\n")

    print(f"Built {len(pages)} pages -> docs/")


if __name__ == "__main__":
    main()
