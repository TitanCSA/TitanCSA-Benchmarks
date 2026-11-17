---
title: Windows virtual HID throughput — requested vs observed cadence
description: Why requested scheduling rate, SDK acceptance, observed reports and USB polling are distinct metrics in the Vdevice virtual HID campaign.
published: 2026-11-17
updated: 2026-11-17
---
# Submission cadence and delivered reports

The campaign requests 125, 1,000 and 10,000 reports per second using a high-resolution waitable timer where supported. It records actual QPC submission intervals, SDK return codes and independently observed content. [Per-run results](../assets/results.json) include actual rate, missing reports and submission cost.

A requested 10 kHz submission schedule is not proof of 10 kHz physical USB polling. The virtual full-speed HID descriptor requests a 1 ms interrupt interval. Windows scheduling, buffers and virtual USB behavior remain part of the path. These finite-rate scenarios do not establish an absolute maximum sustainable throughput.

See the [measured table](latency.md) for all rates and the [raw CSV archive](../assets/raw-results.zip) to reconstruct the observed cadence. Longer saturation and multi-device campaigns must be executed before claiming a maximum throughput or long-term stability bound.

