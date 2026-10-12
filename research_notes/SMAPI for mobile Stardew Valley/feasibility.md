# Engineering Feasibility and Effort: A SMAPI Equivalent for Mobile Stardew Valley (Android first, iOS second), as of Oct 2026

Research notes. Method caveats: the Stardew wiki (stardewvalleywiki.com / wiki.stardewvalley.net) and nexusmods.com could not be fetched directly from this environment (DNS failures), so wiki and Nexus facts come from search-engine snippets of those pages. GitHub pages were fetched directly, but release pages show only day and month (no year). The GitHub API was not available, so issue threads could not be listed in full. NRTnarathip's SMAPILoader shows 0 open issues because support moved to Discord. **So little primary evidence exists for the low-level blockers (Harmony on ARM64, AOT and so on), and those parts lean on inference, which is clearly labelled.** Items marked [Estimate] are mine, not from a source.

## 1. Prior Android SMAPI projects and their reported blockers

### Takeaway
Android SMAPI has been carried by a series of single maintainers: MartyrPher (game 1.4), ZaneYork (1.5), NRTnarathip (1.6) and now the separate JunimoGate. Each handoff came with a long gap after a major game update. The visible blockers are limited mod support, ANR hangs, per-mod Android fixes (SpaceCore, JSON Assets, FarmTypeManager, Content Patcher type conversion) and a 64-bit-only requirement. Public issue trackers are almost empty because support happens on Discord.

### Cited Findings
- Lineage: "originally ported by MartyrPher for Stardew Valley 1.4.x, updated and improved by ZaneYork for Stardew Valley 1.5.x, and then updated and improved by NRTnarathip for Stardew Valley 1.6.x." — [Stardew Valley Wiki: Installing SMAPI on Android (via search snippet)](https://stardewvalleywiki.com/Modding:Installing_SMAPI_on_Android)
- The current Android SMAPI requires game 1.6.15 (another cached copy says 1.6.15.1) from Play Store or Galaxy Store and a 64-bit OS ("32 bit OS are not compatible"). It is described as "still experimental. Some mods don't work yet." — [Stardew Valley Wiki (snippet)](https://stardewvalleywiki.com/Modding:Installing_SMAPI_on_Android); [wiki.stardewvalley.net mirror (snippet)](https://wiki.stardewvalley.net/Modding:Android)
- NRTnarathip/SMAPILoader (the launcher) has 373 stars, 53 forks, 146 commits and GPL-3.0. Its folders are AssemblyStore, LibPatcher, MemoryViewer, SMAPIGameLoader and SharedLibs. It supports 64-bit devices only and the Play Store game only ("does not support modified or pirated game APKs"; "no new game APK needs to be installed"). Features: mod manager, one-click log sharing, one-click SMAPI/launcher update. Save import/export was listed as upcoming. — [GitHub NRTnarathip/SMAPILoader](https://github.com/NRTnarathip/SMAPILoader)
- Installing works like this: install the launcher APK, download a SMAPI zip, then "Install SMAPI From Zip" from the Download folder and "Start Game". — [SMAPILoader wiki: How To Install SMAPI](https://github.com/NRTnarathip/SMAPILoader/wiki/How-To-Install-SMAPI)
- The SMAPI-Android-1.6 fork has 206 stars, 15 forks and 4,639 commits on develop (mostly inherited upstream history). — [GitHub NRTnarathip/SMAPI-Android-1.6](https://github.com/NRTnarathip/SMAPI-Android-1.6)
- Release history, with years inferred and not shown on the page:
  - 25 Nov: 4.1.7.2, the first public build, "not stable". Known issues were application-not-responding (ANR) hangs and limited mod support.
  - 05 Dec: 4.1.7.6 added NPC Map Locations support and fixed textures not loading with SpaceCore/JSON Assets.
  - 24 Dec: 4.1.10.2, the first stable release.
  - 02 Jan: 4.1.10.3 fixed a settings-menu crash with SpaceCore in co-op, fixed Content Patcher string-to-Vector2/3/4 conversion, and disabled Quick Save when FarmTypeManager is installed.
  - 05 Jan: 4.3.2.1 Beta, after which "support is moving to Discord", and zips were distributed there instead of GitHub.
  - — [SMAPI-Android-1.6 releases](https://github.com/NRTnarathip/SMAPI-Android-1.6/releases)
- The game's 1.6 update reached Android/iOS on 4 Nov 2024. — [9to5Google](https://9to5google.com/2024/11/04/stardew-valley-1-6-android-release/). Around late 2024, Reddit users said 1.6 Android was not yet supported. By around April 2025 a working version existed with "basic mods only", with Stardew Valley Expanded working. — [r/SMAPI thread (mirror)](https://redlib.hackliberty.org/r/SMAPI/comments/1gj5i19/smapi_mobile/mdr4265/?context=3)
- ZaneYork fork (1.5 era): 93 stars, 6 forks, 3 open issues, LGPL-3.0. The README has no Android-specific documentation. — [GitHub ZaneYork/SMAPI](https://github.com/ZaneYork/SMAPI). The last 1.5-compatible Android build is archived as 1.5.6.39 (package com.zane.stardewvalley, which implies a repacked or renamed game APK). — [Internet Archive](https://archive.org/details/smapi-stardew-valley-com.zane.stardewvalley)
- In the 1.5.6 era, users reported a white screen and immediate crash after installing the "SMAPI installer and the SMAPI Stardew app", with no log because the game never started. — [Stardew forums thread](https://forums.stardewvalley.net/threads/smapi-mobile-doesnt-launch-stardew-valley-android-1-5-6.26906/)
- JunimoGate is a newer independent launcher (GPL-3.0 with a linking exception, 156 commits, 9 stars, ARM64 APK only, v0.3.1 released 21 Aug). Its modules are App, Android ("private-storage boundaries"), Extraction ("discovers and prepares game inputs"), Rewriter ("applies guarded Android bridge rewrites") and GameHost ("isolated process and SMAPI host contract"). It also has an Android SMAPI fork submodule and a `patches/harmony-android` directory. It builds MonoGame for Android itself and bundles OpenAL Soft and the .NET runtime. It "continues, at the project-goal level, the Android SMAPI launcher work pursued by NRTnarathip/SMAPILoader, but its launcher code is independent." — [GitHub leontismaro/JunimoGate](https://github.com/leontismaro/JunimoGate/tree/main); [Release v0.3.1](https://github.com/leontismaro/JunimoGate/releases/tag/v0.3.1)
- A separate "SpaceCore Android for JunimoGate" port exists (it requires JunimoGate, game 1.6.15+ and SMAPI API 4.3+). This shows that heavy framework mods need dedicated Android forks. — [Nexus mod 50565 (search snippet)](https://www.nexusmods.com/stardewvalley/mods/50565)
- An Android 1.6.15 SMAPI log shows a mod skipped as "assume broken... due to Harmony errors at runtime" through SMAPI's compatibility list. This is weak evidence (a user-uploaded log). — [Scribd log](https://www.scribd.com/document/887971277/SMAPI-Latest)

### Inferences
- [Inference] SMAPILoader's "no new game APK needed / Play Store only" design, its AssemblyStore folder and JunimoGate's "Extraction" and "GameHost" modules point to a launcher architecture: the launcher reads the installed game's APK, extracts managed assemblies (.NET for Android packs these into an assembly store blob, which is why an AssemblyStore tool is needed) and hosts them in its own process and runtime. This replaced ZaneYork's repack-the-APK approach (package `com.zane.stardewvalley`).
- [Inference] The 64-bit-only requirement probably reflects Harmony/MonoMod detour support and current .NET for Android's ARM64 focus.
- [Inference] The observable failure modes (ANR, texture loading with SpaceCore/JSON Assets, Content Patcher type-conversion bugs, a Quick Save conflict with FarmTypeManager) are mostly *game-behaviour divergence* issues, where mobile code differs from PC, rather than raw Harmony crashes. Mobile-only features such as Quick Save have no PC equivalent, so mods can't account for them.

### Gaps
- Full GitHub issue and Discord history for the specific blockers asked about (Harmony ARM64 crashes, Mono AOT/interpreter limits, storage permissions, split APKs, memory) could not be retrieved. The GitHub API was blocked, the SMAPILoader tracker shows 0 open issues, and support is on Discord.
- Release years and SMAPI-Android versions after 4.3.2.1 were not confirmed.

## 2. Platform-specific code in SMAPI and what must be reimplemented for mobile

### Takeaway
SMAPI's core (mod loading, events, the content API, the Cecil-based rewriters and the toolkit) is portable C#. What breaks on mobile is the host: a console window, process launch and install, file paths, the update-check and web UI, keyboard and controller input assumptions, and the PC-specific game API surface the rewriters target. Mobile ports also need a native launcher UI for mod management and log viewing, which upstream SMAPI doesn't have.

### Cited Findings
- SMAPI's stated functions are to load mods, provide APIs and events, rewrite mods for compatibility "so they run on Linux, macOS, and Windows, and in some cases fix code broken by game updates", intercept errors, check for updates, check compatibility and back up saves. — [ZaneYork/SMAPI README (upstream text)](https://github.com/ZaneYork/SMAPI); [NRTnarathip/SMAPI-Android-1.6](https://github.com/NRTnarathip/SMAPI-Android-1.6)
- SMAPI 3.6 "fully rewrites Harmony usage for crossplatform compatibility". This rewriting layer is what an Android port extends. — [Pathoschild Patreon: What's new in SMAPI 3.6](https://www.patreon.com/posts/38441800)
- Mobile launchers reimplemented mod management, log sharing and save handling as Android UI: SMAPILoader has a mod manager and one-click log sharing. JunimoGate has mod import and versioning, groups, profile sharing, save backup and a log viewer in English and Chinese. — [SMAPILoader](https://github.com/NRTnarathip/SMAPILoader); [JunimoGate](https://github.com/leontismaro/JunimoGate/tree/main)
- JunimoGate has a dedicated "Rewriter" module for "guarded Android bridge rewrites". This shows that an extra rewrite layer, mapping PC API calls to the mobile game's API, is needed on top of SMAPI's own rewriters. — [JunimoGate](https://github.com/leontismaro/JunimoGate/tree/main)

### Inferences
- [Estimate, based on knowledge of the upstream SMAPI tree at github.com/Pathoschild/SMAPI, not re-verified this session] Upstream SMAPI splits into SMAPI (core), SMAPI.Toolkit, SMAPI.Installer, SMAPI.Web, bundled mods (ConsoleCommands, SaveBackup) and tests. For mobile:
  - **Discard or replace** the Installer (replaced by the launcher), the console host and colored console logging (replaced by an in-app log viewer and file log), and the terminal-based ConsoleCommands input (needs an in-game or overlay command box).
  - **Keep mostly as-is** the Toolkit (manifest parsing, the update-key logic and the web API client all work over HTTPS), the event system, the content API, translation and the Cecil rewriters.
  - **Must add** an Android rewrite table that maps PC-only members to mobile ones, which is the most game-version-sensitive part. Also needed: hooks for mobile lifecycle (pause and resume, Android killing the process, Quick Save), file paths in app-private storage, and a touch input abstraction.
  - Roughly 70–85% of SMAPI core code is reusable unchanged. Most of the new work is in the launcher, extraction and hosting, and in the per-game-version rewrite and compatibility tables.
- [Inference] Content pipeline: PC 1.6 loads XNB through MonoGame's ContentManager. Mobile assets live inside the APK or OBB, or in a split asset pack, so asset loading must be redirected (JunimoGate's "Extraction" and "private-storage boundaries" modules suggest this).

### Gaps
- No source quantifies how much of the Android fork diverges from upstream (a diff could not be computed without repo access).

## 3. Mod compatibility on mobile ports

### Takeaway
No reliable published percentage exists. The evidence is qualitative: Content Patcher packs and large content mods (SVE) work, but C# framework mods (SpaceCore, JSON Assets, FarmTypeManager, NPC Map Locations) needed specific per-mod fixes or Android-specific forks. Nexus "Android compatible" labels are unreliable because most refer to the 1.5-era port.

### Cited Findings
- "99 percent of mods on Nexus that say they're android compatible mean they're compatible with the 1.5 version (ZaneYork smapi). So unless they specifically say smapi Thailand, it's likely ... incompatible with 1.6+ Android." This is an anecdotal Reddit comment. — [r/SMAPI FAQ thread (mirror)](https://redlib.hackliberty.org/r/SMAPI/comments/1jj1f49/updated_faq_requests)
- As of around April 2025: "basic mods only", and Stardew Valley Expanded working. — [r/SMAPI thread (mirror)](https://redlib.hackliberty.org/r/SMAPI/comments/1gj5i19/smapi_mobile/mdr4265/?context=3)
- Mod-specific fixes appear in the changelogs: SpaceCore, JSON Assets, NPC Map Locations, FarmTypeManager and Content Patcher's vector conversion. — [SMAPI-Android-1.6 releases](https://github.com/NRTnarathip/SMAPI-Android-1.6/releases)
- A dedicated SpaceCore Android port exists for JunimoGate. — [Nexus 50565 (snippet)](https://www.nexusmods.com/stardewvalley/mods/50565)
- The wiki says "Some mods don't work yet." — [Wiki (snippet)](https://stardewvalleywiki.com/Modding:Installing_SMAPI_on_Android)

### Inferences
- [Estimate] Content Patcher-only packs probably work at a high rate (likely 80–95%). The main exceptions are packs that target PC-only UI assets or menus that differ on mobile. C# mods are much lower and bimodal: simple logic and event mods often work, while mods that patch UI or menus, input, rendering or IClickableMenu subclasses often break. The reason is that mobile uses different menu classes, touch input and screen scaling, and has mobile-only features such as Quick Save. A plausible range for the top 100 C# mods is 30–60% working without changes. This is unverified.
- [Inference] Framework mods (SpaceCore, JSON Assets, FTM) are the bottleneck, because dozens of content mods depend on them. A mobile project must budget for maintaining forks of 5–10 framework mods.

### Gaps
- No systematic compatibility list or percentage found. The wiki compatibility page and the Discord lists were not accessible.

## 4. Game update cadence on mobile and breakage

### Takeaway
Mobile reached 1.6 on 4 Nov 2024 and 1.6.15 in December 2024, at the same time as PC. Since then no newer mobile patch was found through 2026, so the mobile target has been very stable. That stability is the main reason the NRTnarathip and JunimoGate ports could mature. Historically the main break was the large engine and version jump (1.5 to 1.6), which took about 1 to 5 months to reach a usable port.

### Cited Findings
- 1.6 arrived on Android, iOS and consoles on 4 Nov 2024. — [9to5Google](https://9to5google.com/2024/11/04/stardew-valley-1-6-android-release/); [CGMagazine](https://www.cgmagonline.com/news/stardew-valley-1-6-patch-mobile-consoles/)
- ConcernedApe: "Stardew Valley 1.6.15 is now available on PC, Android, and iOS". The update was dated around 21 Dec 2024. — [ConcernedApe on X](https://x.com/ConcernedApe/status/1870177483942965637); [TheGamer](https://www.thegamer.com/stardew-valley-patch-1-6-15-live-pc-ios-android/)
- The Mobile Version History page (via snippet) says Android and iOS are equivalent to PC 1.6.15, with experimental multiplayer. A forum user said mobile has been on 1.6.15.0 since December 2024 with no new releases (weak evidence). — [Mobile Version History (snippet)](https://stardewvalleywiki.com/Mobile_Version_History); [Stardew forums](https://forums.stardewvalley.net/threads/update-1-6-15-0-released-today.43813/)
- Port timeline: the first public Android SMAPI for 1.6 came on 25 Nov (about 3 weeks after mobile 1.6), the first stable build on 24 Dec (about 7 weeks), and broader usability around April 2025 per Reddit. — [SMAPI-Android-1.6 releases](https://github.com/NRTnarathip/SMAPI-Android-1.6/releases); [r/SMAPI](https://redlib.hackliberty.org/r/SMAPI/comments/1gj5i19/smapi_mobile/mdr4265/?context=3)
- Android SMAPI requires 1.6.15 or 1.6.15.1, which suggests a small mobile hotfix (1.6.15.1) also broke or required an update. — [Wiki (snippet)](https://stardewvalleywiki.com/Modding:Installing_SMAPI_on_Android)

### Inferences
- [Inference] The 1.5 to 1.6 transition broke the ZaneYork port completely. A new maintainer was needed, and continuity between eras was poor. This is the real maintenance risk: one maintainer leaving equals the project dying.
- [Estimate] Minor mobile patches (1.6.x hotfixes) cost about 1–5 dev-days each: refreshing assembly extraction, re-verifying the rewrite tables and re-testing framework mods. A major update (a hypothetical 1.7, or a .NET or MonoGame runtime change in the mobile build) costs about 1–3 person-months. If ConcernedApe resumes frequent patches, one dev can keep up for minor patches but not for major ones without community help.
- [Inference] Play Store auto-updates are a structural hazard. A launcher-hosted approach breaks the moment the user's installed game updates, unless it pins or caches the assemblies.

### Gaps
- Exact 1.6.15.1 mobile date and any 2025–2026 mobile patch not confirmed. The wiki was inaccessible.

## 5. Architecture options ranked

### Takeaway
Ranking for Android: (b) launcher hosting the game's assemblies is first, the proven current approach. (d) a Content-Patcher-only loader is second as a low-risk MVP. (a) APK repack is third: it worked in the 1.4 and 1.5 eras but is fragile and legally greyer. (c) Box64/Wine is last. For iOS, (e) is the only route, and it is severely constrained.

### Cited Findings
- (b) is what SMAPILoader ("no new game APK needs to be installed", Play Store install required) and JunimoGate (Extraction, GameHost "isolated process", self-built MonoGame Android and .NET runtime) do. — [SMAPILoader](https://github.com/NRTnarathip/SMAPILoader); [JunimoGate](https://github.com/leontismaro/JunimoGate/tree/main)
- (a) is what the earlier ZaneYork-era builds did (a separate package `com.zane.stardewvalley`, installed through an "SMAPI installer" app). — [Internet Archive](https://archive.org/details/smapi-stardew-valley-com.zane.stardewvalley); [Stardew forums](https://forums.stardewvalley.net/threads/smapi-mobile-doesnt-launch-stardew-valley-android-1-5-6.26906/)
- Comparable launcher pattern: Geode's Android launcher "launches an unmodified Geometry Dash with modifications", using its TulipHook library with armv7/aarch64 support. — [geode-sdk org](https://github.com/orgs/geode-sdk/repositories)
- Harmony 2.4 (17 Aug, likely 2025) added "full support for arm64 across all operating systems, including Apple Silicon". Later versions: 2.4.2 (MonoMod.Core 1.3.3, .NET 10) and 2.4.3 (MonoMod.Core 1.3.6). Android is not mentioned. — [Harmony releases](https://github.com/pardeike/Harmony/releases)
- A Resonite guide says MonoMod lacks aarch64 Linux support and that "earlier Android and Apple Silicon efforts seem to have gone somewhat stale". Community arm64 MonoMod branches are "use at your own risk". This may predate Harmony 2.4. — [Resonite wiki](https://wiki.resonite.com/Headless_Server_Software/ARM)
- JunimoGate carries `patches/harmony-android`, which implies stock Harmony needs patching on Android. — [JunimoGate](https://github.com/leontismaro/JunimoGate/tree/main)

### Inferences (pros and cons) [Estimates]
- **(b) Launcher plus its own .NET runtime.** Pros: no redistribution of game code, the user owns the game, and it can bundle a runtime (Mono or CoreCLR on Android) where JIT is allowed, so Harmony detours work. Cons: it must extract assemblies from each game version (assembly store format), rebuild native dependencies (MonoGame, OpenAL, which JunimoGate rebuilds itself), and handle the game's native libs, assets and OBB/split APKs. Any Play Store update can break it. Hard parts: making the game's Android Activity and lifecycle run inside the host app, the signature and license (Play licensing) checks, and memory pressure on low-RAM devices. **Best overall.**
- **(d) Content-Patcher-only data loader.** Pros: no code patching, so most of the ARM64, JIT and Harmony risk goes away, and a much smaller surface. Cons: it still needs some injection point to redirect asset loads (so it still requires (a) or (b) on Android unless the game exposes a mods folder, which it doesn't). It covers only content packs and no C# frameworks. It is the most plausible approach for iOS, by translating CP packs into pre-merged asset overrides offline. **A good MVP or fallback.**
- **(a) On-device APK repack.** Pros: simple conceptually, and proven in the 1.4/1.5 eras. Cons: re-signing changes the package signature (it breaks Play updates and Play Games/cloud saves and may fail license checks), split APKs and app bundles complicate repacking, Android 11+ storage scoped access applies, and redistributing modified game binaries carries more legal and ToS exposure. **Deprecated by the community in favour of (b).**
- **(c) PC build via Box64/Wine (or Box64 plus native Linux .NET).** Pros: real PC SMAPI and full mod compatibility in principle, since it is the PC game. Cons: it requires a second (PC) purchase, x86-64 emulation of a JIT runtime is very slow, there is GPU translation overhead, there are no touch controls, it drains the battery, and it is unrealistic for phones. A variant that runs the PC managed assemblies (which are mostly arch-neutral IL) on native ARM64 .NET in Termux or proot with an ARM64 MonoGame/SDL backend is far more plausible. That is effectively option (b) applied to PC assemblies, with PC SMAPI, but it gives no touch UI. **Niche, for enthusiasts.**
- **(e) iOS.** iOS forbids JIT for App Store and normal sideloaded apps (except under a debugger or some EU and alternative-store situations). Harmony and MonoMod need runtime code generation and memory patching, so iOS must use a full-AOT plus interpreter mode (Mono's interpreter) where Harmony detours can't patch AOT-compiled game methods. Options: (1) Content-Patcher-only, (2) offline IL weaving, where the user's game IPA is decrypted, patched on PC with mods baked in, re-signed and sideloaded (AltStore, SideStore, or EU alternative marketplaces), or (3) a JIT enabler (StikDebug or JITStreamer-style), which is fragile and changes with each iOS release. Getting a decrypted IPA is the major legal and practical hurdle. **Very hard. A realistic iOS target is a CP-only or offline-patched build, not runtime Harmony.**

### Gaps
- No primary source found on whether Harmony 2.4 or MonoMod.Core works on Android ARM64 Mono or CoreCLR without patches, beyond JunimoGate's patch directory.
- No source found on any iOS Stardew SMAPI attempt.

## 6. Skills, team and effort estimate; comparable projects

### Takeaway
Every Android SMAPI generation has essentially been built by one person in their spare time, reaching a first public build about 3 weeks after mobile 1.6 and a stable build about 7 weeks after (building on prior-era work). [Estimate] From scratch: about 4–8 person-months for an Android MVP, about 12–24 for broad parity including framework-mod forks, and iOS is an additional 6–12+ with a much lower ceiling.

### Cited Findings
- NRTnarathip: first public 1.6 build on 25 Nov, stable on 24 Dec, then support moved to Discord. The launcher repo has 146 commits. — [SMAPI-Android-1.6 releases](https://github.com/NRTnarathip/SMAPI-Android-1.6/releases); [SMAPILoader](https://github.com/NRTnarathip/SMAPILoader)
- JunimoGate: 156 commits, at v0.3.1 by 21 Aug, ARM64 only, with a separate SpaceCore port. — [JunimoGate](https://github.com/leontismaro/JunimoGate/tree/main); [v0.3.1](https://github.com/leontismaro/JunimoGate/releases/tag/v0.3.1)
- MelonLoader on Android lives in a separate LemonLoader fork (updated July 2026) with an Il2CppInterop fork for ARM64/Android (updated July 2026). The bootstrap was rewritten in Rust and moved to .NET 8 "because of Android". Mainline MelonLoader still lists "Android & Oculus Quest Support (WIP)", which means years of work without reaching mainline parity. — [LemonLoader GitHub org](https://github.com/orgs/LemonLoader/repositories); [LemonLoader releases](https://github.com/LemonLoader/MelonLoader/releases); [MelonLoader Thunderstore](https://thunderstore.io/c/cairn/p/LavaGang/MelonLoader/)
- Geode runs a separate android-launcher project and its own hooking library, TulipHook (armv7/aarch64). — [geode-sdk org](https://github.com/orgs/geode-sdk/repositories)

### Inferences [Estimates]
- **Skills:**
  - C# and .NET internals: assembly loading, AppDomain/AssemblyLoadContext, reflection.
  - IL and Mono.Cecil rewriting.
  - Harmony and MonoMod internals: detours, trampolines, W^X memory on ARM64, icache flush.
  - The .NET for Android / Xamarin runtime: Mono embedding, the assembly store format, AOT versus JIT versus interpreter.
  - The Android NDK and JNI: hosting another app's native libs, Activity lifecycle, SAF and scoped storage, split APKs.
  - MonoGame Android backend and OpenAL builds.
  - ARM64 assembly for debugging detour crashes.
  - Android Kotlin/Java UI for the launcher.
  - For iOS: Mono full-AOT and the interpreter, code signing and sideloading tooling.
  - Deep knowledge of Stardew's mobile code paths (menus and input) to write rewrite tables and fix framework mods.
- **Team:** 1 core runtime engineer (Mono, Harmony, NDK) plus 1 Android/launcher UI developer, plus 0.5 of a mod-compat engineer who maintains framework-mod forks and the compat list. One exceptional engineer can do the MVP alone, as the evidence shows, but bus-factor risk is high.
- **Phases (from scratch, Android):**
  1. Spike: extract the assemblies, boot the unmodified game in the host app with its own runtime. About 1–2 person-months (PM).
  2. Harmony and MonoMod working on ARM64 in that runtime, with SMAPI core booting and events firing. About 1–2 PM.
  3. Android rewrite and bridge tables, content and asset redirection, a log viewer, a basic mod manager: the MVP, which runs CP packs and simple C# mods. About 1.5–3 PM. **MVP total: about 4–8 PM.**
  4. Framework-mod compatibility (SpaceCore, JA, FTM, GMCM, CP edge cases), touch UI for command and config, save import and export, low-RAM tuning, broad device testing. About 6–12 PM. **Parity total: about 12–24 PM.**
  5. Steady-state maintenance: about 0.2–0.4 FTE while the game is frozen at 1.6.15, rising to 1–3 PM per major game update.
- **Starting from the existing GPL/LGPL forks** (SMAPILoader, JunimoGate, SMAPI-Android-1.6) would cut the MVP to about 1–2 PM.
- **iOS:** Phase 0 is to decide JIT-free versus JIT-enabler. A CP-only or offline pre-patch prototype takes about 3–6 PM. A runtime-Harmony approach on iOS is likely not shippable to normal users (about 6–12+ PM with fragile results).

### Gaps
- No public effort data (hours or people) from any of the Android SMAPI maintainers. No published Pojav Launcher timeline was retrieved this session, and no Geode Android timeline was retrieved.
- Licensing and ToS: ConcernedApe's stance on mobile modding, and Play licensing checks, were not researched in this session.
