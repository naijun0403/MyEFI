# MyEFI
[![MacOS version](https://img.shields.io/badge/Tahoe-26.1-informational.svg)](https://www.apple.com/macos)
[![OpenCore version](https://img.shields.io/badge/OpenCore-1.0.8-informational.svg)](https://github.com/acidanthera/OpenCorePkg)

## Disclaimer
Use at your own risk. I'm not responsible if your equipment explodes.

## How to build
The SMBIOS model name is specified, but things like the detailed serial number are not committed with it.

However, you can specify these yourself and build them.

For a fresh checkout, copy `secret-properties.example.json` to
`secret-properties.json`, fill in your existing SMBIOS identity, and run
```sh
python build.py
```

`secret-properties.json` is local and ignored by Git. Keep its existing values
when updating this EFI. The build script fills the config in place, so run it on
a deployment copy to keep the repository's SMBIOS placeholders intact.

## OpenCore Version
OpenCore 1.0.8 RELEASE

## Currently Support macOS Version
macOS Tahoe 26.1 x86_64

## My Hardware Spec
```
Motherboard: GIGABYTE Z790 AORUS ELITE X WIFI7
CPU: i7-12700K
GPU: AMD Radeon RX 6600 XT
RAM: DDR5 32GB
```

## Dependency update (2026-11-04)

OpenCore, `BOOTx64.efi`, all five bundled OpenCore drivers, and all fifteen
bundled tools come from the same official 1.0.8 RELEASE archive. All eight
`UEFI/Drivers` entries include the new `HideVerbose` setting. The three picker
themes also include the new `OpticalDrive.icns` icon.

| Kext | Previous bundle version | Updated release |
| --- | --- | --- |
| Lilu | 1.7.1 | 1.7.2 |
| VirtualSMC, SMCProcessor, SMCSuperIO | 1.3.7 | 1.3.8 |
| WhateverGreen | 1.7.1d7 (laobamac fork) | 1.7.1 (official Acidanthera) |
| AppleALC | 1.9.6 | 1.9.8 |
| AirportBrcmFixup | 2.2.0 | 2.2.1 |
| BlueToolFixup | 2.7.1 | 2.7.2 |
| AppleIGC | 1.5d1 | v1.9 |
| LucyRTL8125Ethernet | 1.2.2 | v1.2.4 |
| RealtekRTL8111 | 2.5.0 | v3.0.0 |
| AtherosE2200Ethernet | 2.2.2 | v2.4.0 |
| SMCRadeonSensors (not enabled) | 2.3.0 | 2.4.0 |

Release names can differ from internal build versions: the downloaded AppleIGC
v1.9 bundle reports `1.9d2`, Lucy v1.2.4 reports `1.2.400`, and Realtek v3.0.0
reports `3.0.4`. The bundles are copied intact from upstream releases.

CPUFriend 1.3.0, RestrictEvents 1.1.6, NVMeFix 1.1.3, IntelMausi 1.0.8,
USBToolBox 1.2.0, CpuTopologyRebuild 2.0.2, and RadeonSensor/SMCRadeonGPU 0.3.3
already match their latest stable releases. AMFIPass 1.4.1 and both legacy Wi-Fi
bundles match the OCLP 2.5.1 payloads byte for byte. IOSkywalkFamily's distribution
is named v1.2.0 while its internal bundle version remains 1.0.

The existing IntelBluetoothFirmware/IntelBTPatcher 2.5.0 builds are retained;
upstream's latest published stable release is older (2.4.0). The existing
`AirportItlwm_Sequoia.kext` is also retained because upstream's 2.3.0 stable
AirportItlwm releases target Sonoma or earlier, not Sequoia. CPUFriendDataProvider,
UTBMap, and the unused legacy USB injectors are preserved.

Release URLs, archive SHA-256 checksums, installed versions, and retained-build
exceptions are recorded in [update-manifest.json](update-manifest.json).

## RX 6600 XT and OBS

The graphics configuration uses `MacPro7,1`, `agdpmod=pikera`, and `-wegnoigpu`.
These are consistent with the RX 6600 XT and the unsupported UHD 770 integrated
GPU in the i7-12700K. No GPU device-ID spoof or acceleration-disabling boot
argument is configured. The GPU boot arguments and SMBIOS remain as configured.

WhateverGreen now uses the official release together with Lilu 1.7.2. Lilu
1.7.2 fixes the Tahoe AMDSupport lockups that motivated the previous custom
WhateverGreen build; see the [Lilu release](https://github.com/acidanthera/Lilu/releases/tag/1.7.2)
and the [original workaround discussion](https://github.com/acidanthera/WhateverGreen/pull/126).

The local diagnostic session on 2026-11-04 was running **macOS Sequoia 15.8.2
(24H232), Intel x86_64, and OBS 33.0.1**, although this repository targets Tahoe.
System Information reported the RX 6600 XT with 8 GB VRAM and Metal 3 support.
OBS initialized its AMD OpenGL renderer successfully and enumerated H.264/HEVC
hardware encoders. This confirms renderer initialization and encoder discovery,
not a completed recording test.

OBS logged `The stream is nil`; the system's `replayd` service also logged
`SLContentStreamCreate: Failed to create content stream` and CoreGraphics error
1003. OBS 33.0.1 requests the `64RGBAHalf` ScreenCaptureKit pixel format on
macOS 15+, including Intel systems. The OBS developers identify this as an Intel
regression in [PR #14124](https://github.com/obsproject/obs-studio/pull/14124): that
format is only available on Apple Silicon. The fix was still open on the review
date. This closely matches the observed failure; the user subsequently confirmed
that OBS works after the 32.0.4 workaround below.

For the current workaround:

1. Back up OBS profiles and scene collections, then use the official
   [OBS 32.0.4 macOS Intel build](https://github.com/obsproject/obs-studio/releases/tag/32.0.4)
   until a release including PR #14124 is available. Its source predates the
   `64RGBAHalf` change and uses the previous capture format. The initially
   suggested 32.2.2 build also crashed on this machine; see the follow-up below.
2. Add or edit a **macOS Screen Capture** source. For the whole desktop, select
   **Display Capture** and explicitly choose the connected monitor. The saved
   source inspected here used Application Capture; earlier logs also referenced
   invalid window/display IDs. Those messages can occur when the selected
   target is missing and should be checked separately.
3. Verify **OBS Studio > Review App Permissions > Screen Recording**. Permission
   was already granted in the inspected logs; resetting all privacy permissions
   is not part of this EFI update.

See the official [capture source](https://obsproject.com/kb/macos-screen-capture-source)
and [permissions](https://obsproject.com/kb/macos-permissions-guide) guides.

The follow-up on the same day found three OBS 32.2.2 crash reports with the same
main-thread stack: `QWidget::setCursor` -> `QImage::toCGImage` -> `CGImageCreate`
-> `CGColorSpaceGetType`. This matches the Qt 6.11.1 color-space lifetime bug
[QTBUG-147602](https://bugreports.qt.io/browse/QTBUG-147602) and the OBS
[startup-crash report #14061](https://github.com/obsproject/obs-studio/issues/14061).
It occurred in both normal and safe mode, before scene loading. The app's
signature verified successfully, and no external OBS plugins were installed.

The official OBS 32.0.4 Intel installer was checked against GitHub's published
SHA-256 digest and its app signature verified. The existing app and OBS settings
were backed up locally before installation. With its bundled Qt 6.8.3, OBS
started in normal mode, loaded the existing scene collection and capture source,
and remained running through the startup check without a new crash report.
The user confirmed that OBS works after this replacement. Long-session stability
has not been measured.

## Validation and installation

The existing `build.py` flow was exercised in a temporary directory using
synthetic identity values. The resulting config passed the OpenCore **1.0.8**
`ocvalidate` with no issues. All plist files parse, configured kext/driver/ACPI
paths exist, enabled kext dependencies precede their consumers, configured kext
executables include x86_64, and EFI binaries have x64 PE headers.

The committed config still contains SMBIOS placeholders. Direct `ocvalidate`
on that template will report an invalid SystemUUID until `build.py` fills it in.
Populate `secret-properties.json` with your existing identity, build a deployment
copy, and validate that copy with the validator from the 1.0.8 archive. Back up
the working EFI and test the complete updated EFI from a USB drive before
replacing the boot drive's EFI. A subsequent running-system check confirmed that
the updated Lilu 1.7.2, official WhateverGreen 1.7.1, AirportBrcmFixup 2.2.1, and
AppleIGC 1.9d2 are loaded on Sequoia 15.8.2. Intermittent boot-time display loss
predates this update and remains under investigation.

## Intermittent boot-time display loss (2026-11-04)

The reported failure occurs after macOS finishes booting: both monitors show
**No Signal**, and restarting restores output. Its cause is not yet confirmed.
The working system currently uses two DisplayPort displays, a 2560x1440 Odyssey
G52A at approximately 164 Hz and a 1920x1080 P27FBB-RGGL at 165 Hz, both with
30-bit framebuffers. A 30-bit framebuffer does not establish the physical link's
bit depth or prove that HDR is enabled.

Kernel logs contain repeated `psp_hdcp_services: failed` / `Failed HDCP: status 4`
messages. They also occur during working sessions, so they do not establish the
cause of the blank boots. The available OpenCore logs end at
`EXITBS:START`, when control passes to macOS; that endpoint alone is not evidence
of a bootloader hang.

Start with tests that distinguish display-link negotiation from GPU startup:

1. At the next failure, power-cycle a monitor or reconnect its DisplayPort cable
   before restarting the computer. Recovery without a computer restart would
   support a link/hot-plug problem. Record whether both outputs recover.
2. Test several boots with one monitor at 60 Hz, temporarily disabling Adaptive
   Sync/FreeSync and HDR if enabled. Restore one setting at a time to identify
   whether the failure depends on dual displays or the selected display mode.
3. An additional elimination test is to disable `RadeonSensor.kext` and
   `SMCRadeonGPU.kext` together on a separate USB EFI. This removes the optional
   GPU temperature-monitoring pair while retaining Lilu, WhateverGreen, VirtualSMC,
   and graphics acceleration. This test is not a confirmed fix.

The Radeon [connector-priority documentation](https://github.com/acidanthera/WhateverGreen/blob/1.7.1/Manual/FAQ.Radeon.en.md)
describes a possible multi-monitor remedy, but its sense IDs must come from this
card's connector data; PCI paths and connector IDs should not be guessed.

## Remaining configuration improvements

| Priority | Finding | Action |
| --- | --- | --- |
| High | UTBMap declares 25 logical ports on one XHCI controller. The running controller exposes only HS01-HS15; none of SS01-SS09 is instantiated. | Remap the physical USB ports and retain at most 15 logical ports on that controller, including the required internal Bluetooth port. |
| Fixed | NVRAM/Delete contained the patch value `sbvmm,cpuname,pci` instead of the variable name `revpatch`. | Replace the deletion key with `revpatch`, preserving the configured patch value. |
| Conditional | `hibernatemode=3`, `standby=1`, and OpenCore `HibernateMode=Auto` are enabled. | If failures correlate with sleep/hibernate, test an S3-only setup following the sleep guide; the power preferences have not been changed during this audit. |
| Cleanup | Audio `DeviceProperties/layout-id=16` and `alcid=11` disagree; several Ethernet drivers are enabled while AppleIGC is the attached driver. | Confirm the intended audio layout and installed network cards before simplifying these entries. |
| Firmware review | `EnableWriteUnprotector`, `RebuildAppleMemoryMap`, and `SyncRuntimePermissions` are all enabled. | Obtain a DEBUG boot log showing MAT support before revising runtime-memory quirks. |

For USB remapping, count a USB 3 connector's USB 2 and USB 3 companions separately.
The `port-count` property describes the highest port number; merely changing it
to 15 is not a port map. Preserve the physically identified ports needed for
keyboard, mouse, boot media, and internal Bluetooth. USBToolBox explicitly
[does not patch the port limit](https://github.com/USBToolBox/kext/tree/1.2.0).
See the [USB mapping guide](https://dortania.github.io/OpenCore-Post-Install/usb/)
and [sleep guide](https://dortania.github.io/OpenCore-Post-Install/universal/sleep.html).
The USB map issue needs correction independently of the display diagnosis;
there is no evidence yet that it causes the blank screens.
