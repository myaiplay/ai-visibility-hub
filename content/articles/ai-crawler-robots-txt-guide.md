---
title: "robots.txt for AI Crawlers: Full Allow-List"
description: Copy-paste robots.txt configuration for GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, and Google-Extended — plus how to verify AI engines can actually reach your pages.
type: article
date: 2026-08-16
utm: article_robots
---

# robots.txt for AI crawlers: the complete allow-list guide

<p class="meta">16 August 2026 · AI Visibility Index</p>

<div class="answer">
<strong>Direct answer:</strong> To let AI search engines read and cite your site, your robots.txt must not block their crawlers. The critical ones are GPTBot and OAI-SearchBot (ChatGPT), PerplexityBot (Perplexity), ClaudeBot (Claude), Google-Extended (Google AI training), plus Bingbot — because ChatGPT's search relies heavily on Bing's index. Add explicit <code>Allow: /</code> rules for each, then verify by fetching your robots.txt in a browser.
</div>

If an AI crawler can't fetch your pages, the model learns about you from third-party sources — review sites, directories, competitors' comparisons — or from nothing. This is the single most common technical blocker we see, and it takes two minutes to check.

## The crawlers that matter

| Crawler | Belongs to | Blocks what if disallowed |
|---|---|---|
| GPTBot | OpenAI | ChatGPT training data |
| OAI-SearchBot | OpenAI | ChatGPT search citations |
| ChatGPT-User | OpenAI | Live browsing when users ask |
| PerplexityBot | Perplexity | Perplexity answers and citations |
| ClaudeBot | Anthropic | Claude's knowledge of your site |
| Google-Extended | Google | Gemini/AI training (separate from Search) |
| Bingbot | Microsoft | Bing index — feeds ChatGPT search and Copilot |

A subtlety worth knowing: `GPTBot` and `OAI-SearchBot` are different gates. Blocking GPTBot keeps you out of future training data; blocking OAI-SearchBot keeps you out of *cited answers today*. If you want AI search traffic, the second one is the one that matters most.

## Copy-paste allow-list

```
# AI search crawlers - allow
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

# Everyone else
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/

Sitemap: https://yoursite.com/sitemap.xml
```

Keep the `Disallow` lines for genuine private areas only. Never put `Disallow: /` under `User-agent: *` — it blocks everything, including the AI crawlers you just allowed above (specific rules win, but a global block under `*` combined with missing specific rules is the classic failure).

## Three common ways sites accidentally block AI

1. **A managed host's default robots.txt.** Some website builders ship a restrictive default. Check yours even if you never wrote one.
2. **A CDN/WAF bot rule.** Cloudflare and similar services can challenge bots before robots.txt is even read. If your security settings block "AI bots" as a category, robots.txt won't save you.
3. **A blanket `Disallow: /` left over from a staging migration.** Embarrassingly common.

## How to verify it worked

1. Open `https://yoursite.com/robots.txt` in a browser — read what the world sees.
2. Confirm your site is in Bing's index: search `site:yoursite.com` on Bing. No results = ChatGPT search can't find you either. (We built a [free index check](https://aicantfindme.com/services/index-check?utm_source=hub&utm_medium=article&utm_campaign=hub_cta) for exactly this.)
3. Spot-check with a live prompt: ask ChatGPT "what does [yoursite.com] do?" If it can describe your services, crawling is working.

## Frequently asked questions

### Does allowing AI crawlers hurt my Google rankings?

No. robots.txt for AI crawlers is independent of Googlebot and Google Search. Google-Extended only governs AI training usage — Google states it does not affect Search inclusion or ranking.

### Should I block AI crawlers to protect my content?

That's a legitimate choice for some publishers, but it trades away discoverability: engines can't recommend what they can't read. For a local business whose pages exist to win customers, blocking is usually self-sabotage.

### Is robots.txt the only thing AI crawlers check?

No. They also need your pages to be server-rendered or otherwise readable without heavy JavaScript, fast enough to fetch, and not behind a login. robots.txt is the gate — but it's only the gate.
