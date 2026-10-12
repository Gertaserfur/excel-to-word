# History of SMAPI / Mod Loading on Mobile Stardew Valley (2018 – Oct 2026)

Research notes compiled 2026-10-12. Some sites (stardewvalleywiki.com, nexusmods.com, forums.stardewvalley.net) could not be reached directly from the research environment. Where they are cited, the claim comes from search-engine snippets of those pages. GitHub release pages show day and month but often not the year. **Years marked "(inferred)" come from context**, such as the matching SMAPI version, issue dates, or a Unix timestamp in a tag name. They are not shown on the page itself.

## Q1. Mobile launch, porting studio, and codebase divergence (2018 → 1.5 mobile → 1.6 mobile)

### Takeaway
The Secret Police (London) ported the game, and Chucklefish published it. iOS launched 24 Oct 2018 and Android on 13–14 Mar 2019. Both shipped without multiplayer or mods. For years the mobile code was a separate branch that lagged far behind PC. ConcernedApe described the mobile 1.5 release (Jan 2023) as "to some degree, a completely new rewrite." Mobile 1.6 arrived on 4 Nov 2024 alongside the 1.6.9 patch.

### Cited Findings
- **Oct 2018:** Chucklefish announced the iOS version for 24 Oct 2018 at $7.99 with no IAP. The porting studio was "London-based mobile development studio, The Secret Police," which had worked with the creator "for about a year." Chucklefish handled business and marketing. — [Shacknews](https://shacknews.com/article/107791/stardew-valley-crops-up-on-ios-in-two-weeks?amphtml=1); [PhoneArena](https://www.phonearena.com/news/Stardew-Valley-mobile-release_id109766); [stardewvalley.net](https://stardewvalley.net/stardew-valley-coming-to-mobile/)
- **Oct 2018:** At launch, iOS cut "multiplayer and mod support." PC saves could be transferred via iTunes. — [Shacknews](https://shacknews.com/article/107791/stardew-valley-crops-up-on-ios-in-two-weeks?amphtml=1); [TechRadar](https://www.techradar.com/news/stardew-valley-is-coming-to-mobile) (said mobile "does not support mods," so modded saves may not transfer cleanly)
- **26 Feb 2019:** The Android release was announced for 14 Mar 2019 on Google Play, with pre-registration opening the same day. — [Android Authority](https://androidauthority.com/stardew-valley-android-912474); [Ubergizmo](https://www.ubergizmo.com/2019/02/stardew-valley-android-release-date)
- **13 Mar 2019:** Android went live a day early. It was the full game up to v1.3 minus multiplayer, ported by The Secret Police. — [Android Police](https://www.androidpolice.com/2019/03/13/stardew-valley-for-android-is-out-a-day-early/); [Android Authority](https://androidauthority.com/stardew-valley-android-912474)
- **2019–2020 mobile build numbering:** Android builds had their own version numbers, separate from PC (e.g. "1.25", "1.31", "1.322", "1.331", then "1.4.4.131", "1.4.5.137", "1.4.5.139"). These appear as requirements in MartyrPher's installer releases. — [MartyrPher releases](https://github.com/MartyrPher/SMAPI-Android-Installer/releases)
- **Dec 2020:** The PC 1.5 update released. Mobile got 1.5 only on **7–9 Jan 2023**, after missing a 2022 target. ConcernedApe: "1.5 mobile is, to some degree, a completely new rewrite of the mobile app," which should allow quicker updates such as 1.6. — [TechCrunch](https://techcrunch.com/2023/01/09/stardew-valley-apps-ios-android-patch-1-5); [TouchArcade](https://toucharcade.com/2023/01/09/stardew-valley-1-5-update-mobile-download-android-ios-iphone/); [Shacknews](https://shacknews.com/article/133641/stardew-valley-15-update-mobile)
- **Jan 2023:** PocketGamer described the 1.5 mobile rollout as a limited "soft launch" for bug testing. Pocket Tactics called it fully live. — [PocketGamer](https://www.pocketgamer.com/stardew-valley/1-5-update-soft-launch/); contrasted with [Pocket Tactics](https://www.pockettactics.com/stardew-valley/mobile-update)
- **Jan 2023:** Pathoschild stated in a GitHub thread that Android 1.5.6 had shipped and uses **Xamarin.Android 12.0**. He had first guessed .NET Framework 4.5, then corrected it. — [ZaneYork issue #246](https://github.com/ZaneYork/SMAPI-Android-Installer/issues/246)
- **19 Mar 2024:** The PC 1.6 update launched. In Apr 2024, ConcernedApe said mobile/console would come "as soon as possible." — [TouchArcade](https://toucharcade.com/2024/04/08/stardew-valley-1-6-update-mobile-console-in-progress-release-date-as-soon-as-possible-concernedape/)
- **4 Nov 2024:** 1.6 reached console and mobile, with 1.6.9 rolling out to all platforms. It was free for owners and available on the Play Store. — [Shacknews](https://shacknews.com/article/141512/stardew-valley-1-6-console-release-date); [9to5Google](https://9to5google.com/2024/03/19/stardew-valley-1-6-android/); [ConcernedApe on X](https://x.com/ConcernedApe/status/1853844270807175428)
- **Dec 2024:** A user forum post says Android and iPhone had been on 1.6.15.0 since December 2024 (user claim, less authoritative). — [SDV forums](https://forums.stardewvalley.net/threads/update-1-6-15-0-released-today.43813/latest)
- **Mar 2026:** A user reported a "Stardew Valley 1.6.15.1 Android update." Another user mentioned 1.6.15.2 on 30 Mar 2026. SMAPILoader v1.1.7 (Jun, likely 2026) patches a crash on 1.6.15.3. — [NRT issue #20](https://github.com/NRTnarathip/SMAPI-Android-1.6/issues/20); [SMAPILoader releases](https://github.com/NRTnarathip/SMAPILoader/releases)

### Inferences
- The early mobile port was a separate code fork, with its own build numbers and Xamarin.Android/MonoGame-on-Android packaging. Every unofficial loader had to re-target each mobile build. The 1.5 rewrite changed assembly layout again (see Q2).
- Starting with 1.6 (Nov 2024), mobile version numbers track PC (1.6.9 → 1.6.15.x). This made it much easier to port current SMAPI (4.x) to Android.

### Gaps
- I did not verify whether The Secret Police also did the 1.5 and 1.6 mobile rewrites, or whether that work moved in-house or to another studio.
- I could not reach a primary source with exact dates for the mobile 1.6.15.1, 1.6.15.2 and 1.6.15.3 builds.

## Q2. ZaneYork and MartyrPher Android SMAPI projects (2019–2026)

### Takeaway
ZaneYork, a Chinese developer, built the first Android SMAPI fork in spring 2019 and offered it upstream. Pathoschild rejected it on 13 Apr 2019. ZaneYork paused development in June 2019. MartyrPher's SMAPI-Android-Installer then became the de facto Android SMAPI from June 2019 to February 2020, covering mobile 1.25 to 1.4.5.139. It worked by repacking and re-signing the game APK. ZaneYork returned in March 2020 with his own installer, which became the dominant tool. It covered mobile 1.4.x (SMAPI 3.7.6.x builds, 2021, inferred), then 1.5.6 (SMAPI 3.18.x builds, Apr–Jul 2023, inferred). He never updated it for mobile 1.6. He was banned from Google Play, and he archived the repo on 23 Apr 2026.

### Cited Findings
**ZaneYork, phase 1 (2019)**
- **Apr 2019:** ZaneYork opened PR #635, "Experimental Android support," against Pathoschild/SMAPI. The commits are by "yangzhi." His approach "needs a Android Application to grab Dlls from Stardew Valley and delegate it." Without root it "should extract Contents from apk file." The commits mention "Android Mod Transportation," an "OnDraw Hook," and bundled re-made versions of ContentPatcher, LookupAnything, UI Info Suite and Json Assets. — [PR #635](https://github.com/Pathoschild/SMAPI/pull/635)
- **9 Apr 2019, Pathoschild:** "This is an interesting approach, but I prefer not changing the game executable or recreating each mod." He asked whether a launcher approach could work instead. — [PR #635](https://github.com/Pathoschild/SMAPI/pull/635)
- **12 Apr 2019, Pathoschild:** "It's still experimental and unofficial though, so expect bugs, issues, and most mods outright not working yet." — [PR #635](https://github.com/Pathoschild/SMAPI/pull/635)
- **13 Apr 2019:** Pathoschild closed the PR without merging. His reasons: it "removes support for players on Linux/Mac/Windows and removes most of the internal code," and bundled mods had "incompatible licenses or are fully copyrighted." He added: "Feel free to ... maintain a SMAPI fork for Android!" — [PR #635](https://github.com/Pathoschild/SMAPI/pull/635)
- **21 Sep 2019, Pathoschild:** ZaneYork "stopped updating their fork and support in June," so MartyrPher's fork "appeared to be the de facto Android version." — [Pathoschild issue #632](https://github.com/Pathoschild/SMAPI/issues/632)
- The ZaneYork/SMAPI fork on GitHub now shows 93 stars and 6 forks. Its README is upstream-style and does not mention Android. — [ZaneYork/SMAPI](https://github.com/ZaneYork/SMAPI)

**MartyrPher SMAPI-Android-Installer (Jun 2019 – Feb 2020)**
- **How it works:** The installer pulls the game APK from the device, creates the needed directories, adds SMAPI files to the APK, signs it (v1 scheme only, using Google's debug keystore and apksigner), and installs the modified app. Users then launch a separate "SMAPI Stardew Valley" icon, and mods go in `StardewValley/Mods`. The author reported about 21 s on a Galaxy S10 and about 1 min 13 s on a Galaxy S6. The manual .zip install was removed in v0.8.7 because it "causes more harm than good." — [MartyrPher README](https://github.com/MartyrPher/SMAPI-Android-Installer)
- **Release timeline** (years inferred as 2019–2020 from Pathoschild's Sep 2019 comment and the SMAPI 3.2 era):
  - V0.86 pre-release, 24 Jun 2019: game 1.25. First standalone release, with console and Json Assets support.
  - v0.8.7, 2 Jul 2019: game 1.25+. Harmony mods did not work on Android 5.1.1 and below.
  - v0.8.8, 20 Jul 2019: game 1.31. Added MonoMod assemblies for experimental Harmony on old Android.
  - 0.9.0, 11 Aug 2019: game 1.322. Updated the manifest and classes.dex.
  - 0.9.1, 22 Sep 2019: game 1.331, SMAPI 2.11.3.
  - 0.9.2, 27 Nov 2019: game 1.331. Warned that many mods were already 1.4-only.
  - 3.2.0.2, 11 Feb 2020: game 1.4.4.131, SMAPI 3.2.0. First 1.4 build.
  - 3.2.0.3, 17 Feb 2020: game 1.4.5.137.
  - 3.2.0.4, 22 Feb 2020 (final): game 1.4.5.139.
  - Source: [MartyrPher releases](https://github.com/MartyrPher/SMAPI-Android-Installer/releases)
- **Current status:** 162 stars, 39 forks, 65 open issues, no archive notice. The last GitHub activity was around 27 Feb 2020. — [MartyrPher repo](https://github.com/MartyrPher/SMAPI-Android-Installer); [GitHub search listing](https://github.com/search?q=SMAPI+android&type=repositories)

**ZaneYork SMAPI-Android-Installer, phase 2 (2020–2026)**
- **14 Mar 2020:** Pathoschild thanked ZaneYork for "the new Android installer" and asked whether it was a separate fork or a continuation of MartyrPher's. — [issue #632](https://github.com/Pathoschild/SMAPI/issues/632)
- **How it works:** The installer extracts the original game package, generates the SMAPI dependency files, adds SMAPI launch code to the package, then signs it and installs it as a new SMAPI-prefixed app. Later builds use the package/data path `Android/data/com.zane.stardewvally/files/` for Mods. The Chinese README describes the same flow. — [ZaneYork README](https://github.com/ZaneYork/SMAPI-Android-Installer); [v3.18.3.3 release](https://github.com/ZaneYork/SMAPI-Android-Installer/releases/tag/v3.18.3.3)
- **Distribution:** GitHub Releases and Coolapk (a Chinese app store). It was briefly on Google Play, but "Removed from google play and developer account blocked for seemingly no reason." Support ran through a QQ group. — [ZaneYork README](https://github.com/ZaneYork/SMAPI-Android-Installer)
- **Release tags** (years inferred; the page shows only day/month):
  - v3.7.6.5–v3.7.6.10, 29 Jan–5 Apr (likely 2021). v3.7.6.7 notes "Fix backward compatibility with 1.4.5.145," meaning mobile game 1.4.5.145.
  - v3.18.2.2_ALPHA, 11 Apr (likely 2023).
  - v3.18.3.1, 26 Jun (likely 2023).
  - v3.18.3.2, 8 Jul (likely 2023).
  - v3.18.3.3 "Latest," 11 Jul (likely 2023). Notes: improved compatibility and save/load performance, fixed install logic, fixed seasonal content packs and GenericModConfigMenu.
  - The releases page also says "many of mods may not works, dont post issue to request mods compat."
  - Source: [ZaneYork releases](https://github.com/ZaneYork/SMAPI-Android-Installer/releases)
- **Mobile 1.5 transition:**
  - Issue #70: crashes after 1.5, "2 months since SMAPI was updated for android." — [issue #70](https://github.com/ZaneYork/SMAPI-Android-Installer/issues/70)
  - 22 Dec 2022: issue #246 asked about 1.5 support. ZaneYork replied 23 Dec 2022 ("yes, once he has enough time").
  - 8 Jan 2023: ZaneYork said the 1.5 mobile release changed its assembly format "AGAIN." He planned to redirect saves to the original directory and aimed for a release before March 2023.
  - Pathoschild (8 Jan 2023) noted that the team lacked early access to prepare.
  - Source: [issue #246](https://github.com/ZaneYork/SMAPI-Android-Installer/issues/246)
  - Mar 2023: issue #279 asked for 1.5 progress. Apr 2023: issue #302 reported Json Assets, SAAT and SVE not working. — [issue #279](https://github.com/ZaneYork/SMAPI-Android-Installer/issues/279); [issue #302](https://github.com/ZaneYork/SMAPI-Android-Installer/issues/302)
  - Issue #639: SMAPI shuts down on mobile 1.5.6.52. — [issue #639](https://github.com/ZaneYork/SMAPI-Android-Installer/issues/639)
- **1.6 breakage:**
  - Issue #878: mobile 1.6.x users could not use newer mods such as Content Patcher 2.0 without SMAPI 4+. — [issue #878](https://github.com/ZaneYork/SMAPI-Android-Installer/issues/878)
  - 11 Nov 2024: ZaneYork unpinned the 1.5 issue. There are no later maintainer replies. — [issue #246](https://github.com/ZaneYork/SMAPI-Android-Installer/issues/246)
- **Archive:** Archived by the owner on **23 Apr 2026**. At that point: 788 stars, 78 forks, 115 watchers, 492 open issues, LGPL-3.0. No official reason was given. — [ZaneYork repo](https://github.com/ZaneYork/SMAPI-Android-Installer)
- **Conflict:** A GitHub search listing showed "last updated Jul 15, 2025" alongside an "(archived)" label, while the repo page gives the archive date as 23 Apr 2026. "Last updated" probably reflects the last push, not the archive date. — [GitHub search](https://github.com/search?q=SMAPI+android&type=repositories)

### Inferences
- Both early installers repacked and re-signed the APK and installed a second app. That is why users needed to uninstall or migrate data, and why Google Play account and signature issues followed.
- ZaneYork's version scheme appears to be the upstream SMAPI version plus a build suffix (3.7.6.x is based on SMAPI 3.7.6, 3.18.3.x on SMAPI 3.18.3). So Android SMAPI stayed on SMAPI 3.x until late 2024.
- Why it stalled: 1.5 mobile changed the assembly format (Xamarin.Android 12), there was no early access, it was a single developer, and Google Play banned the account. ZaneYork never moved to the 1.6/.NET-based mobile build.

### Gaps
- I could not confirm the exact years of the ZaneYork release tags (the GitHub API was blocked in this environment, and the pages show only day/month).
- I found no statement from ZaneYork on why he archived the repo.
- I did not confirm the Nexus/ModDrop distribution of the ZaneYork-era builds.

## Q3. After mobile 1.5 and 1.6: breakage and new projects (2023–Oct 2026)

### Takeaway
Mobile 1.5 (Jan 2023) broke existing loaders until ZaneYork's 3.18.x builds (Apr–Jul 2023, inferred). Mobile 1.6 (Nov 2024) broke ZaneYork's tool for good. Within weeks, Thai developer NRTnarathip released a new architecture that leaves the APK unpatched: a "SMAPI Launcher" app (SMAPILoader) plus a SMAPI 4.x Android fork (SMAPI-Android-1.6). Both were first released in late Nov 2024 and are still maintained through mid-2026. Another approach appeared in 2026: Ekyso's "Cinderbox" runs the desktop PC game on Android with a SMAPI 4.5.2 fork. Smaller forks and companions (JunimoGate, Cinderbox Companion) also appeared.

### Cited Findings
**NRTnarathip SMAPI-Android-1.6 (SMAPI fork)**
- **Releases** (years inferred):
  - SMAPI 4.1.7.2, 25 Nov 2024: "First version upload, not stable."
  - 4.1.7.6, 5 Dec 2024.
  - 4.1.10.2, 24 Dec 2024: "First release stable version."
  - 4.1.10.3, 2 Jan 2025: fixed a SpaceCore co-op menu crash and a Content Patcher conversion bug.
  - SMAPI-4.3.2.1 Beta, 5 Jan 2026. The tag's Unix timestamp 1762834431 is 11 Nov 2025 UTC, so the build dates from Nov 2025 and the release was published 5 Jan 2026. Its notes say to download the zip from the Discord "smapi-beta" channel and that GitHub issues are no longer supported.
  - Source: [releases](https://github.com/NRTnarathip/SMAPI-Android-1.6/releases); [4.1.10.3](https://github.com/NRTnarathip/SMAPI-Android-1.6/releases/tag/4.1.10.3)
- **Repo stats at time of research:** 206 stars, 15 forks, fork of Pathoschild/SMAPI, "SMAPI Android & Install Guide." — [repo](https://github.com/NRTnarathip/SMAPI-Android-1.6)
- **Issue #20** (opened 23 Mar 2026): the "Stardew Valley 1.6.15.1 Android update" was incompatible with SMAPI 4.3.2.1 beta and crashed on launch. The maintainer promised a fix and closed the issue as completed on 27 Jun 2026. — [issue #20](https://github.com/NRTnarathip/SMAPI-Android-1.6/issues/20)
- A Nexus Mods page, "SMAPI for Android" (mod 44436), distributes the Android SMAPI, showing v4.3.2 with a 4.3.2.5 changelog entry ("disable Save Emergency popup on title menu"). This comes from a search snippet; I could not load the page, and the dates were inconsistent. — [Nexus 44436](https://www.nexusmods.com/stardewvalley/mods/44436)

**NRTnarathip SMAPILoader ("SMAPI Launcher Android")**
- **Features:** Mod Manager, one-click log sharing, one-click updates of SMAPI and the launcher, "No need to install a new game APK," 64-bit only. The game must be downloaded from the Play Store, and modified or pirated APKs are not supported. The README credits Eky-Team for guides on patching .NET 8 to .NET 9 and thanks Pathoschild for support and guidance. It links the "SMAPI Thailand" Discord. GPL-3.0, 373 stars, 53 forks. — [SMAPILoader](https://github.com/NRTnarathip/SMAPILoader)
- **Install flow:** Install the launcher APK, download the `SMAPI.4.x.x-(xxxx).zip` from the SMAPI-Android-1.6 releases, use "Install SMAPI From Zip," then "Start Game." The wiki page was last edited 24 Dec 2024. — [wiki](https://github.com/NRTnarathip/SMAPILoader/wiki/How-To-Install-SMAPI)
- **Releases** (years inferred):
  - 1.0.7-beta, 30 Nov 2024: 32-bit device check.
  - 1.0.12-beta, 5 Dec 2024: multiplayer support.
  - 1.1.0 stable, 20 Dec 2024: SMAPI 4.1.7.7+, dark mode.
  - 1.1.1, 23 Dec 2024: Share Log.
  - 1.1.2, 29 Dec 2024.
  - 1.1.3, 31 Dec 2024: patches `monosgen-2.0.so` into the APK.
  - 1.1.4, 2 Jan 2025.
  - 1.1.5, 1 Apr (likely 2026): supports game 1.6.15.1+.
  - 1.1.6, 1 Apr (likely 2026): accepts SMAPI-Android zips from Nexus Mods.
  - 1.1.7 "Latest," 28 Jun (likely 2026): fixes a crash on game 1.6.15.3.
  - Source: [SMAPILoader releases](https://github.com/NRTnarathip/SMAPILoader/releases); [1.1.5](https://github.com/NRTnarathip/SMAPILoader/releases/tag/1.1.5)
- **Related tool:** NRTnarathip/SMAPI-AndroidTool, a "Command-line tool for Android SMAPI developers" (updated 24 Jun 2025). — [GitHub search](https://github.com/search?q=SMAPI+android&type=repositories)

**Other 2023–2026 projects (from a GitHub search listing, 24 results)**
- stardewrocks/android-compatible-mods, a list of mods that work or don't with Android SMAPI. 5 stars, updated 20 Oct 2023.
- leontismaro/JunimoGate, an "Android SMAPI launcher" (Chinese/English). 9 stars, updated 21 Aug (2026 implied by the listing). Paired with the fork leontismaro/JunimoGate-SMAPI.
- 0p41xxx/SMAPILoader-Android-FFA and 0p41xxx/SMAPILoader-personal, forks of SMAPILoader with 0 stars.
- ObfuscatedVoid/Cinderbox-Companion, 44 stars, "updated yesterday" (around 11 Oct 2026). A mirror exists at cang-yang/Cinderbox-Companion.
- Source: [GitHub search](https://github.com/search?q=SMAPI+android&type=repositories); [cang-yang mirror](https://github.com/cang-yang/Cinderbox-Companion)

**Cinderbox (Ekyso), 2026: the desktop game on Android**
- Ekyso/Cinderbox is "A native launcher for Desktop Stardew Valley for Android." Per its Nexus page: "custom fork of the latest SMAPI," "99% mod compatibility," and you "MUST own Stardew Valley on Steam/GOG." Since v0.8.0 it can log in to Steam and download the game files. Latest release 0.8.1, around 16 Aug 2026. The Nexus page (mod 43278) is labelled "Cinderbox - Play Desktop SDV on Android." — [Cinderbox GitHub](https://github.com/Ekyso/Cinderbox); [Cinderbox releases](https://github.com/Ekyso/Cinderbox/releases/); [Nexus 43278](https://www.nexusmods.com/stardewvalley/mods/43278) (via search snippet)
- Ekyso/SMAPI-For-Cinderbox is an "Android port of SMAPI 4.5.2 for use with the Cinderbox launcher." It "Runs upstream PC SMAPI on Android, reporting as Linux so desktop mods use correct code paths," and rewrites desktop mod API calls to mobile facades. 20 stars, LGPL-3.0. A Vortex Gaming guide cites SMAPI 4.5.1 instead. — [SMAPI-For-Cinderbox](https://github.com/Ekyso/SMAPI-For-Cinderbox); [Vortex Gaming guide](https://vortexgaming.io/en/postdetail/697278)
- Cinderbox Companion syncs saves with Steam Cloud (auto-push requires root), downloads game files, has a "SMAPI Setup" feature, and includes a Nexus-backed mod manager. MIT license. — [Cinderbox-Companion](https://github.com/ObfuscatedVoid/Cinderbox-Companion)
- A 2026 YouTube video, "RUN PC SMAPI AND SDV WITH 99% MODS COMPATIBILITY ON ANDROID ... (NOT EMULATOR!!) 2026," promotes this approach. — [YouTube](https://www.youtube.com/watch?v=ZPAxFO0Sw4s)

### Inferences
- The "Eky-Team" credited in the SMAPILoader README for .NET 8 → .NET 9 patching guides is very likely the same Ekyso/Ekysoh behind Cinderbox. This is not verified.
- The ecosystem has split into two models:
  - (a) Mobile-build SMAPI: NRTnarathip's launcher plus fork. It needs a Play Store copy, is tied to mobile build numbers, and breaks on each mobile patch (1.6.15.1 in Mar 2026, 1.6.15.3 around Jun 2026).
  - (b) Desktop-build-on-Android: Cinderbox. It needs a Steam/GOG copy and gets near-full PC mod compatibility.
- Distribution has partly moved from GitHub to Discord and Nexus (NRT's beta says download from Discord, and the 1.1.6 launcher accepts Nexus zips).
- No "SMAPIDroid" project was found under that name.

### Gaps
- I could not get exact years for the SMAPILoader 1.1.5–1.1.7 releases, so 2026 is inferred from issue #20's timeline.
- I could not open the Nexus pages for upload dates and download counts, or the Stardew forums ("How to mod on Android," 1.6 era).
- I found no ModDrop-specific information.
- I did not get the Cinderbox first release date or star count (likely early 2026; its Discord server ID suggests about Jan 2026, but that is unverified).

## Q4. iOS mod loading efforts

### Takeaway
I found no working, documented SMAPI or mod loader for iOS, whether jailbroken or sideloaded, in 2018–2026. Pathoschild's tracker lists iOS as "no current support." Claims of jailbreak-based iOS SMAPI come only from low-quality SEO pages and TikTok.

### Cited Findings
- Pathoschild's platform tracker (opened 23 Mar 2019) lists iOS as "no current support." Android is "unofficial support, many mods compatible." — [issue #632](https://github.com/Pathoschild/SMAPI/issues/632)
- A user reply on the official forum: SMAPI has a port for Android but not iOS, and mods don't work on iOS "even if you jailbreak." Forum users warn that workarounds are "nine times out of ten malicious." I saw this only via search snippet. — [SDV forum "Smapi IOS"](https://forums.stardewvalley.net/threads/smapi-ios.27208/); [SDV forum "Will mods ever come to iOS"](https://forums.stardewvalley.net/threads/will-mods-ever-come-to-ios.2772/)
- An SEO page (kerusso.com mirror) claims a jailbroken device plus SMAPI works. **Unverified and likely spam.** TikTok pages say "You cannot mod iOS." — [kerusso page](https://ftp.kerusso.com/royal-network/stardew-valley-mods-on-ios-a-complete-guide-1764806671); [TikTok](https://www.tiktok.com/discover/how-to-get-stardew-valley-mods-on-ios?lang=en)
- The wiki's Getting Started page lists SMAPI as compatible with "Linux/Mac/Windows and (unofficially) Android." Search snippet only; the site was unreachable. — [SDV wiki](https://stardewvalleywiki.com/Modding:Player_Guide/Getting_Started)

### Inferences
- iOS forbids runtime code loading and APK-style repacking, and the 2018 port is AOT-compiled. Together these probably explain why no loader emerged. This is a technical inference, not a sourced statement.

### Gaps
- I did not search for iOS save-editing or texture-replacement hacks (non-SMAPI) or sideloaded IPA tweaks in detail. I found no reliable source for any of them.

## Q5. Official statements (ConcernedApe, Pathoschild)

### Takeaway
Pathoschild has consistently said, from 2019 to 2025, that SMAPI officially supports only Linux, macOS, Windows and Steam Deck. He won't port to mobile himself, but he helps and documents community ports. He closed ZaneYork's upstream PR in 2019 and points mobile work to "the unofficial port's repo." ConcernedApe has made no mobile-specific mod-support commitment that I could find. On console he said he isn't "opposed" but it may not be "possible, for numerous reasons."

### Cited Findings
- **Pathoschild, 23 Mar 2019** (issue #632): he doesn't plan to port SMAPI to mobile or consoles himself but will help anyone familiar with those platforms. — [issue #632](https://github.com/Pathoschild/SMAPI/issues/632)
- **Pathoschild, 9–13 Apr 2019** (PR #635): he prefers "not changing the game executable or recreating each mod," calls the Android port "experimental and unofficial," and suggests "maintain a SMAPI fork for Android!" — [PR #635](https://github.com/Pathoschild/SMAPI/pull/635)
- **Pathoschild, 7–8 Jan 2023:** he engaged in the ZaneYork tracker about mobile 1.5 internals (Xamarin.Android 12.0) and noted the lack of early access. — [ZaneYork issue #246](https://github.com/ZaneYork/SMAPI-Android-Installer/issues/246)
- **Pathoschild, May–Jul 2025** (issue #632): "pull requests are welcome" for ARM64. "ARM64 won't be officially supported" unless it can be built on x64 or through GitHub CI. Detailed work belongs on the SDV Discord "or the unofficial port's repo." Also, SMAPI no longer needs Harmony after 1.6, and about 6–35% of mods use Harmony. — [issue #632](https://github.com/Pathoschild/SMAPI/issues/632)
- **NRTnarathip's README** thanks Pathoschild "for support and guidance." — [SMAPILoader](https://github.com/NRTnarathip/SMAPILoader)
- **SMAPI's CurseForge page:** Linux/macOS/Windows, and "This page is not for Android," with Android pointed to a separate guide. — [CurseForge](https://www.curseforge.com/stardewvalley/utility/smapi)
- **ConcernedApe on console mods:** "If it was simple to do, I wouldn't be opposed. But I don't think it would be possible, for numerous reasons." Date not captured. — [GamesRadar](https://www.gamesradar.com/games/simulation/stardew-valley-doesnt-have-mod-support-on-console-for-numerous-reasons-says-creator-concernedape-but-hes-not-opposed-to-it-if-its-ever-possible/)

### Inferences
- Pathoschild's stance is "unofficial but tolerated and assisted." It has not changed in seven years.

### Gaps
- I found no direct ConcernedApe quote specifically about mobile mod support, and I could not search X directly. The GamesRadar article date was not captured.

## Q6. Has mobile ever received official mod support or console-style restrictions?

### Takeaway
No. As of Oct 2026, no mobile version has official mod support. Mods were explicitly excluded at the 2018 iOS launch, and every mobile mod loader is third-party. I found no evidence of active anti-mod measures. The breakage comes from version changes and app-store constraints: the Play account ban for ZaneYork's installer, and the requirement for an official Play Store APK.

### Cited Findings
- iOS launched without mod support (Oct 2018). — [Shacknews](https://shacknews.com/article/107791/stardew-valley-crops-up-on-ios-in-two-weeks?amphtml=1)
- Pathoschild's tracker still lists Android as "unofficial" and iOS/consoles as "no current support." — [issue #632](https://github.com/Pathoschild/SMAPI/issues/632)
- ZaneYork's installer was removed from Google Play and his "developer account blocked for seemingly no reason." — [ZaneYork README](https://github.com/ZaneYork/SMAPI-Android-Installer)
- Mobile 1.5 changed the assembly format, mobile 1.6 moved to the modern stack, and 1.6.15.x patches broke SMAPI again in 2026. None of this is documented as intentional anti-modding. — [issue #246](https://github.com/ZaneYork/SMAPI-Android-Installer/issues/246); [issue #20](https://github.com/NRTnarathip/SMAPI-Android-1.6/issues/20)

### Inferences
- The developers are passively neutral. There is no official support and no observed enforcement or anti-tamper measures against Android loaders.

### Gaps
- I did not confirm whether ConcernedApe or the mobile team ever commented on the Android loaders or on save-compatibility issues they cause.
