---
title: Windows input benchmark dataset — raw reports and provenance
description: Download measured QPC timestamps, sequence validation, environment records, failed runs and derived statistics for the TitanCSA benchmark laboratory.
dataset: true
published: 2026-11-17
updated: 2026-11-17
---
# Download the evidence

[Raw CSV/JSON and environment archive](assets/raw-results.zip) · [HID per-run results](assets/results.json) · [HID aggregate intervals](assets/aggregates.json) · [Controller per-run results](assets/xinput-results.json) · [Joystick results](assets/joystick-results.json) · [Stability records](assets/stability-results.json) · [Resource diagnostics](methodology/diagnostics.md)

Data are CC BY 4.0; benchmark code is MIT. Upstream software and repository metadata retain their own terms. Cite the run ID and exact repository revision. Raw runs are append-only: a failed run is retained, and a retry receives a new identifier.

`submission.csv` records sequence, entry QPC, return QPC and SDK error. `reception.csv` records source sequence, submission QPC, receive QPC and content validity. XInput uses corresponding `xinput-*.csv` files with one acknowledged state outstanding. QPC frequency, warm-up, seed, rate, profile and origin are in each run JSON. PnP text snapshots are retained when collected. Derived JSON records validation status and file hashes.

The archive contains real measurements and invalid-run diagnostics. It contains no simulated ranking, private credentials, activation keys or commercial package.
