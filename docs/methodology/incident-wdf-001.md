---
title: Vdevice WDF-001 — signed fix and validation scope
description: Follow the original Vdevice 1.0.5.0 controller crash, the signed demo teardown tests and the signed Release 1.0.4.1 setup checks.
---
# WDF-001: signed demo fix and commercial qualification

The original 1.0.5.0 controller campaigns recorded the bugchecks described below. The queue-lifetime fix is available in the signed demo and the signed commercial Release. [Vdevice issue #1](https://github.com/TitanCSA/Vdevice/issues/1).

| Edition with signed driver | Verified scope |
|---|---|
| [Demo 1.0.6.0](https://github.com/TitanCSA/Vdevice/releases/tag/v1.0.6.0-demo) | The Windows 11 Hyper-V guest with Secure Boot enabled passed 100 create/delete cycles, 100 early owner-close cycles, and ten rounds of the five device examples, including virtual DS4 and Xbox One/GIP. The controller filter service was running. Windows stayed on the same boot and recorded no bugcheck. |
| [Demo 1.0.6.1](https://github.com/TitanCSA/Vdevice/releases/tag/v1.0.6.1-demo) | Includes the queue-lifetime fix. Setup passed the Windows 10 and Windows 11 upgrade and removal checks. [Package and setup evidence](https://titancsa.github.io/assets/vdevice-signed-versions-2026-11-25.json). |
| Commercial Release 1.0.4.1 | Setup passed the Windows 10 and Windows 11 upgrade and removal checks. A separate Windows 11 test with Secure Boot and Memory Integrity enabled confirmed that the matching Release SDK could read the new driver after restart, before activation. [Package and setup evidence](https://titancsa.github.io/assets/vdevice-signed-versions-2026-11-25.json). |

**Two real guest bugchecks interrupted separate controller campaigns.** Two DS4 series passed the per-run validation before the next repetition crashed. In a later Xbox One/GIP campaign, two producer/receiver sequences completed before another crash; those filter series remain excluded from latency comparisons because the adapter captured extra protocol reports without one-to-one generated-state correlation. Both minidumps have the same WDF queue-purge signature at `Vdevice+0x651e`. Successful latency rows do not erase this incident and do not establish safe repeated teardown.

| Evidence | Observation |
|---|---|
| Bugcheck | `WDF_VIOLATION 0x10D`, argument 1 `0xA` ? fatal queue operation |
| Stack boundary | `Wdf01000!imp_WdfIoQueuePurge` ? `Vdevice+0x651e` |
| Driver under investigation | Vdevice 1.0.5.0, SHA-256 `3977be4dd7811eb4e0f0bc0ad9e2e2df3f63facc514d5484a08c78fd9b1bc5c8` |
| Test contexts | Virtual DS4 and virtual Xbox One/GIP with Interceptor Gamepad & Controller 1.0.13.0 in Windows 11 Hyper-V |
| Driver Verifier | Flags `0x00000000`; no verified drivers configured |
| Host impact | None observed; all tested drivers and the crash remained in the dedicated VM |

## What the original campaign established

Windows recorded the bugcheck and saved a minidump and kernel dump. Microsoft CDB analysis reaches Vdevice at an asynchronous WDF queue-purge call. The WDF in-flight log explicitly reports that the queue **is already deleted**, with `0xC0000056 (STATUS_DELETE_PENDING)`. The public source has `WdfIoQueuePurge` calls in `VdEndpointPurge` and queue deletion in `DeleteVirtual`. This establishes the invalid queue state at the failing call; it does not yet establish the complete ordering of the initiating callbacks.

The original crash analysis established a deleted queue at the failing call. It left the exact sequence of initiating callbacks open. The fix keeps queue operations alive until completion and drains them before retirement. [Source change](https://github.com/TitanCSA/Vdevice/commit/9aee17beccafeec33f839c428a6f368d82fe73ab).

## Follow-up after the demo fix

The commercial test establishes readiness before activation. Repeated activated Release teardown, longer-duration testing and additional hardware coverage remain to be measured.

The dumps remain local because a kernel dump contains broad system state. Their SHA-256 fingerprints and a sanitized incident record are published in `reports/incident-wdf-001.json`. The dataset retains the completed and interrupted runs from the original 1.0.5.0 campaign.
