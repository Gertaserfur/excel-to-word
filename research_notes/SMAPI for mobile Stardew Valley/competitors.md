# Competitive Landscape: Mobile Stardew Valley Mod Loaders and Analogous Mobile Mod Loaders (as of Oct 2026)

Research date: 2026-10-12. Environment note: the agent proxy blocked direct fetches of stardewvalleywiki.com, wiki.stardewvalley.net, nexusmods.com and forums.stardewvalley.net, and the GitHub API was blocked for these repos. GitHub HTML pages could be fetched. Nexus/wiki/forum facts below come from search-engine snippets, so they are second-hand and less reliable than the GitHub data.

## Competitor matrix (summary)

| Tool | Approach | Platform | Game version | Mod compatibility | Install method | Monetization | Popularity metrics | Weaknesses |
|---|---|---|---|---|---|---|---|---|
| **SMAPI Launcher / SMAPILoader (NRTnarathip)** + **SMAPI for Android** (Nexus mod 44436) | Patches the official Android game. Ships a launcher APK plus an Android fork of SMAPI. | Android, 64-bit only | Official mobile 1.6.15.1+ (Play Store; the wiki also lists Galaxy Store). Launcher v1.1.7 fixes a crash on 1.6.15.3. | "Most" SMAPI mods and content packs. The wiki calls it experimental and says some mods don't work. Android SMAPI 4.3.2.x is behind PC SMAPI. | Sideload the launcher APK from GitHub, then "Install SMAPI From Zip" with the zip from Nexus | Free, open source (SMAPI fork) | SMAPILoader: 373 stars, 53 forks. SMAPI-Android-1.6 fork: 206 stars, 15 forks. Nexus: about 1,934 endorsements; download counts didn't load. Discord: "SMAPI Thailand". | 64-bit only, Play Store copy only (per README). Breaks on game updates. Lags upstream SMAPI. Single maintainer. Latest release seen was v1.1.7 (28 Jun, year not shown). |
| **Cinderbox (Ekyso)** + **SMAPI-For-Cinderbox** | Runs the **PC/desktop** Stardew build natively on Android using a patched MonoGame, Mono/.NET runtime and OpenAL. This is a port of the runtime, not emulation. | Android, arm64/arm32. Android 8–12 support added experimentally in 0.8.0. | Desktop 1.6 (requires owning it on Steam/GOG). SMAPI 4.5.2 port. | Claims "99% mod compatibility". Reports itself as Linux so desktop mods take the right code paths. | Sideload the APK from Nexus (mod 43278), GitHub or Discord. Supply game files yourself, or log in to Steam inside the app (v0.8.0+). | Free (no paid tier found) | Discord about 4.1K+ members. SMAPI fork has 20 stars. Very active: 0.3.0–0.3.4 in Mar, 0.8.0/0.8.1 on 15–16 Aug (2026 inferred). | Requires buying the game a second time on PC. Beta. Legal grey area around pulling Steam files. Known .NET runtime issue with some mods (Walk of Life). |
| **Cinderbox-Companion (ObfuscatedVoid)** | Companion utility | Android | Official Android port and Cinderbox | Manages SMAPI mods. Nexus browsing needs an API key. | Sideload APK | Free | 44 stars | Root needed for auto-sync. Depends on other loaders. |
| **JunimoGate** | Open-source launcher that builds on the work of MartyrPher, ZaneYork and NRTnarathip | Android | Not confirmed | Mod import, version management, save import/export, backups, logs | Not confirmed | Not confirmed | Not found | Found only on a wiki user-talk page. Repo not located, so unverified. |
| **Legacy ports** (MartyrPher's SMAPI-Android-Installer, ZaneYork's SMAPI Android / "SMAPI 13.x") | Patched-APK installers | Android | Pre-1.6 mobile builds (1.4/1.5 era) | Obsolete for 1.6 | Repackage APK | Free | Not measured | Don't work with 1.6. Reddit advice is that unless it says "SMAPI Thailand" it is likely incompatible with 1.6+. |
| **Winlator / GameHub / Box64 (PC .exe under Wine)** | x86 emulation plus Wine | Android with high-end Snapdragon | PC build | Theoretically all SMAPI mods | Emulator app plus the PC game | Free (GameHub is a commercial app) | One report: locked 60 FPS on Snapdragon 8 Elite with GameHub 5.1.0. No SMAPI-specific data. | Heavy and fiddly. Battery drain. Touch controls. Little community traction compared with Cinderbox. |
| **Modded APKs** (HappyMod etc.) | Pre-patched cheat APKs | Android | Varies | Cheats only, not SMAPI mods | Sideload | Ad-supported sites | No reliable figures | Malware/trojan risk, piracy, no updates |
| **iOS** | None | iOS | N/A | None | N/A | N/A | N/A | No SMAPI or loader exists |

## Which Android SMAPI ports/launchers currently exist and work with mobile 1.6.x?

### Takeaway
The established route for the official mobile 1.6.x game is NRTnarathip's open-source SMAPI Launcher (SMAPILoader, 373 stars) plus "SMAPI for Android" from Nexus. It works on 64-bit Android with game version 1.6.15.1 or later. The newer, fast-growing challenger is Cinderbox. It takes a different approach: it runs the desktop build on Android with a near-upstream SMAPI 4.5.2, and its Discord has 4.1K+ members. Older ports (MartyrPher, ZaneYork) are obsolete.

### Cited Findings
- The wiki says Android SMAPI requires Stardew Valley 1.6.15.1 or later from the Play Store or Galaxy Store, and a 64-bit OS. The install flow is to install the SMAPI Launcher APK, then use "Install SMAPI From Zip". There is "a port of SMAPI to Android which supports most SMAPI mods and content packs", but some mods may not be compatible — [Stardew Valley Wiki: Installing SMAPI on Android](https://stardewvalleywiki.com/Modding:Installing_SMAPI_on_Android) (via search snippet)
- The wiki calls the Android launcher still experimental and says some mods don't work yet. It says the Android build is very custom, so official SMAPI isn't compatible — [Nexus forums guide](https://forums.nexusmods.com/topic/13506427-guide-how-to-mod-stardew-valley-on-mobile-devices) / wiki (via search snippet)
- NRTnarathip/SMAPILoader is described as "SMAPI Launcher Android". It has 373 stars and 53 forks. It supports 64-bit devices only and needs the game downloaded from the Play Store. It includes a built-in Mod Manager, and its Discord is "SMAPI Thailand" (discord.com/invite/ETtycvcJjr) — [GitHub NRTnarathip/SMAPILoader](https://github.com/NRTnarathip/SMAPILoader)
- Release history (years not shown on the page):
  - v1.0.7-beta (30 Nov): 32-bit check
  - v1.0.12-beta (05 Dec): multiplayer
  - 1.1.0 stable (20 Dec): SMAPI 4.1.7.7+
  - 1.1.1 (23 Dec): Share Log
  - 1.1.3 (31 Dec): patches monosgen-2.0.so into the APK
  - 1.1.4 (02 Jan)
  - 1.1.5 (01 Apr): 1.6.15.1+, landscape support
  - 1.1.6 (01 Apr): supports SMAPI-Android zips from Nexus
  - v1.1.7 (28 Jun): fixes crash on 1.6.15.3. This was the latest release on the page.

  Release reactions ranged from 11 to 56 people. Download counts were not visible — [GitHub releases](https://github.com/NRTnarathip/SMAPILoader/releases)
- NRTnarathip/SMAPI-Android-1.6 (a fork of Pathoschild/SMAPI) has 206 stars, 15 forks, 4,639 commits and no releases in the repo — [GitHub](https://github.com/NRTnarathip/SMAPI-Android-1.6)
- The Nexus page "SMAPI for Android" (mod 44436) lists version 4.3.2 (changelog 4.3.2.5) and about 1,934 endorsements. Download counts did not load — [Nexus mod 44436](https://www.nexusmods.com/stardewvalley/mods/44436) (via search snippet)
- The forum identifies "SMAPI for Android by NRTnarathip", with community on the SMAPI Thailand Discord — [Stardew forums: How to mod on Android](https://forums.stardewvalley.net/threads/how-to-mod-on-android.54287/) (via search snippet)
- A 2025 Reddit comment says that unless a build specifically says "SMAPI Thailand", it is likely incompatible with 1.6+ Android modding — [r/SMAPI FAQ (mirror)](https://redlib.hackliberty.org/r/SMAPI/comments/1jj1f49/updated_faq_requests)
- JunimoGate is described as an open-source Android launcher with integrated mod, save and diagnostics management, building on work by MartyrPher, ZaneYork and NRTnarathip. The only source is a wiki user-talk page — [Stardew Wiki User talk](https://www.stardewvalleywiki.com/User_talk:ZVZJDwqI)
- Cinderbox is "Play Desktop SDV on Android". It runs a custom fork of the latest SMAPI with "99% mod compatibility", and you must own Stardew on Steam/GOG — [Nexus mod 43278](https://www.nexusmods.com/stardewvalley/mods/43278) (via search snippet)
- Cinderbox releases (years not shown on the page):
  - 0.3.0 (23 Mar): full rewrite with Material 3, 11 themes, 12 languages, controller navigation, working multiplayer, mod bundles, and resolution scaling from 25% to 100%
  - 0.3.3 (25 Mar): supports mods copied from Stardrop
  - 0.3.4 (27 Mar): Mono runtime 8.0.24
  - 0.8.0 (15 Aug): compiled with .NET 10, initial Android 8–12 support, Steam login, CinderTap, mod updates from SMAPI logs
  - 0.8.1 (16 Aug): latest

  The "Build Dependencies" pre-releases contain a patched MonoGame, Mono runtime, OpenAL Soft, SkiaSharp, zstd and LZ4 for arm64 and arm32. Known issue: a .NET runtime problem with the Walk of Life mod. The repo has 4 open issues — [GitHub Ekyso/Cinderbox releases](https://github.com/Ekyso/Cinderbox/releases/)
- SMAPI-For-Cinderbox is an Android port of SMAPI 4.5.2 (LGPL-3.0, 20 stars, 4,754 commits). It "reports itself as Linux so desktop mods take the right code paths", rewrites desktop mod API calls to mobile facades, redirects asset paths to external storage, and includes no game assets — [GitHub Ekyso/SMAPI-For-Cinderbox](https://github.com/Ekyso/SMAPI-For-Cinderbox)
- The Cinderbox Discord has about 4.1K+ members — [discordhub listing](https://discordhub.net/server/cinderbox); [Discord invite](https://discord.com/invite/cinderbox-1464708507923124264)
- A guide describes Cinderbox as currently available in beta — [vortexgaming.io guide](https://vortexgaming.io/en/postdetail/697278)
- Cinderbox-Companion (44 stars) covers:
  - Steam Cloud save sync with conflict detection
  - game file download from Steam with branch selection
  - a Cinderbox setup wizard
  - a SMAPI mod manager with Nexus browsing (requires an API key)
  - Root, Shizuku, All Files and SAF access modes

  It works with both the official Android port and Cinderbox — [GitHub ObfuscatedVoid/Cinderbox-Companion](https://github.com/ObfuscatedVoid/Cinderbox-Companion)
- Other projects on GitHub mirror the Android SMAPI (e.g. Jakub-Glab/SMAPI-Android-1.6) and point to the NRTnarathip/SMAPILoader wiki install guide — [GitHub Jakub-Glab/SMAPI-Android-1.6](https://github.com/Jakub-Glab/SMAPI-Android-1.6)

### Inferences
- Release-date years are not shown. The NRTnarathip launcher's sequence (Nov → Dec → Jan → Apr → Jun) most likely spans Nov 2024 to Jun 2025. If no release has appeared since v1.1.7 on 28 Jun, the project may have slowed in 2026, while Cinderbox shipped its large 0.8.x update in Aug 2026. Treat both year assignments as unconfirmed.
- The Cinderbox Discord server ID (1464708507923124264) decodes to roughly January 2026 as a Discord snowflake. That points to a young project with fast growth (4.1K+ members).
- The market has split in two:
  - **Official-APK patching (NRTnarathip):** cheap for users, who already own the mobile game. But it runs an older SMAPI fork (4.3.2.x) against a custom mobile codebase, so compatibility is partial.
  - **Desktop-on-Android (Cinderbox):** close to full PC mod compatibility and the latest SMAPI (4.5.2). But the user must own the PC version, and there is legal/ToS friction.
- The gaps a new entrant could fill:
  - iOS
  - reliability across game updates
  - mod discovery and dependency resolution
  - a store-distributed (non-sideloaded) experience

### Gaps
- Download counts were not retrievable for the Nexus SMAPI for Android page (44436) or Cinderbox (43278), because the fetch was blocked and snippets showed "--". GitHub release asset download counts were not visible either.
- The SMAPI Thailand Discord member count was not found.
- I could not confirm whether NRTnarathip has published releases after v1.1.7, or whether it supports the latest mobile patch (any 1.6.15.x/1.6.16 changes in 2026).
- JunimoGate's repo, status and metrics were not verified.
- No first-hand YouTube view counts were collected.

## Alternative approaches: PC Stardew + SMAPI on Android via Winlator / Box64 / Mobox / GameHub / .NET

### Takeaway
Emulating the Windows build (Winlator, GameHub, Box64/Wine) is possible on flagship phones, but there is little evidence that it is used for Stardew modding. Cinderbox has largely made it unnecessary: it runs the desktop build natively on an ARM .NET/Mono + MonoGame stack, which is lighter than x86 emulation.

### Cited Findings
- A self-reported r/EmulationOnAndroid post claims Stardew Valley, previously unplayable on that chip, now runs at a locked 60 FPS with GameHub 5.1.0 on a Snapdragon 8 Elite. It is a single report with no mention of SMAPI — [r/EmulationOnAndroid mirror](https://twt.omada.cafe/r/EmulationOnAndroid/comments/1nlf1i3/gamehub_510_antutu_update_insane_performance/nf73wms/?context=3)
- Cinderbox's stack is a patched MonoGame, Mono runtime 8.0.24 (later compiled with .NET 10) and OpenAL Soft built for arm64/arm32. This is a native port of the runtime, not x86 emulation — [GitHub Ekyso/Cinderbox releases](https://github.com/Ekyso/Cinderbox/releases/)
- The same pattern exists for Terraria. One user ran tModLoader on Android with "an Android app that runs desktop .NET apps", pointed at the GOG Linux build of Terraria, with .tmod files copied from PC — [Lemmy post](https://lemmy.blehiscool.com/post/291750/1086643)

### Inferences
- "Desktop .NET game on an Android .NET runtime" is an emerging general pattern (Cinderbox for Stardew, the .NET launcher used for Terraria/tModLoader). It is likely more efficient than Wine/Box64, because Stardew is a managed C#/MonoGame game.

### Gaps
- I found no Stardew-specific Winlator/Box64 + SMAPI performance threads or tutorial view counts.
- The name of the Android ".NET desktop app runner" used in the Terraria post was not given in the snippet.

## Modded APKs ("mod menu" / cheat APKs from HappyMod, etc.)

### Takeaway
Cheat/"mod menu" APKs for Stardew are common on APK sites, but they are not SMAPI mod loaders. They carry well-documented malware and piracy risks. I found no reliable Stardew-specific prevalence data.

### Cited Findings
- Several HappyMod-named domains are flagged unsafe in URL scans — [MalwareTips scan happymods.net](https://tools.malwaretips.com/url-scan/happymods.net); [MalwareTips happymod.ac](https://tools.malwaretips.com/url-scan/happymod.ac)
- Malicious HappyMod clones distribute cracked APKs that are often flagged for trojans and spyware. User-uploaded mods are "completely unverified". Many modded games use Dynamic Code Loading to evade antivirus scans — [bearvpn.com: Is HappyMod Safe? (2026)](https://bearvpn.com/blog/is-happymod-safe/) (vendor blog, moderate reliability)
- The Android SMAPI guides stress that the Android SMAPI is a different build from Nexus's PC SMAPI, and that the launcher must come from GitHub — [Nexus forums guide](https://forums.nexusmods.com/topic/13506427-guide-how-to-mod-stardew-valley-on-mobile-devices)

### Inferences
- A legitimate tool's main trust challenge is that it looks like these sideloaded APKs. Open source, official Nexus/GitHub distribution and clear "you need your own copy" messaging set legitimate tools apart.

### Gaps
- No download data for Stardew mod APKs on HappyMod/APKPure. No documented malware incidents specific to Stardew.

## Save editing and content swapping (XNB replacement) as pre-SMAPI mobile modding

### Takeaway
I could not verify any current sources in this pass. Historically (from background knowledge, unverified here), mobile players edited save XML files and replaced XNB assets in the game's data folder before Android SMAPI ports existed. The 1.6 Content Patcher era and Android scoped storage have made this less relevant.

### Cited Findings
- One SEO-quality page says Android modding must get past "Scoped Storage" restrictions that recent Android versions introduced — [teck.net page](https://wp03.teck.net/smapi-android-2kqa.html) (low reliability)
- SMAPI-For-Cinderbox redirects asset paths to external storage, which shows that file-access problems are a central engineering concern — [GitHub](https://github.com/Ekyso/SMAPI-For-Cinderbox)
- Cinderbox-Companion offers Root, Shizuku, All Files and SAF access modes to reach game and save files — [GitHub](https://github.com/ObfuscatedVoid/Cinderbox-Companion)

### Gaps
- No primary sources were retrieved on mobile XNB replacement or mobile save editors (wiki and forum fetches were blocked).

## iOS options

### Takeaway
I found no SMAPI or mod loader for iOS Stardew. All sources say iOS is unsupported, which leaves a market gap that Apple's platform restrictions keep closed.

### Cited Findings
- A Steam guide (Jan 2022) lists SMAPI support: PC/Mac full, Android partial, iOS none — [Steam community discussion](https://steamcommunity.com/app/413150/discussions/0/3192490350131102805)
- Forum replies blame Apple's install restrictions. A homebrew iOS port "would take quite a while to build, with no guarantee of 100% success" — [Stardew forums: SMAPI for iOS devices?](https://forums.stardewvalley.net/threads/smapi-for-ios-devices.11309); [Will mods ever come to iOS](https://forums.stardewvalley.net/threads/will-mods-ever-come-to-ios.2772/latest)
- The Nexus mobile guide says, "At the moment, mods only work on Android devices" — [Nexus forums guide](https://forums.nexusmods.com/topic/13506427-guide-how-to-mod-stardew-valley-on-mobile-devices)

### Inferences
- An iOS route would most plausibly need EU alternative marketplaces (DMA) or sideloading via AltStore/TrollStore-style tools. iOS also restricts JIT, which matters for Mono-based runtime patching. No sources confirm anyone is attempting it.

### Gaps
- No 2025–2026 sources on iOS attempts, EU alt-store options, or jailbreak tweaks for Stardew.

## Analogous mobile mod loaders: lessons

### Takeaway
Two models have worked on mobile:
- **First-party, platform-sanctioned and monetized:** Minecraft Bedrock add-ons and Marketplace, available on iOS too.
- **Community "launcher that runs an unmodified store copy and injects the loader":** Geode for Geometry Dash on Android, and Starlight for Among Us.

Generic Unity loaders on Android (LemonLoader/MelonLoader) have stalled, and PC-centric mod ecosystems (Town of Us, tModLoader) mostly haven't reached mobile officially.

### Cited Findings
- **Minecraft Bedrock:** add-ons run on every Bedrock platform, including iOS and Android. Marketplace items cost Minecoins, e.g. 310 Minecoins (about $1.55) to 490 Minecoins (about $2.45). Recent items require 1.21.120+. One add-on has 3.5/5 from 2,594 reviews — [minecraftpal Marketplace listing](https://www.minecraftpal.com/marketplace/item/da11d052-dfa7-46e0-b212-3ddd6db42bfd/adventurecraft-add-on); [creativemode.net 2026 add-ons guide](https://creativemode.net/blog/minecraft-bedrock-addons-how-to-create-powerful-add-ons-in-2026-no-code)
- **Geode (Geometry Dash):** the geode-sdk/android-launcher repo (BSL-1.0, 106 stars, 59 forks, 20 open issues) "launches an unmodified Geometry Dash with modifications", meaning a vanilla copy with the Geode loader added. It supports `geode-launcher://` deep links, including a safe-mode launch. The repo was reported as last updated 16 Feb 2026 — [GitHub geode-sdk/android-launcher](https://github.com/geode-sdk/android-launcher); last-update date per search snippet
- **LemonLoader (MelonLoader for Android/Quest):** the latest release is 0.6.5.1 and is installer-only. "Core LemonLoader development is still in the works, albeit slowly." On-device installs don't back up game data or OBBs. Official MelonLoader (v0.7.3) release notes list only desktop changes — [GitHub LemonLoader releases](https://github.com/LemonLoader/MelonLoader/releases); [LavaGang MelonLoader releases](https://github.com/LavaGang/MelonLoader/releases)
- An itch.io comment says MelonLoader testing found Android support very limited — [itch.io thread](https://itch.io/t/3625813/melon-loader-android)
- **Among Us:** most mods (e.g. Town of Us) are PC-only, and converting them to mobile is not possible due to the limits of the mobile format — [TouchTapPlay](https://www.touchtapplay.com/can-i-install-mods-in-among-us-mobile-ios-and-android-answered/); [criticalhits Town of Us guide](https://criticalhits.com.br/games/among-us-como-baixar-instalar-e-jogar-o-mod-town-of-us/)
- **Starlight (Among Us):** an Android mod manager/launcher with custom roles and game modes that requires the official Among Us app. Version 1.6.1 is listed on FileHippo (third-party listing) — [FileHippo Starlight](https://filehippo.com/android/download_starlight-among-us-mods/)
- **Terraria:** no official tModLoader on mobile. The workaround runs the desktop GOG Linux build plus tModLoader through an Android .NET app runner — [Lemmy post](https://lemmy.blehiscool.com/post/291750/1086643)
- Search results for "tModLoader APK" and "Among Us mod menu Android" are dominated by SEO spam and fake pages — [example spam page](https://canadianafund.gc.ca/?p=17244)

### Inferences
- **Lessons for a Stardew mobile loader:**
  1. Launch the user's legitimately installed store copy without redistributing the game. Geode, Starlight and NRTnarathip all do this, and it reduces legal friction.
  2. Give it a recovery/safe-mode path. Geode's deep links are an example.
  3. Spam and fake APKs crowd out search results, so trusted distribution (GitHub, Nexus) and brand recognition matter.
  4. Generic engine loaders (LemonLoader) stall without a dedicated maintainer, while game-specific loaders with an active community (Geode, SMAPI ports) survive.
  5. The only mobile modding with iOS reach is first-party (Minecraft). Third-party loaders are Android-only.
  6. Monetization is almost entirely absent in community loaders: they are free and open source, supported by Discord and donations. Only first-party systems (Minecraft Marketplace) earn money.
- Legal friction: Cinderbox's Steam login and file download, and APK patching, rely on the user owning the game. ConcernedApe has not been documented as acting against Android SMAPI (no source found either way).

### Gaps
- Geode's total Android downloads, Discord size and release dates were not retrieved. LemonLoader star counts were not retrieved.
- Starlight's developer site, popularity and iOS status were not verified.
- No sources were found on takedowns or legal actions against mobile loaders.
