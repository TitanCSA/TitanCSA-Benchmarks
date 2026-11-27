---
title: TitanCSA drivers — eighteen-point architecture and evidence audit
description: Per-project source, SDK, licensing, installation, runtime evidence and performance limitations for the four main TitanCSA driver products.
---
# Main projects: architecture and evidence audit

**Source** means inspected code at the pinned revision. **Documented** means an upstream claim. **Measured** means selected paths actually executed in the owned guest; it never certifies every supported device. No driver behavior was changed.

## Interceptor

| Audit point | Evidence and boundary |
|---|---|
| 01 Architecture | Source: KMDF input filter, control interface and product-specific input/controller masks. [driver](https://github.com/TitanCSA/Interceptor/tree/fc8742edfdc8ca12872ea2eb2dcbe8e84a278859/driver) |
| 02 Ring 0 / Ring 3 | Source: signed SYS handles kernel/PnP/I/O work; C++ SDK, examples and installer execute in user mode. SDK calls do not grant arbitrary kernel execution. |
| 03 Driver type | Source: WdfFdoInitSetFilter paths; input/device family depends on product build masks. |
| 04 API / SDK | Source: Init_AllDevices, Get_Input_With_Timeout and Send_Input; product-specific event families. [Interceptor](https://github.com/TitanCSA/Interceptor/tree/fc8742edfdc8ca12872ea2eb2dcbe8e84a278859/Interceptor) |
| 05 Languages | Source inventory: C kernel implementation, C++ SDK/examples, PowerShell build/install orchestration and C# installer/UI components. Registry wrappers are not separate kernel implementations. |
| 06 Compatible devices | Documented product families: keyboard/mouse, HID/XUSB/XInputHID/GIP controllers. Selected virtual fixtures are measured; physical devices remain unqualified. |
| 07 Verified functionality | Measured: keyboard forwarding, mouse modification and XUSB modification. |
| 08 Mechanism | Source: capture through family-specific filter paths, user-mode decision and forwarding. Measured modification must be independently visible; PnP attachment is required. |
| 09 Technical limitations | These virtual fixtures cover selected transport paths. GIP/ViGEm-filter extra protocol reports lack one-to-one capture correlation. See the [WDF-001 incident](../methodology/incident-wdf-001.md) for the signed demo teardown and commercial pre-activation checks. |
| 10 Windows compatibility | Documented: Windows 10/11 x64 (Interceptor combined specifies 1709+). Measured: Windows 11 build 26100 Hyper-V only, Secure Boot on and HVCI off. No HLK/HVCI qualification claimed. |
| 11 Signature | Measured installation: downloaded release SYS Authenticode verified as Valid, Microsoft Windows Hardware Compatibility Publisher. Source/release identity and hashes are separate evidence; source availability does not certify a rebuilt SYS. |
| 12 License | Inspected: user-mode source MIT; driver/demo/evaluation-source terms and third-party licenses are separate. One-hour demo behavior was retained. [LICENSE](https://github.com/TitanCSA/Interceptor/tree/fc8742edfdc8ca12872ea2eb2dcbe8e84a278859/LICENSE); [driver/README.md](https://github.com/TitanCSA/Interceptor/tree/fc8742edfdc8ca12872ea2eb2dcbe8e84a278859/driver/README.md) |
| 13 Benchmark possibilities | Executed: generated virtual fixtures crossing selected filters, independent observed content and capture/PnP gating. Missing: exhaustive physical controllers, Bluetooth and every protocol feature. |
| 14 Installation | Executed signed release GUI/CLI installer in owned VM, PnP/service/signature checks, device creation and independent behavior checks. Controller association sometimes needs a guest restart. [docs/INSTALLATION.md](https://github.com/TitanCSA/Interceptor/tree/fc8742edfdc8ca12872ea2eb2dcbe8e84a278859/docs/INSTALLATION.md) |
| 15 Existing examples | [Examples](https://github.com/TitanCSA/Interceptor/tree/fc8742edfdc8ca12872ea2eb2dcbe8e84a278859/Examples); consumed as source fixtures, not assumed to prove support. Vdevice ExampleRuntime uses a stable USB serial for repeatable per-instance filter association. |
| 16 Repository activity | Metadata: pinned commit fc8742edfdc8ca12872ea2eb2dcbe8e84a278859; last commit 2026-11-16T00:19:31Z; archived=False; latest audited release v1.4.22.0-demo. README-only updates after the audit do not change the measured binary. |
| 17 Existing tests | Source inventory: `Examples/UI/FrameRefreshTests.cs`, `Installer/UI/Tests/InstallerTests.ps1`, `Installer/UI/Tests/ManagedInstallerTests.cs`. Only actual lab results and the recorded upstream Vdevice live test are asserted as executed. |
| 18 Performance risks | Observed: scheduler/SDK/queue overhead, large filtered mouse end-to-end delays, and shared-host tails. Vdevice controller teardown reproduced WDF queue-purge STATUS_DELETE_PENDING. Profile-specific ViGEm/vJoy median advantages remain visible; no universal TitanCSA speed/stability claim. |

## Interceptor-Keyboard-Mouse

| Audit point | Evidence and boundary |
|---|---|
| 01 Architecture | Source: KMDF input filter, control interface and product-specific input/controller masks. [driver](https://github.com/TitanCSA/Interceptor-Keyboard-Mouse/tree/a189e6ed3a399bea80b887ab44f0de001097449e/driver) |
| 02 Ring 0 / Ring 3 | Source: signed SYS handles kernel/PnP/I/O work; C++ SDK, examples and installer execute in user mode. SDK calls do not grant arbitrary kernel execution. |
| 03 Driver type | Source: WdfFdoInitSetFilter paths; input/device family depends on product build masks. |
| 04 API / SDK | Source: Init_AllDevices, Get_Input_With_Timeout and Send_Input; product-specific event families. [Interceptor](https://github.com/TitanCSA/Interceptor-Keyboard-Mouse/tree/a189e6ed3a399bea80b887ab44f0de001097449e/Interceptor) |
| 05 Languages | Source inventory: C kernel implementation, C++ SDK/examples, PowerShell build/install orchestration and C# installer/UI components. Registry wrappers are not separate kernel implementations. |
| 06 Compatible devices | Documented product families: keyboard/mouse. Selected virtual fixtures are measured; physical devices remain unqualified. |
| 07 Verified functionality | Measured: keyboard forwarding, mouse forwarding/modification/controlled block. |
| 08 Mechanism | Source: capture through family-specific filter paths, user-mode decision and forwarding. Measured modification must be independently visible; PnP attachment is required. |
| 09 Technical limitations | These virtual fixtures cover selected transport paths. GIP/ViGEm-filter extra protocol reports lack one-to-one capture correlation. See the [WDF-001 incident](../methodology/incident-wdf-001.md) for the signed demo teardown and commercial pre-activation checks. |
| 10 Windows compatibility | Documented: Windows 10/11 x64 (Interceptor combined specifies 1709+). Measured: Windows 11 build 26100 Hyper-V only, Secure Boot on and HVCI off. No HLK/HVCI qualification claimed. |
| 11 Signature | Measured installation: downloaded release SYS Authenticode verified as Valid, Microsoft Windows Hardware Compatibility Publisher. Source/release identity and hashes are separate evidence; source availability does not certify a rebuilt SYS. |
| 12 License | Inspected: user-mode source MIT; driver/demo/evaluation-source terms and third-party licenses are separate. One-hour demo behavior was retained. [LICENSE](https://github.com/TitanCSA/Interceptor-Keyboard-Mouse/tree/a189e6ed3a399bea80b887ab44f0de001097449e/LICENSE); [driver/README.md](https://github.com/TitanCSA/Interceptor-Keyboard-Mouse/tree/a189e6ed3a399bea80b887ab44f0de001097449e/driver/README.md) |
| 13 Benchmark possibilities | Executed: generated virtual fixtures crossing selected filters, independent observed content and capture/PnP gating. Missing: exhaustive physical controllers, Bluetooth and every protocol feature. |
| 14 Installation | Executed signed release GUI/CLI installer in owned VM, PnP/service/signature checks, device creation and independent behavior checks. Controller association sometimes needs a guest restart. [docs/INSTALLATION.md](https://github.com/TitanCSA/Interceptor-Keyboard-Mouse/tree/a189e6ed3a399bea80b887ab44f0de001097449e/docs/INSTALLATION.md) |
| 15 Existing examples | [Examples](https://github.com/TitanCSA/Interceptor-Keyboard-Mouse/tree/a189e6ed3a399bea80b887ab44f0de001097449e/Examples); consumed as source fixtures, not assumed to prove support. Vdevice ExampleRuntime uses a stable USB serial for repeatable per-instance filter association. |
| 16 Repository activity | Metadata: pinned commit a189e6ed3a399bea80b887ab44f0de001097449e; last commit 2026-11-16T00:18:51Z; archived=False; latest audited release v1.0.5.0-demo. README-only updates after the audit do not change the measured binary. |
| 17 Existing tests | Source inventory: `Installer/UI/Tests/InstallerTests.ps1`, `Installer/UI/Tests/ManagedInstallerTests.cs`. Only actual lab results and the recorded upstream Vdevice live test are asserted as executed. |
| 18 Performance risks | Observed: scheduler/SDK/queue overhead, large filtered mouse end-to-end delays, and shared-host tails. Vdevice controller teardown reproduced WDF queue-purge STATUS_DELETE_PENDING. Profile-specific ViGEm/vJoy median advantages remain visible; no universal TitanCSA speed/stability claim. |

## Interceptor-Gamepad-Controller

| Audit point | Evidence and boundary |
|---|---|
| 01 Architecture | Source: KMDF input filter, control interface and product-specific input/controller masks. [driver](https://github.com/TitanCSA/Interceptor-Gamepad-Controller/tree/1146b8541683985345c28c4ecf2fc8000c908ae2/driver) |
| 02 Ring 0 / Ring 3 | Source: signed SYS handles kernel/PnP/I/O work; C++ SDK, examples and installer execute in user mode. SDK calls do not grant arbitrary kernel execution. |
| 03 Driver type | Source: WdfFdoInitSetFilter paths; input/device family depends on product build masks. |
| 04 API / SDK | Source: Init_AllDevices, Get_Input_With_Timeout and Send_Input; product-specific event families. [Interceptor](https://github.com/TitanCSA/Interceptor-Gamepad-Controller/tree/1146b8541683985345c28c4ecf2fc8000c908ae2/Interceptor) |
| 05 Languages | Source inventory: C kernel implementation, C++ SDK/examples, PowerShell build/install orchestration and C# installer/UI components. Registry wrappers are not separate kernel implementations. |
| 06 Compatible devices | Documented product families: HID/XUSB/XInputHID/GIP controllers. Selected virtual fixtures are measured; physical devices remain unqualified. |
| 07 Verified functionality | Measured: XUSB modification and DS4 modification. |
| 08 Mechanism | Source: capture through family-specific filter paths, user-mode decision and forwarding. Measured modification must be independently visible; PnP attachment is required. |
| 09 Technical limitations | These virtual fixtures cover selected transport paths. GIP/ViGEm-filter extra protocol reports lack one-to-one capture correlation. See the [WDF-001 incident](../methodology/incident-wdf-001.md) for the signed demo teardown and commercial pre-activation checks. |
| 10 Windows compatibility | Documented: Windows 10/11 x64 (Interceptor combined specifies 1709+). Measured: Windows 11 build 26100 Hyper-V only, Secure Boot on and HVCI off. No HLK/HVCI qualification claimed. |
| 11 Signature | Measured installation: downloaded release SYS Authenticode verified as Valid, Microsoft Windows Hardware Compatibility Publisher. Source/release identity and hashes are separate evidence; source availability does not certify a rebuilt SYS. |
| 12 License | Inspected: user-mode source MIT; driver/demo/evaluation-source terms and third-party licenses are separate. One-hour demo behavior was retained. [LICENSE](https://github.com/TitanCSA/Interceptor-Gamepad-Controller/tree/1146b8541683985345c28c4ecf2fc8000c908ae2/LICENSE); [driver/README.md](https://github.com/TitanCSA/Interceptor-Gamepad-Controller/tree/1146b8541683985345c28c4ecf2fc8000c908ae2/driver/README.md) |
| 13 Benchmark possibilities | Executed: generated virtual fixtures crossing selected filters, independent observed content and capture/PnP gating. Missing: exhaustive physical controllers, Bluetooth and every protocol feature. |
| 14 Installation | Executed signed release GUI/CLI installer in owned VM, PnP/service/signature checks, device creation and independent behavior checks. Controller association sometimes needs a guest restart. [docs/INSTALLATION.md](https://github.com/TitanCSA/Interceptor-Gamepad-Controller/tree/1146b8541683985345c28c4ecf2fc8000c908ae2/docs/INSTALLATION.md) |
| 15 Existing examples | [Examples](https://github.com/TitanCSA/Interceptor-Gamepad-Controller/tree/1146b8541683985345c28c4ecf2fc8000c908ae2/Examples); consumed as source fixtures, not assumed to prove support. Vdevice ExampleRuntime uses a stable USB serial for repeatable per-instance filter association. |
| 16 Repository activity | Metadata: pinned commit 1146b8541683985345c28c4ecf2fc8000c908ae2; last commit 2026-11-16T00:18:57Z; archived=False; latest audited release v1.0.13.0-demo. README-only updates after the audit do not change the measured binary. |
| 17 Existing tests | Source inventory: `Examples/UI/FrameRefreshTests.cs`, `Installer/UI/Tests/InstallerTests.ps1`, `Installer/UI/Tests/ManagedInstallerTests.cs`. Only actual lab results and the recorded upstream Vdevice live test are asserted as executed. |
| 18 Performance risks | Observed: scheduler/SDK/queue overhead, large filtered mouse end-to-end delays, and shared-host tails. Vdevice controller teardown reproduced WDF queue-purge STATUS_DELETE_PENDING. Profile-specific ViGEm/vJoy median advantages remain visible; no universal TitanCSA speed/stability claim. |

## Vdevice

| Audit point | Evidence and boundary |
|---|---|
| 01 Architecture | Source: KMDF/UdeCx USB-device emulation with user-mode descriptor/report SDK. [driver](https://github.com/TitanCSA/Vdevice/tree/ff8a74d0136012b04b76a0e86b7a5abf89e64294/driver) |
| 02 Ring 0 / Ring 3 | Source: signed SYS handles kernel/PnP/I/O work; C++ SDK, examples and installer execute in user mode. SDK calls do not grant arbitrary kernel execution. |
| 03 Driver type | Source: UdeCx device-emulation driver, not an input-rewriting filter. |
| 04 API / SDK | Source: Create_Device, Delete_Device and Send_Input; raw USB/HID configuration. [Vdevice](https://github.com/TitanCSA/Vdevice/tree/ff8a74d0136012b04b76a0e86b7a5abf89e64294/Vdevice) |
| 05 Languages | Source inventory: C kernel implementation, C++ SDK/examples, PowerShell build/install orchestration and C# installer/UI components. Registry wrappers are not separate kernel implementations. |
| 06 Compatible devices | Documented/examples: USB HID keyboard, mouse, DS4, X360 and Xbox One/GIP; arbitrary descriptor support remains subject to Windows stacks. |
| 07 Verified functionality | Measured: vendor HID sequences/checksums, independent keyboard/mouse reception, XUSB/DS4/GIP state delivery, generic joystick and upstream five-profile live test. |
| 08 Mechanism | Source: virtual USB endpoints and report queuing consumed by Windows class drivers; receiver independently uses HID/Raw Input/XInput/WinMM. |
| 09 Technical limitations | These virtual fixtures cover selected transport paths. GIP/ViGEm-filter extra protocol reports lack one-to-one capture correlation. See the [WDF-001 incident](../methodology/incident-wdf-001.md) for the signed demo teardown and commercial pre-activation checks. |
| 10 Windows compatibility | Documented: Windows 10/11 x64 (Interceptor combined specifies 1709+). Measured: Windows 11 build 26100 Hyper-V only, Secure Boot on and HVCI off. No HLK/HVCI qualification claimed. |
| 11 Signature | Measured installation: downloaded release SYS Authenticode verified as Valid, Microsoft Windows Hardware Compatibility Publisher. Source/release identity and hashes are separate evidence; source availability does not certify a rebuilt SYS. |
| 12 License | Inspected: user-mode source MIT; driver/demo/evaluation-source terms and third-party licenses are separate. One-hour demo behavior was retained. [LICENSE](https://github.com/TitanCSA/Vdevice/tree/ff8a74d0136012b04b76a0e86b7a5abf89e64294/LICENSE); [driver/README.md](https://github.com/TitanCSA/Vdevice/tree/ff8a74d0136012b04b76a0e86b7a5abf89e64294/driver/README.md) |
| 13 Benchmark possibilities | Executed: vendor HID, virtual controllers and matched joystick subset. Missing: physical latency, exhaustive endpoint/control coverage and hardware bandwidth. |
| 14 Installation | Executed signed release GUI/CLI installer in owned VM, PnP/service/signature checks, device creation and independent behavior checks. Controller association sometimes needs a guest restart. [docs/INSTALLATION.md](https://github.com/TitanCSA/Vdevice/tree/ff8a74d0136012b04b76a0e86b7a5abf89e64294/docs/INSTALLATION.md) |
| 15 Existing examples | [Examples](https://github.com/TitanCSA/Vdevice/tree/ff8a74d0136012b04b76a0e86b7a5abf89e64294/Examples); consumed as source fixtures, not assumed to prove support. Vdevice ExampleRuntime uses a stable USB serial for repeatable per-instance filter association. |
| 16 Repository activity | Metadata: pinned commit ff8a74d0136012b04b76a0e86b7a5abf89e64294; last commit 2026-11-16T00:20:51Z; archived=False; latest audited release v1.0.5.0-demo. README-only updates after the audit do not change the measured binary. |
| 17 Existing tests | Source inventory: `Tests/ExampleLiveTests.cpp`, `Tests/ExampleTests.cpp`, `Tests/InstallerNativeTests.cpp`, `Tests/InstallerStateTests.cs`, `Tests/InstallerTests.ps1`, `Tests/WorkshopTests.cs`, `Tests/WorkshopTests.ps1`. Only actual lab results and the recorded upstream Vdevice live test are asserted as executed. |
| 18 Performance risks | Observed: scheduler/SDK/queue overhead, large filtered mouse end-to-end delays, and shared-host tails. Vdevice controller teardown reproduced WDF queue-purge STATUS_DELETE_PENDING. Profile-specific ViGEm/vJoy median advantages remain visible; no universal TitanCSA speed/stability claim. |

[Numerical results](../gamepad/results.md) · [Source and competitor inventory](index.md) · [WDF-001 incident and fix status](../methodology/incident-wdf-001.md)
