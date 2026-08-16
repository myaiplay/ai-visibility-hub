---
title: Why ChatGPT doesn't recommend your business (and how to check in 5 minutes)
description: The three reasons AI search skips local businesses — crawler access, weak entity signals, and no citable answer — plus a five-minute self-check.
type: article
date: 2026-08-16
utm: article_why_skipped
---

# Why ChatGPT doesn't recommend your business (and how to check in 5 minutes)

<p class="meta">16 August 2026 · AI Visibility Index</p>

<div class="answer">
<strong>Direct answer:</strong> ChatGPT skips businesses for one of three reasons: (1) its crawlers can't read your site, (2) it can't confirm you're a specific, real business in a specific place, or (3) no page on the web gives it a short, sourced answer to quote. Check by asking ChatGPT, Google AI, and Perplexity "best [your category] in [your city]" and noting who gets named.
</div>

When a customer asks an AI engine who to hire, the answer isn't a ranking page — it's a sentence. "Here are three options in Denver." If your competitor is in that sentence and you're not, the sale is gone before your website had a chance.

Google rankings don't rescue you. Google AI uses Google's index, but ChatGPT leans heavily on Bing and its own browsing, and Perplexity has a separate retrieval stack. You can rank #1 on Google and still be absent from all three.

## The five-minute check

Run the same two prompts on ChatGPT, Google AI (AI Overviews / AI Mode), and Perplexity:

1. **best [your category] in [your city]**
2. **who should I hire for [your service] near [your city]?**

Record three facts per engine: were you named, who was named instead, and whether the answer cited a source you control (your site, your Google Business Profile, a page you wrote).

**Interpretation:** if you're invisible on the recommendation prompt but present when someone asks "[your brand] reviews", you have a *discovery* problem, not a reputation problem. The model can talk about you when asked by name — it just won't volunteer you.

## The three reasons you get skipped

**1. Crawler access.** A `Disallow: /` in robots.txt — or no explicit allow for GPTBot, ClaudeBot, PerplexityBot, and Google-Extended — means the model works from third-party pages about you, or nothing. Check `https://yoursite.com/robots.txt` before rewriting a word of copy. Our [complete allow-list guide](/articles/ai-crawler-robots-txt-guide/) has the copy-paste config.

**2. Weak entity.** The model must know you're a specific business in a specific place — not a vague brand string. Consistent name/address/phone across directories, Organization or LocalBusiness schema on your homepage, a Google Business Profile, and listings in the directories your category actually uses are how you become a *thing* the model can name.

**3. No citable answer.** Pages that wander for 800 words before the point get summarised poorly. Lead each key page with a 75–150 word direct answer — who you serve, where, what you do, what it costs or how you work — then the evidence. Models prefer extractable blocks over vibes.

## What to do this week

1. Unblock AI crawlers in robots.txt if they're blocked.
2. Add Organization/LocalBusiness JSON-LD matching your homepage.
3. Put a direct answer at the top of your main service page.
4. Re-run the three-engine prompt. Screenshot it. That's your baseline.

## Frequently asked questions

### Is this the same as SEO?

Related, but not identical. Google AI features use Google's index; ChatGPT relies on Bing and its own browsing; Perplexity has a separate stack. Ranking on Google does not guarantee you're the name in an AI answer.

### Why would AI recommend a weaker competitor?

Models cite what they can retrieve as a clear entity with a short, sourced answer. A competitor with weaker service but cleaner schema, directory listings, and answer-first pages often wins the recommendation.

### How often do AI answers change?

Constantly. No tool can guarantee identical results every run — which is why single-prompt screenshots mislead. Test each prompt multiple times and look at the pattern, not one answer.
