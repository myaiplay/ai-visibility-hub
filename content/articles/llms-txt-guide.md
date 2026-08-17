---
title: What is llms.txt? The plain-English guide (plus a free generator)
description: llms.txt is a proposed standard file that tells AI models what your site is and what matters on it. Here's what it does, what it doesn't, and how to make one.
type: article
date: 2026-08-17
utm: article_llmstxt
---

# What is llms.txt? The plain-English guide

<p class="meta">17 August 2026 · AI Visibility Index</p>

<div class="answer">
<strong>Direct answer:</strong> llms.txt is a plain-text file you place at <code>yoursite.com/llms.txt</code> that gives AI models a curated map of your site: who you are, what you do, and which pages matter most — in clean markdown, without navigation, ads, or boilerplate. Think of it as a briefing document for AI crawlers. It's an emerging convention, not a guarantee: adoption by the big AI providers is growing but not universal. It takes ten minutes to add and costs nothing.
</div>

## What it actually looks like

A llms.txt file is markdown with a simple shape:

```
# Your Business Name

> One-paragraph summary: what you do, where, for whom.

## Services
- [Emergency plumbing](https://yoursite.com/emergency): 24/7 callout in Denver
- [Drain cleaning](https://yoursite.com/drains): fixed-price, same-day

## About
- [Pricing](https://yoursite.com/pricing)
- [Reviews](https://yoursite.com/reviews)
```

That's it. A title, a summary, and short lists of your most important links with one-line descriptions.

## What it does — and what it doesn't

**What it does:** when an AI crawler or tool that respects the convention visits your site, it gets a clean, unambiguous briefing instead of guessing from your homepage's hero banner and cookie banner. For businesses whose sites are heavy on images and light on text, this is often the clearest description of the business that exists anywhere on the domain.

**What it doesn't do:** it's not a ranking switch. No major AI engine has promised that llms.txt alone gets you recommended. It works the same way good schema and clear copy work — it removes ambiguity, so the model *can* represent you correctly when it has reason to. Treat it as one layer in the stack, after crawler access and before content polish.

## llms.txt vs robots.txt vs sitemap.xml

| File | Audience | Purpose |
|---|---|---|
| robots.txt | Crawlers | Permission: what may be fetched |
| sitemap.xml | Search engines | Inventory: what exists |
| llms.txt | AI models | Briefing: what it all means |

They complement each other. robots.txt says "you may enter"; llms.txt says "here's who we are once you're in."

## How to make one in five minutes

1. Write your one-paragraph summary: business name, category, city, what you do, who for.
2. List your 5–10 most important pages with one-line descriptions.
3. Save as `llms.txt` in your site root so it serves at `/llms.txt`.
4. Verify: open `https://yoursite.com/llms.txt` in a browser and read what an AI would read.

We built a free generator that formats it for you: [llms.txt Creator](https://aicantfindme.com/services/llms-txt-creator?utm_source=hub&utm_medium=article&utm_campaign=article_llmstxt) — fill in the fields, download the file, upload it to your site root.

## Frequently asked questions

### Do ChatGPT or Perplexity officially support llms.txt?

The convention is young and support is informal but growing — several AI crawlers and retrieval tools fetch it when present. Like early sitemaps, the cost of adoption is near zero and the direction of travel is clear.

### Where exactly does the file go?

In your site's web root, so it's reachable at `https://yourdomain.com/llms.txt`. On most hosts that's the same folder as your homepage or your existing robots.txt.

### Can llms.txt hurt my SEO?

No. It's a plain-text file ignored by anything that doesn't look for it. Google doesn't penalise extra text files, and it doesn't replace any SEO fundamentals.
