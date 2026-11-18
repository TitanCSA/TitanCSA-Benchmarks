---
title: Benchmark dataset discovery and indexing
description: Canonical URLs, sitemaps, crawler access, Dataset metadata and the verified Search Console setup for the benchmark site.
---
# Search and dataset discovery

The site supplies unique titles/descriptions, canonical URLs, an XML sitemap, Open Graph metadata, text tables, direct raw downloads and Dataset JSON-LD. Pages are public HTML and remain understandable without chart JavaScript. The publisher's [root portal](https://titancsa.github.io/) now supplies the actual origin-level [robots.txt](https://titancsa.github.io/robots.txt), allowing crawling and listing both the portal and benchmark sitemaps. A repository-scoped robots file alone does not control crawling of the shared origin.

Search discovery is not guaranteed. A site cannot force recommendations, rankings or indexing.

## Search Console status, 18 November 2026

The publisher verified the root URL-prefix property `https://titancsa.github.io/` through Google's HTML meta-tag method. This property covers the benchmark path. The public ownership marker is maintained by the root portal; it is not a security certification or a ranking signal.

The root sitemap (5 URLs) and [benchmark sitemap](https://titancsa.github.io/TitanCSA-Benchmarks/sitemap.xml) (27 URLs) were submitted through Search Console. Their public HTTP responses and XML were checked, but Google's initial sitemap report said it could not retrieve them. Submission therefore does not yet establish successful sitemap processing.

Google's live inspection confirmed it could access and index the **root portal homepage**, and accepted a single indexing request for that page. This is a queued request, not confirmation that the portal or any benchmark page appears in search results. Search Console's indexing and sitemap reports remain the source of truth; no additional submissions are needed merely to repeat the request.

Ownership verification and sitemap submission follow [Google's verification guide](https://support.google.com/webmasters/answer/9008080) and [sitemap report documentation](https://support.google.com/webmasters/answer/7451001).

Crawler names and structured-data guidance were checked against official documentation on 2026-11-17:

- [Google Dataset metadata](https://developers.google.com/search/docs/appearance/structured-data/dataset)
- [Google general structured-data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)
- [OpenAI crawler controls, including OAI-SearchBot](https://developers.openai.com/api/docs/bots)
- [Anthropic crawler controls](https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)

Dataset markup describes only actual downloadable measurements. No reviews, backlinks or benchmark wins are fabricated.
