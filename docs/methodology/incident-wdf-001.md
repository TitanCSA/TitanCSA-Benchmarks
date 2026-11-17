---
title: Known stability incident ? WDF queue purge during virtual controller testing
description: An evidence record of a Windows WDF bugcheck observed in the dedicated VM, including driver hash, queue state and unresolved initiating cause.
---
# WDF-001: stability qualification is incomplete

**Two real guest bugchecks interrupted separate controller campaigns.** Two DS4 series passed the per-run validation before the next repetition crashed. In a later Xbox One/GIP campaign, two producer/receiver sequences completed before another crash; those filter series remain excluded from latency comparisons because the adapter captured extra protocol reports without one-to-one generated-state correlation. Both minidumps have the same WDF queue-purge signature at `Vdevice+0x651e`. Successful latency rows do not erase this incident and do not establish safe repeated teardown.

| Evidence | Observation |
|---|---|
| Bugcheck | `WDF_VIOLATION 0x10D`, argument 1 `0xA` ? fatal queue operation |
| Stack boundary | `Wdf01000!imp_WdfIoQueuePurge` ? `Vdevice+0x651e` |
| Driver under investigation | Vdevice 1.0.5.0, SHA-256 `3977be4dd7811eb4e0f0bc0ad9e2e2df3f63facc514d5484a08c78fd9b1bc5c8` |
| Test contexts | Virtual DS4 and virtual Xbox One/GIP with Interceptor Gamepad & Controller 1.0.13.0 in Windows 11 Hyper-V |
| Driver Verifier | Flags `0x00000000`; no verified drivers configured |
| Host impact | None observed; all tested drivers and the crash remained in the dedicated VM |

## What is established

Windows recorded the bugcheck and saved a minidump and kernel dump. Microsoft CDB analysis reaches Vdevice at an asynchronous WDF queue-purge call. The WDF in-flight log explicitly reports that the queue **is already deleted**, with `0xC0000056 (STATUS_DELETE_PENDING)`. The public source has `WdfIoQueuePurge` calls in `VdEndpointPurge` and queue deletion in `DeleteVirtual`. This establishes the invalid queue state at the failing call; it does not yet establish the complete ordering of the initiating callbacks.

**The exact lifetime race and initiating sequence are still under investigation.** Private matching driver symbols were not loaded in the first analysis. Stack involvement does not prove that every Vdevice configuration fails or that another component is irrelevant. No driver was patched or rebuilt to change the benchmark outcome.

## Required follow-up

Preserve the dump and exact signed binary; correlate WDF queue state with endpoint purge and device deletion. Build an isolated teardown reproducer, review callback/queue lifetime ordering, and test the eventual fix under cancellation, repeated removal, restart and concurrent requests. Any changed kernel image needs its normal signing and qualification process before distribution.

The dumps remain local because a kernel dump contains broad system state. Their SHA-256 fingerprints and a sanitized incident record are published in `reports/incident-wdf-001.json`. Raw completed and interrupted runs remain in the dataset. This is an open stability limitation, not a resolved bug or a production certification.
