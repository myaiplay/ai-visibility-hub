---
title: Schema markup for AI search — the JSON-LD that gets you cited
description: Structured data tells AI engines exactly what your business is. The specific schema types that matter for AI visibility, with copy-paste examples.
type: article
date: 2026-08-17
utm: article_schema
---

# Schema markup for AI search: the JSON-LD that gets you cited

<p class="meta">17 August 2026 · AI Visibility Index</p>

<div class="answer">
<strong>Direct answer:</strong> schema markup (JSON-LD in your page HTML) is how you tell machines — unambiguously — "this is a business, named X, located at Y, offering Z". AI engines use these signals to build the entity understanding behind their recommendations. The two types that matter most for a local business are <code>Organization</code>/<code>LocalBusiness</code> on your homepage and <code>FAQPage</code> on Q&A content. Add them, keep them consistent with your visible content, and you become far easier for an AI to cite correctly.
</div>

## Why AI engines care about schema

When ChatGPT or Perplexity decides who to name, it's really asking: *which entities do I understand well enough to talk about confidently?* A business described only in flowing marketing prose requires the model to guess. A business with clean JSON-LD hands it a form already filled in: legal name, address, phone, hours, services, ratings.

This is the same machinery behind Google's knowledge panels — but AI answer engines lean on it too, because structured data is the cheapest way for them to avoid making things up about you.

## The four types worth your time

**1. Organization or LocalBusiness (homepage).** The foundation. Include name, address, phone, opening hours, service area, same-as links to your profiles:

```
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Summit Plumbing",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Denver",
    "addressRegion": "CO"
  },
  "telephone": "+1-303-555-0134",
  "url": "https://summitplumbing.example",
  "openingHours": "Mo-Su 00:00-24:00",
  "sameAs": [
    "https://www.facebook.com/summitplumbing",
    "https://www.google.com/maps/place/..."
  ]
}
</script>
```

**2. FAQPage (Q&A sections).** Question-and-answer blocks marked as FAQ are exactly the shape AI engines love to quote — a question a customer asks, with a direct answer attached.

**3. Article (blog content).** Author, date, headline — establishes freshness and attribution for your content.

**4. Service or Product (offer pages).** What you sell and at what price — lets AI answer "how much does X charge?" without guessing.

## The rules that actually matter

- **Match the visible page.** Markup describing content that isn't shown to visitors violates Google's guidelines and erodes trust signals everywhere.
- **Consistency beats completeness.** Name, address, and phone identical across schema, your footer, your Google Business Profile, and directories. One inconsistency can split your entity in two.
- **Test it.** Run your URL through Google's Rich Results Test and validator.schema.org after adding anything.

Not sure what shape your site is in? Our [free AI Readiness Score](https://aicantfindme.com/services/ai-readiness?utm_source=hub&utm_medium=article&utm_campaign=article_schema) checks your homepage's schema, indexability, and answer-first content in one pass.

## Frequently asked questions

### Is schema a ranking factor?

Not directly in classic SEO, and AI engines don't publish their weighting. What schema demonstrably does is improve *entity understanding* — which is the substrate recommendations are built from.

### Do I need a developer to add JSON-LD?

Usually no. It's a paste-in script block; most CMSs have a field or plugin for it, and many SEO plugins generate Organization/LocalBusiness schema from a settings form.

### Can wrong schema hurt me?

Yes — markup that contradicts your visible content (fake reviews, wrong addresses) can trigger spam policies and confuses AI engines. When in doubt, mark up less, accurately.
