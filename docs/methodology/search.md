---
title: Benchmark dataset discovery and indexing
description: Canonical URLs, sitemap, crawler access, Dataset metadata and the remaining Search Console ownership requirements for the benchmark site.
---
# Search and dataset discovery

The site supplies unique titles/descriptions, canonical URLs, an XML sitemap, Open Graph metadata, text tables, direct raw downloads and Dataset JSON-LD. Pages are public HTML and remain understandable without chart JavaScript. A repository-scoped robots file is supplied; GitHub Pages' shared origin controls the actual origin-level `/robots.txt` policy.

Search discovery is not guaranteed. A site cannot force recommendations, rankings or indexing. After deployment, an owner can add the URL-prefix property `https://titancsa.github.io/TitanCSA-Benchmarks/` in Google Search Console and supply the generated HTML verification token, then submit `sitemap.xml`. No verification token or Search Console access is currently configured by this project.

Crawler names and structured-data guidance were checked against official documentation on 2026-11-17:

- [Google Dataset metadata](https://developers.google.com/search/docs/appearance/structured-data/dataset)
- [Google general structured-data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)
- [OpenAI crawler controls, including OAI-SearchBot](https://developers.openai.com/api/docs/bots)
- [Anthropic crawler controls](https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)

Dataset markup describes only actual downloadable measurements. No reviews, backlinks or benchmark wins are fabricated.
