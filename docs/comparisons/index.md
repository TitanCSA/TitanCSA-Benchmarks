---
title: Windows input driver comparison — source audit and measured scope
description: Pinned source, release and license inventory for TitanCSA, Interception, ViGEmBus, HidHide, vJoy and libvirtualhid, separated by actual purpose.
published: 2026-11-17
updated: 2026-11-17
---
# Source-backed project and competitor audit

Repository metadata checked: 2026-11-17T11:02:37.443484+00:00. Source is pinned by commit; release artifacts have independent hashes. README claims are not automatically runtime-verified.

| Project | Latest audited release | Commit | Last commit date | Archived | Repository license metadata |
|---|---|---|---|---|---|
| [TitanCSA/Interceptor](https://github.com/TitanCSA/Interceptor) | v1.4.22.0-demo | [fc8742edfd](https://github.com/TitanCSA/Interceptor/commit/fc8742edfdc8ca12872ea2eb2dcbe8e84a278859) | 2026-11-16 | False | NOASSERTION |
| [TitanCSA/Interceptor-Keyboard-Mouse](https://github.com/TitanCSA/Interceptor-Keyboard-Mouse) | v1.0.5.0-demo | [a189e6ed3a](https://github.com/TitanCSA/Interceptor-Keyboard-Mouse/commit/a189e6ed3a399bea80b887ab44f0de001097449e) | 2026-11-16 | False | NOASSERTION |
| [TitanCSA/Interceptor-Gamepad-Controller](https://github.com/TitanCSA/Interceptor-Gamepad-Controller) | v1.0.13.0-demo | [1146b85416](https://github.com/TitanCSA/Interceptor-Gamepad-Controller/commit/1146b8541683985345c28c4ecf2fc8000c908ae2) | 2026-11-16 | False | NOASSERTION |
| [TitanCSA/Vdevice](https://github.com/TitanCSA/Vdevice) | v1.0.5.0-demo | [ff8a74d013](https://github.com/TitanCSA/Vdevice/commit/ff8a74d0136012b04b76a0e86b7a5abf89e64294) | 2026-11-16 | False | NOASSERTION |
| [TitanCSA/Interception-V2](https://github.com/TitanCSA/Interception-V2) | v2.0.0 | [04ad866313](https://github.com/TitanCSA/Interception-V2/commit/04ad866313c6ded542c10ee3e640f78ccee2ebb9) | 2026-11-16 | False | Inspect file-level terms |
| [oblitum/Interception](https://github.com/oblitum/Interception) | v1.0.1 | [39eecbbc46](https://github.com/oblitum/Interception/commit/39eecbbc46a52e0402f783b872ef62b0254a896a) | 2021-08-09 | False | Inspect file-level terms |
| [nefarius/ViGEmBus](https://github.com/nefarius/ViGEmBus) | v1.22.0 | [d986e1d937](https://github.com/nefarius/ViGEmBus/commit/d986e1d93708ec9b11049542fa6027272cce716c) | 2023-09-08 | True | BSD-3-Clause |
| [nefarius/ViGEmClient](https://github.com/nefarius/ViGEmClient) | v1.16.18.0 | [b66d02d57e](https://github.com/nefarius/ViGEmClient/commit/b66d02d57e32cc8595369c53418b843e958649b4) | 2023-09-08 | True | MIT |
| [nefarius/HidHide](https://github.com/nefarius/HidHide) | v1.5.230.0 | [5aba4b1bfd](https://github.com/nefarius/HidHide/commit/5aba4b1bfda159f87f5e37bd48f72201616bf87a) | 2026-11-09 | False | MIT |
| [LizardByte/libvirtualhid](https://github.com/LizardByte/libvirtualhid) | v2026.1112.1356.48 | [2234c0079a](https://github.com/LizardByte/libvirtualhid/commit/2234c0079a6a7b0e2f25990d3c705be85bcd37fd) | 2026-11-12 | False | NOASSERTION |
| [jshafer817/vJoy](https://github.com/jshafer817/vJoy) | v2.1.9.1 | [911a2a53a9](https://github.com/jshafer817/vJoy/commit/911a2a53a972f73ea8b4a021c390c953012b7fb9) | 2020-04-17 | False | MIT |
| [microsoft/Windows-driver-samples](https://github.com/microsoft/Windows-driver-samples) | win11-22h2 | [d49bb7d72f](https://github.com/microsoft/Windows-driver-samples/commit/d49bb7d72f3651952b2b6e4ad28d14fe2247eb69) | 2026-11-05 | False | MS-PL |
| [BrunnerInnovation/vJoy](https://github.com/BrunnerInnovation/vJoy) | v2.2.2.0 | [5c3a6528ce](https://github.com/BrunnerInnovation/vJoy/commit/5c3a6528ce5e192ee425dc024407238f02c87e83) | 2023-12-19 | False | MIT |
| [njz3/vJoy](https://github.com/njz3/vJoy) | v2.2.1.1 | [02a337bfaf](https://github.com/njz3/vJoy/commit/02a337bfaf0de44a80f7de5fb70979d05351e276) | 2024-10-29 | False | MIT |

## Compare by purpose

| Category | Relevant solutions | Boundary |
|---|---|---|
| Keyboard/mouse interception | TitanCSA combined/split, Interception V2, oblitum/Interception | Requires attachment and proof that generated events cross the filter |
| Gamepad interception | TitanCSA combined/controller-only | HID, XUSB, XInputHID and GIP are separate paths; creation is not interception |
| Virtual-device creation | Vdevice, ViGEmBus, libvirtualhid, vJoy, Microsoft VHF/UdeCx samples | Compare only equivalent functional profiles |
| Device hiding | HidHide | Complementary access control, not an interception/rewriting replacement |

## Inspected source evidence

### TitanCSA/Vdevice
- `Udecx`: [driver/Driver/Driver.c:158](https://github.com/TitanCSA/Vdevice/blob/ff8a74d0136012b04b76a0e86b7a5abf89e64294/driver/Driver/Driver.c#L158). Source presence is verified; build-time product masks determine which families are enabled.
- `VD_TRIAL_SECONDS`: [driver/Driver/Driver.c:19](https://github.com/TitanCSA/Vdevice/blob/ff8a74d0136012b04b76a0e86b7a5abf89e64294/driver/Driver/Driver.c#L19). Source presence is verified; build-time product masks determine which families are enabled.
- `Send_Input`: [Examples/UI/ExampleRuntime.h:42](https://github.com/TitanCSA/Vdevice/blob/ff8a74d0136012b04b76a0e86b7a5abf89e64294/Examples/UI/ExampleRuntime.h#L42). Source presence is verified; build-time product masks determine which families are enabled.

### TitanCSA/Interceptor
- `WdfFdoInitSetFilter`: [driver/InterceptorDriver/ControllerGip.c:944](https://github.com/TitanCSA/Interceptor/blob/fc8742edfdc8ca12872ea2eb2dcbe8e84a278859/driver/InterceptorDriver/ControllerGip.c#L944). Source presence is verified; build-time product masks determine which families are enabled.
- `IC_PRODUCT_INPUT_MASK`: [driver/InterceptorDriver/Control.c:372](https://github.com/TitanCSA/Interceptor/blob/fc8742edfdc8ca12872ea2eb2dcbe8e84a278859/driver/InterceptorDriver/Control.c#L372). Source presence is verified; build-time product masks determine which families are enabled.
- `Get_Input_With_Timeout`: [Examples/Console/01_Keyboard_Swap_H_J.cpp:26](https://github.com/TitanCSA/Interceptor/blob/fc8742edfdc8ca12872ea2eb2dcbe8e84a278859/Examples/Console/01_Keyboard_Swap_H_J.cpp#L26). Source presence is verified; build-time product masks determine which families are enabled.

### TitanCSA/Interceptor-Keyboard-Mouse
- `WdfFdoInitSetFilter`: [driver/InterceptorDriver/ControllerGip.c:866](https://github.com/TitanCSA/Interceptor-Keyboard-Mouse/blob/a189e6ed3a399bea80b887ab44f0de001097449e/driver/InterceptorDriver/ControllerGip.c#L866). Source presence is verified; build-time product masks determine which families are enabled.
- `IC_PRODUCT_CONTROLLER_MASK`: [driver/InterceptorDriver/Control.c:366](https://github.com/TitanCSA/Interceptor-Keyboard-Mouse/blob/a189e6ed3a399bea80b887ab44f0de001097449e/driver/InterceptorDriver/Control.c#L366). Source presence is verified; build-time product masks determine which families are enabled.
- `Get_Input_With_Timeout`: [Examples/Console/01_Keyboard_Swap_H_J.cpp:26](https://github.com/TitanCSA/Interceptor-Keyboard-Mouse/blob/a189e6ed3a399bea80b887ab44f0de001097449e/Examples/Console/01_Keyboard_Swap_H_J.cpp#L26). Source presence is verified; build-time product masks determine which families are enabled.

### TitanCSA/Interceptor-Gamepad-Controller
- `WdfFdoInitSetFilter`: [driver/InterceptorDriver/ControllerGip.c:944](https://github.com/TitanCSA/Interceptor-Gamepad-Controller/blob/1146b8541683985345c28c4ecf2fc8000c908ae2/driver/InterceptorDriver/ControllerGip.c#L944). Source presence is verified; build-time product masks determine which families are enabled.
- `IC_PRODUCT_INPUT_MASK`: [driver/InterceptorDriver/Control.c:372](https://github.com/TitanCSA/Interceptor-Gamepad-Controller/blob/1146b8541683985345c28c4ecf2fc8000c908ae2/driver/InterceptorDriver/Control.c#L372). Source presence is verified; build-time product masks determine which families are enabled.
- `Controller_GIP`: [Examples/Console/Controller_01_Invert_Vertical.cpp:111](https://github.com/TitanCSA/Interceptor-Gamepad-Controller/blob/1146b8541683985345c28c4ecf2fc8000c908ae2/Examples/Console/Controller_01_Invert_Vertical.cpp#L111). Source presence is verified; build-time product masks determine which families are enabled.

### TitanCSA/Interception-V2
- `interception_create_context`: [library/interception.c:43](https://github.com/TitanCSA/Interception-V2/blob/04ad866313c6ded542c10ee3e640f78ccee2ebb9/library/interception.c#L43). Source presence is verified; build-time product masks determine which families are enabled.
- `WdfFdoInitSetFilter`: [driver/InterceptorDriver/ControllerGip.c:866](https://github.com/TitanCSA/Interception-V2/blob/04ad866313c6ded542c10ee3e640f78ccee2ebb9/driver/InterceptorDriver/ControllerGip.c#L866). Source presence is verified; build-time product masks determine which families are enabled.

## Runtime status

Executed paths include Vdevice vendor HID, keyboard/mouse, XUSB, DS4 and Xbox One/GIP; both Interceptor keyboard/mouse editions; combined and controller-only controller transformations; ViGEmBus XUSB/DS4; and Brunner vJoy WinMM axes/buttons. See the per-run result pages for valid repetitions, invalid runs and exact receiver APIs. The original DS4 and GIP filter campaigns recorded the WDF-001 guest crash. The signed demo 1.0.6.0 passed separate teardown tests. Source presence and successful latency rows do not certify stability or other device profiles. Windows libvirtualhid driver-backed profiles require a separate license; no runtime score is assigned without it.

## Licenses and build observations

TitanCSA SDK/application files use their published terms; driver evaluation-source restrictions and third-party MIT/MS-PL mappings must be read separately. Repository license metadata alone does not relicense a commercial driver. Signed release downloads are used; driver source was inspected without changing trial behavior.

The Interceptor public SDK needs Windows IOCTL definitions when built with `WIN32_LEAN_AND_MEAN`; the benchmark target explicitly includes `windows.h` and `winioctl.h`. This integration requirement is recorded rather than changing the measured driver. All seven original Interception SDK examples and the new benchmark tools have their own source provenance.
