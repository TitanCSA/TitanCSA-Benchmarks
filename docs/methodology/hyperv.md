---
title: Dedicated Hyper-V input driver benchmark lab
description: VM ownership checks, immutable parent disk, clean checkpoints and fixed resources used for isolated Windows driver measurements.
---
# Hyper-V lab isolation

`TitanCSA-Benchmark-Lab` uses a dedicated differencing VHDX, 2 vCPU and 3 GiB fixed RAM. Dynamic Memory is disabled. Secure Boot is enabled. A stopped existing lab image supplies the immutable parent; the parent's VM is not started or changed. The owned lab's identity is recorded under ignored `.local/lab.json` and checked before restore, copy or installation.

The initial inherited image contained historical `Filter` packages. Those were discovered through PnP inspection and removed only in the dedicated child VM. The original checkpoint is retained as `Inherited-Image-Before-Input-Cleanup`; it is not the corrected clean baseline. After removing the historical packages and uninstalling the measured drivers, Windows was restarted and `Clean-Benchmark-Baseline` was created. `reports/clean-baseline-v2.txt` records the checked driver inventory. Older pilot data retain their original provenance and are not claimed to be pristine-image measurements.

Driver-specific `*-Cleaned-Ready` checkpoints isolate later configurations. Restores apply only to the recorded benchmark VM. Export results before restoring: guest results intentionally disappear with the checkpoint. No checkpoint or clock manipulation is used to extend a demonstration allowance; each evaluation stays within the published session terms.

PowerShell Direct controls the guest without embedding a password in scripts or publications. Compilers run on the host, producing static-CRT executables copied into the guest. Drivers and workloads run only in the guest. WPR is already installed there. Installing a second compiler and WDK in the measured VM is unnecessary for these prebuilt signed-driver scenarios and would change background services and storage load.

Hyper-V does not supply universal native USB passthrough. No physical USB controller is assigned here; RDP redirection is not treated as direct USB hardware. Results are explicitly virtual-device software-path measurements.
