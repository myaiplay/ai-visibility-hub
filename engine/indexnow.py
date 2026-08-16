#!/usr/bin/env python3
"""Ping IndexNow (Bing/Yandex) with all hub URLs after each build.

No account or key provisioning needed — the key file is served from the
site root (static/<key>.txt). Never fails the build.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SITEMAP = ROOT / "docs" / "sitemap.xml"
HOST = "myaiplay.github.io"
KEY = "aivh7f3e9c2b4d58a1e6f0c5b7d9e2a4"
KEY_LOCATION = f"https://{HOST}/ai-visibility-hub/{KEY}.txt"


def main():
    if not SITEMAP.exists():
        print("No sitemap — run build.py first.")
        return
    urls = re.findall(r"<loc>(.*?)</loc>", SITEMAP.read_text())
    if not urls:
        print("No URLs in sitemap.")
        return

    import requests
    try:
        r = requests.post(
            "https://api.indexnow.org/indexnow",
            headers={"Content-Type": "application/json"},
            json={"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION,
                  "urlList": urls},
            timeout=30,
        )
        # 200 = accepted, 202 = key validation pending — both fine
        print(f"IndexNow ping: HTTP {r.status_code} for {len(urls)} URLs")
    except Exception as e:
        print(f"IndexNow ping failed (non-fatal): {e}")


if __name__ == "__main__":
    main()
