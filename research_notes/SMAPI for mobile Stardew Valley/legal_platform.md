# Legal, Licensing and Platform-Policy Constraints on a Mobile SMAPI-like Mod Loader (as of Oct 2026)

*Not legal advice. Several primary sources (stardewvalley.net, stardewvalleywiki.com, androidauthority.com, android-developers.googleblog.com) failed DNS resolution from the research environment and could not be fetched directly, so some findings rely on search-result summaries. Uncertainty is flagged throughout.*

## 1. ConcernedApe / Stardew Valley EULA, modding policy, and stance on mobile mods; DMCA history

### Takeaway
No current, citable ConcernedApe statement on *mobile* mods was found. The only mobile-specific statement located is from the 2018 port announcement ("mods will not be supported"). ConcernedApe has said mod support on console is not something he opposes but doesn't think is feasible. No DMCA takedown of an Android SMAPI port or launcher was found; the one notable Stardew DMCA (2025) was a third-party IP holder hitting a PC content mod by mistake.

### Cited Findings
- At the 2018 iOS/Android port announcement, the developer said mods would not be supported on mobile, and that save data with mods could cause compatibility problems — [Inquirer Technology](https://technology.inquirer.net/80093/stardew-valley-crops-mobile-devices); [Gameluster](https://gameluster.com/stardew-valley-making-way-mobile-devices/)
- On console (Switch/Switch 2), ConcernedApe responded to a fan request that adding mod support is not something he would oppose if it were simple, but he doesn't think it is possible, "for many reasons" — [Gameblog.fr](https://www.gameblog.fr/jeu-video/ed/news/stardew-valley-createur-support-mods-consoles-709280); [GoNintendo](https://www.gonintendo.com/contents/56517-stardew-valley-creator-doesn-t-think-mods-are-possible-in-the-console-version); [Multiplayer.it](https://multiplayer.it/notizie/stardew-valley-avra-le-mod-su-console-lautore-risponde-con-alcune-considerazioni.html)
- The PC modding community is large (30,000+ mods on Nexus, PC-only per the report) — [Gameblog.fr](https://www.gameblog.fr/jeu-video/ed/news/stardew-valley-createur-support-mods-consoles-709280)
- Wizards of the Coast issued a DMCA takedown (late March 2025) against "Baldur's Village", a Stardew PC mod on Nexus Mods, then said it was "issued mistakenly" and the mod was restored ~April 1, 2025 — [VGC](https://videogameschronicle.com/news/wizards-of-the-coast-apologises-for-its-dmca-takedown-of-stardew-valley-mod-based-on-baldurs-gate-3); [EN World](https://www.enworld.org/posts/9625637/)
- The community Android SMAPI ports are documented openly on the official Stardew Valley Wiki (wiki.stardewvalley.net "Modding:Installing SMAPI on Android"), which describes the port as experimental and requiring 1.6.15.1+ from Play Store or Galaxy Store on a 64-bit OS — [Stardew Valley Wiki (search summary)](https://wiki.stardewvalley.net/Modding:Android)
- A forum user reported that a SMAPI Android launcher refused to recognize a legitimately purchased copy installed via a third-party container ("gbox"), saying the user had to get the game "officially" — [Nexus forums (anecdote via search)](https://forums.nexusmods.com/profile/194616081-sunfish511/)

### Inferences
- The fact that the officially hosted Stardew Valley Wiki documents Android SMAPI installation, and that ports have existed since ~2019 (MartyrPher, ZaneYork, now NRTnarathip) without any found takedown, suggests de facto tolerance of on-device, bring-your-own-game modding. Tolerance is not a license; it can be revoked.
- ConcernedApe's console comment ("not opposed... if simple") suggests his objection is practical/support-burden rather than principled, which is favorable for a respectful, clearly-unofficial project that does not generate support load for him or the mobile porter.
- Main EULA-type risk: typical game EULAs prohibit reverse engineering/modification; a loader that patches the game binary on-device may technically breach the EULA (a contract claim against users / the developer) even if no copyright is infringed by distribution.

### Gaps
- Could not fetch stardewvalley.net (DNS failure); the text of the Stardew Valley EULA / Terms and any official "modding policy" page could not be verified. The report writer should not quote a specific EULA clause.
- No 2024–2026 statement from ConcernedApe specifically on mobile modding was found.
- No evidence found either way of DMCA takedowns of Android SMAPI ports or modded Stardew APKs (absence of evidence, not evidence of absence; modded APK sites are often taken down quietly).
- Identity/stance of the current mobile porter/publisher (the 2018 port was published with Chucklefish; current maintainer of mobile builds not verified) — not researched successfully.

## 2. Licenses: SMAPI (LGPL-3.0), Harmony (MIT), MonoMod (MIT) — forking and redistribution

### Takeaway
SMAPI is LGPL-3.0; Harmony and MonoMod are MIT. Forking/porting SMAPI is legally permitted, but the fork's modified SMAPI code must stay LGPL with source available, notices retained, and the user able to replace the library. These licenses cover only the loader code — they grant nothing over the game itself, its binaries, or the "Stardew Valley" trademark.

### Cited Findings
- SMAPI's LICENSE.txt is the GNU Lesser General Public License v3 (29 June 2007) — [Pathoschild/SMAPI LICENSE.txt](https://github.com/Pathoschild/SMAPI/blob/develop/LICENSE.txt)
- Harmony is MIT, "Copyright (c) 2017 Andreas Pardeike"; Harmony uses MonoMod.Core — [pardeike/Harmony LICENSE](https://github.com/pardeike/Harmony/blob/master/LICENSE)
- MonoMod and HarmonyX are MIT-licensed (as listed in the LemonLoader/MelonLoader repo's third-party license section) — [LemonLoader/MelonLoader](https://github.com/LemonLoader/MelonLoader)
- Existing Android ports are GitHub forks of Pathoschild/SMAPI (NRTnarathip/SMAPI-Android-1.6, and a further fork Jakub-Glab/SMAPI-Android-1.6 with ~4,600 commits); their READMEs reuse upstream SMAPI text and do not state affiliation or endorsement — [NRTnarathip/SMAPI-Android-1.6](https://github.com/NRTnarathip/SMAPI-Android-1.6); [Jakub-Glab/SMAPI-Android-1.6](https://github.com/Jakub-Glab/SMAPI-Android-1.6)
- Comparable project: LemonLoader (MelonLoader Android port) is Apache-2.0, includes MIT/Apache/LGPLv3 components, downloads Unity runtime libs at runtime (under Unity ToS) rather than bundling them, and explicitly disclaims affiliation with Unity — [LemonLoader/MelonLoader](https://github.com/LemonLoader/MelonLoader)

### Inferences
- LGPL-3.0 obligations for a port: publish source of modified SMAPI, keep the LGPL license and copyright notices, mark changes, and (for LGPL's relinking clause) allow users to swap in a modified SMAPI build. Shipping the loader inside a closed-source launcher APK is acceptable only if SMAPI remains a replaceable library and its source is provided. Simplest compliance: keep the whole project open source under LGPL-3.0 (or GPL-compatible).
- The LemonLoader pattern — downloading proprietary runtime pieces at install time rather than redistributing them — is a useful model: never bundle Stardew's own DLLs (StardewValley.dll, MonoGame/FNA game assemblies, etc.) in the distributed APK.
- MIT for Harmony/MonoMod imposes only notice retention.
- "SMAPI" is a project name, not a registered trademark as far as found, but using it implies endorsement; see section 6.

### Gaps
- Did not verify whether the Android port's launcher (SMAPILoader) carries its own license distinct from the SMAPI fork's LGPL.
- No trademark registration search done for "SMAPI" or "Stardew Valley".

## 3. Redistributing the APK vs patching the user's own install; precedent (MCPE launchers, Pojav, Geode, MelonLoader)

### Takeaway
Distributing the game APK or modified game binaries is copyright infringement. The safe pattern used by Android SMAPI, Geode, and LemonLoader is a separate launcher that uses the game the user has already installed from an official store and loads mods at runtime, never shipping game code. No public litigation against such launchers was found; the risk is mainly DMCA/ToS-based, not established case law.

### Cited Findings
- Android SMAPI install flow: install the "SMAPI Launcher" APK from NRTnarathip/SMAPILoader releases, download a SMAPI zip, "Install SMAPI From Zip", then "Start Game." The guide does not document internally whether it clones/patches the installed APK — [SMAPILoader wiki: How To Install SMAPI](https://github.com/NRTnarathip/SMAPILoader/wiki/How-To-Install-SMAPI)
- The wiki requires the game from Play Store or Galaxy Store (official sources) — [Stardew Valley Wiki (search summary)](https://wiki.stardewvalley.net/Modding:Android)
- Earlier Android SMAPI ports were by MartyrPher and later ZaneYork; official SMAPI is not compatible with the custom Android version — [Stardew Valley Wiki (search summary)](https://stardewvalleywiki.com/Modding:Installing_SMAPI_on_Android)
- Geode (Geometry Dash mod loader) has an android-launcher repo described as launching an **unmodified** Geometry Dash with modifications applied; BSL-1.0 licensed, updated Feb 2026 — [Geode docs](https://docs.geode-sdk.org/); [Geode README](https://cdn.jsdelivr.net/gh/geode-sdk/geode@main/README.md)
- A weak secondary source says RobTop has not officially endorsed Geode but has not banned users for using it — [Cal Poly-hosted article (low reliability)](https://grandavehousing.calpoly.edu/news/geode-gd-what-it-is)
- LemonLoader fetches Unity runtime libraries at runtime rather than redistributing them — [LemonLoader/MelonLoader](https://github.com/LemonLoader/MelonLoader)

### Inferences
- Safest technical/legal model: (a) launcher contains only original/open-source code; (b) reads the game from the user's own official install on-device (Play/Galaxy); (c) any patching/re-signing happens on the device and the output is never uploaded or shared; (d) optionally verify the source install came from an official store to avoid becoming a piracy vector (the "gbox" anecdote suggests the current launcher does some source check).
- On-device patching still likely breaches the EULA (contract) and could raise anti-circumvention (DMCA §1201 / EU equivalents) questions if it bypasses a licensing/integrity check; interoperability exemptions (e.g., 17 U.S.C. §1201(f), EU Software Directive Art. 6) may help but are untested for game mod loaders — flag as legal uncertainty.
- If the launcher must re-sign the APK (Android won't let a third party inject into another app's process otherwise), the result is a separately-signed copy; any Play license / Play Integrity check in the game could fail, and any "share/export APK" feature would turn the tool into a piracy distribution vector.

### Gaps
- Could not find sources on Minecraft PE launcher takedowns (e.g., BlockLauncher, Toolbox), PojavLauncher legal issues, or any Nintendo takedown of a mobile mod loader. Searches returned only spam. The report writer should not cite specific precedent here.
- No court case directly on mobile game mod loaders was found.
- Internal mechanism of SMAPILoader (clone vs. virtual container vs. in-place) not verified from source.

## 4. Google Play policy; Android developer verification (2026); Play Integrity / licensing in Stardew mobile

### Takeaway
A loader that injects code into another app and downloads executable mod DLLs is very likely ineligible for Google Play (Device and Network Abuse policy). Distribution has to be off-Play, and from Sept 30, 2026 (four countries) and globally in 2027, off-Play APKs on certified devices must be registered by a verified developer, or users must use ADB or the new "advanced flow". A pseudonymous hobby loader is affected most.

### Cited Findings
- Google Play Device and Network Abuse policy bars apps that "interfere with, disrupt, damage, or access in an unauthorized manner" devices, other apps, or services; a Play app may not modify itself except via Play updates, and may not download executable code (dex, JAR, .so) from outside Play; game-cheating apps affecting other apps are listed violations — [Google Play: Device and Network Abuse](https://support.google.com/googleplay/android-developer/answer/9888379?hl=en)
- 2021 addition extended rules to interpreted code (JS, Python, Lua) loaded at runtime — [The Register](https://www.theregister.com/software/2021/07/30/google-play-puts-android-apps-on-notice-no-naughty-javascript-python-lua/528673)
- Android developer verification timeline (official): Aug 2026 developer APIs, limited distribution accounts and power-user "advanced flow" launch; **Sept 30, 2026** enforcement on certified devices (Android 7+) in Brazil, Indonesia, Singapore, Thailand; **2027+** global — [Android Developers: Developer verification](https://developer.android.com/developer-verification)
- Off-Play developers register via the Android Developer Console; Play Console auto-registers ~99% of Play apps; fees "potential" (not specified on page) — [Android Developers: Developer verification](https://developer.android.com/developer-verification)
- Limited distribution accounts (students/hobbyists): up to 20 devices, no government ID or fee — [Android Developers: Developer verification](https://developer.android.com/developer-verification)
- Press reports: the advanced flow includes a mandatory 24-hour waiting period and multiple steps; unregistered apps can still be installed via ADB or the advanced flow — [Android Authority timeline](https://www.androidauthority.com/android-sideloading-changes-timeline-3679204/); [GSMArena](https://gsmarena.com/google_android_developer_verification_app_sideloading_changes_timeline-news-73354.php); [9to5Google: Android Developer Verifier app](https://9to5google.com/2026/03/30/android-developer-verifier-app/)
- Early milestone dates differ between reports (April 2026 Verifier service rollout vs July 2026 APIs); Sept 30, 2026 and 2027 milestones are consistent — [Android Authority](https://www.androidauthority.com/android-sideloading-changes-timeline-3679204/); [9to5Google](https://9to5google.com/2026/03/30/android-developer-verifier-app/)
- Play Integrity API offers a licensing verdict (whether the user installed/paid via Play) and app-tampering detection — [Android Developers: Play Integrity overview](https://developer.android.com/google/play/integrity/overview?authuser=1)

### Inferences
- Play listing: effectively not viable. Even a "launcher only" app that downloads SMAPI/mod DLLs violates the executable-code rule, and modifying Stardew would be "unauthorized access" to another app without the rights holder's permission. An officially sanctioned integration by the rights holder is the only plausible Play path.
- Distribution post-2027: the maintainer would need to register as a verified developer (exposes legal identity to Google; Google could then de-register the app on a rights-holder complaint), or users face the ADB/24-hour advanced flow. The 20-device hobbyist account is far too small for public distribution. This is a major new platform risk: the rights holder or Google gains a de facto kill switch over a registered loader.
- Galaxy Store and other OEM stores have their own policies (not researched); F-Droid would reject a loader for a proprietary game unless flagged as non-free (unverified).
- If the Stardew mobile build checks Play licensing/Play Integrity, a re-signed copy might fail; circumventing that check would be the highest legal risk point (anti-circumvention).

### Gaps
- Could not confirm whether Stardew Valley Android actually uses Play Licensing (LVL) or Play Integrity; no primary source found.
- Fee amount for full off-Play developer verification not found on the official page.
- Galaxy Store policy on mod loaders not researched.

## 5. Apple: App Store rules, EU DMA alternative marketplaces, sideloading, JIT — is iOS viable?

### Takeaway
App Store distribution is effectively prohibited (Guideline 2.5.2 bars executing code that changes other apps, and iOS sandboxing prevents touching another app's bundle). The only technical route is EU-only alternative distribution (AltStore PAL's non-notarized "AltStore Classic" + StikDebug JIT) or developer-signing, and that still requires decrypting/re-packaging the user's Stardew IPA, which is legally and technically much riskier than Android. iOS is not realistically viable for a public project as of Oct 2026.

### Cited Findings
- Guideline 2.5.2: apps must be self-contained, "may not read or write data outside the designated container area, nor may they download, install, or execute code which introduces or changes features or functionality of the app, including other apps" — [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- Guideline 4.7 allows only HTML5/JS mini apps, streaming games, chatbots, plug-ins, and emulators to offer non-embedded software, with 4.7.2 barring exposing native APIs without permission — [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- Guideline 5.2.1: no third-party trademarks/copyrighted works without permission; apps should be submitted by the IP owner/licensee — [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- April 2025: AltStore PAL (EU, DMA) added "AltStore Classic", allowing non-notarized apps including JIT-requiring ones; StikDebug enables on-device JIT; AltServer still needed for management — [9to5Mac](https://9to5mac.com/2025/04/19/altstore-pal-switch-game-emulation-jit-compilation/); [Reclaim The Net](https://reclaimthenet.org/altstore-classic-launch-eu-jit-apps-emulators-iphone)
- Apple treats the EU as a separate distribution zone with alternative marketplaces — [Reclaim The Net](https://reclaimthenet.org/altstore-classic-launch-eu-jit-apps-emulators-iphone)

### Inferences
- Notarization for EU alternative marketplaces still applies baseline review; a loader injecting into another developer's app would very likely fail notarization, pushing it to the non-notarized AltStore Classic path (EU only, technical users).
- iOS App Store apps are FairPlay-encrypted; producing a modifiable copy requires decryption, which is likely anti-circumvention territory. This is a qualitatively higher risk than Android's unencrypted APKs.
- Stardew's .NET/MonoGame on iOS is AOT-compiled; Harmony-style runtime patching needs JIT or interpreter support, so even technically, JIT (StikDebug) dependence makes it fragile.

### Gaps
- 2026 status of AltStore PAL/Classic and of Apple's DMA compliance changes was not confirmed (sources are from 2025).
- Did not verify Stardew iOS runtime (AOT vs interpreter) from a primary source.

## 6. Relationship strategy: ConcernedApe / publisher / porter cooperation; Pathoschild on SMAPI branding

### Takeaway
No public statement from Pathoschild on unofficial mobile ports using the "SMAPI" name was found, and no record of ConcernedApe or the mobile porter cooperating with Android ports. Signals (the officially hosted wiki documents Android SMAPI; ConcernedApe's "not opposed if simple" remark) suggest approaching them is worthwhile, but cooperation is unconfirmed.

### Cited Findings
- The official SMAPI is not compatible with the custom Android version; Android ports were built separately by MartyrPher then ZaneYork, and forum users note both were sometimes outdated, implying maintenance separate from Pathoschild's project — [Stardew Valley Wiki (search summary)](https://stardewvalleywiki.com/Modding:Installing_SMAPI_on_Android); [Stardew forums](https://forums.stardewvalley.net/threads/i-cant-figure-out-how-to-get-higher-than-smapi-3-7-on-my-android.14663/latest)
- The current port repos reuse upstream SMAPI branding/README without an affiliation statement — [NRTnarathip/SMAPI-Android-1.6](https://github.com/NRTnarathip/SMAPI-Android-1.6)
- Precedent for a clean non-affiliation disclaimer: LemonLoader explicitly disclaims affiliation with Unity and acknowledges the trademark — [LemonLoader/MelonLoader](https://github.com/LemonLoader/MelonLoader)
- ConcernedApe: not opposed to console mod support if it were simple — [Gameblog.fr](https://www.gameblog.fr/jeu-video/ed/news/stardew-valley-createur-support-mods-consoles-709280)

### Inferences
- Recommended posture: distinct project name (e.g., not "SMAPI Mobile" without Pathoschild's OK), prominent "unofficial, not affiliated with ConcernedApe, the mobile publisher/porter, or the SMAPI project" disclaimer, no use of Stardew logos/art in icons, free of charge (monetization raises infringement and EULA exposure and invites takedown), and early private outreach to Pathoschild (for naming/API compatibility and smapi.io integration) and ConcernedApe (to agree on support-load boundaries, e.g., modded saves/bug reports flagged).
- Overall safest distribution model, ranked: (1) official cooperation/whitelisting by the rights holder (only route to Play/App Store); (2) open-source LGPL launcher on GitHub, verified-developer-registered APK distributed off-Play, patching only the user's own official install on-device, never bundling game files, never bypassing license checks, no APK export; (3) iOS: do not pursue publicly.

### Gaps
- Pathoschild's views on mobile branding: not found (would need SMAPI Discord/GitHub issues).
- No info found on whether the mobile porter has ever responded to modding requests.
