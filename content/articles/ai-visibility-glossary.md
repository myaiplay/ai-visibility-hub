---
title: AI visibility glossary — 18 terms in plain English
description: GEO, AEO, entity, OAI-SearchBot, share of model — the vocabulary of AI search explained simply, so you can tell real signal from vendor jargon.
type: article
date: 2026-08-17
utm: article_glossary
---

# AI visibility glossary: 18 terms in plain English

<p class="meta">17 August 2026 · AI Visibility Index</p>

<div class="answer">
<strong>Why this exists:</strong> the AI-search industry sprouts jargon faster than it sprouts standards. Half of it describes real mechanics; half is marketing fog. Here's the vocabulary you'll meet, in plain English, with an honest note on what actually matters.
</div>

## The big ideas

**AI visibility** — How often AI engines name your business when people ask buying questions. Measured as a rate across many prompt runs, not a single ranking. The metric that matters most.

**GEO (Generative Engine Optimisation)** — The practice of improving how generative AI engines represent and recommend you. The AI-era sibling of SEO.

**AEO (Answer Engine Optimisation)** — Older term for the same idea, from the featured-snippet era. Now mostly folded into GEO.

**Share of model** — Of all the times an AI recommends *someone* in your category, the share that names you. Like share of voice, for AI answers.

**Entity** — A thing the model recognises as real and distinct: a business with a name, place, and consistent identity. Becoming a clean entity is half the battle — models recommend things, not strings of text.

**Citation** — When an AI answer links to or names a source. Being *cited* (as a source) and being *recommended* (as an option) are different wins; you want both.

## The machinery

**AI crawler** — The bot that fetches your pages for an AI company. The ones to know: **GPTBot** (OpenAI training), **OAI-SearchBot** (ChatGPT search citations), **ChatGPT-User** (live browsing), **PerplexityBot**, **ClaudeBot**, **Google-Extended**. Each can be allowed or blocked separately in robots.txt — [our allow-list guide](/articles/ai-crawler-robots-txt-guide/) has the config.

**Retrieval** — The step where the AI fetches current information before answering. If retrieval can't find you, no amount of training-data presence saves you.

**RAG (Retrieval-Augmented Generation)** — The architecture behind search-enabled AI: retrieve documents, then generate an answer grounded in them. Why "being findable" and "being quotable" are two separate problems.

**Index** — The database of crawled pages an engine searches. Google AI uses Google's index; ChatGPT leans on [Bing's](/articles/chatgpt-runs-on-bing/); Perplexity runs its own.

**Grounding** — Anchoring an answer in retrieved sources rather than the model's memory. Grounded answers are the ones that can name you correctly.

**Hallucination** — When a model states something false with confidence. Clean entities and consistent data across the web are the best defence against hallucinated claims about your business.

## The formats

**llms.txt** — A proposed briefing file at your site root telling AI models what you are and what matters. [Plain-English guide here](/articles/llms-txt-guide/).

**JSON-LD** — The script format for schema markup. Machine-readable identity for your business — [with examples](/articles/schema-for-ai-search/).

**Schema / structured data** — Standardised tags (schema.org) describing businesses, articles, FAQs. The vocabulary JSON-LD carries.

**Answer-first content** — Pages that lead with a 75–150 word direct answer before the detail. The format AI engines extract most reliably.

**Prompt tracking** — Running fixed sets of buyer questions against AI engines over time to measure visibility. What our [data engine](/dashboard/) does nightly.

## Frequently asked questions

### Is GEO just SEO with a new name?

They overlap heavily — good structure, clear entities, quality content help both. The differences are in retrieval sources (Bing matters again), output format (sentences, not links), and measurement (visibility rates, not positions).

### Which single term should I care about most?

AI visibility rate — the share of relevant buyer questions where you get named. Everything else is a means to move that number.

### Are "AI SEO tools" that promise rankings legit?

Be sceptical of anyone promising fixed positions in AI answers — answers are regenerated every run and vary. Legitimate tools measure patterns across many runs and show their evidence. That's the standard to hold vendors to, [us included](https://aicantfindme.com?utm_source=hub&utm_medium=article&utm_campaign=article_glossary).
