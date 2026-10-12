# Technical stack: Stardew Valley on Android/iOS vs. SMAPI on PC, and what a mobile SMAPI has to do

Research date: 2026-10-12. Most of the Android findings come from **primary source code**: I shallow-cloned and read three repos.
- `NRTnarathip/SMAPILoader` (the launcher APK). HEAD commit 70a2478, dated 2026-06-28.
- `NRTnarathip/SMAPI-Android-1.6` (the SMAPI fork). HEAD commit dated 2026-04-03, "BumpVersion: 4.3.2.5".
- `ZaneYork/SMAPI-Android-Installer` (the older installer). HEAD commit dated 2025-07-15.

Note: the domains stardewvalleywiki.com, wiki.stardewvalley.net and learn.microsoft.com would not resolve from this environment. Wiki facts below therefore come from search-result snippets, not full page reads.

## Q1. PC: runtime, frameworks, and what SMAPI 4.x needs from the runtime

### Takeaway
On PC, Stardew Valley 1.6 is a 64-bit MonoGame 3.8 game that runs on .NET 6 (CoreCLR with a JIT). SMAPI 4.x needs three runtime features:
1. **Load-time IL rewriting with Mono.Cecil.** SMAPI reads each mod DLL, rewrites its references, writes it to bytes, then calls `Assembly.Load(byte[])`.
2. **Runtime method detouring with Harmony 2.x.** Harmony runs on MonoMod.Core and needs JIT, `System.Reflection.Emit`/DynamicMethod, and writable/executable memory to patch native code.
3. **Reflection.Emit-generated proxies.** Pintail uses these for mod-to-mod APIs.

All three assume a JIT-capable runtime that can load assemblies dynamically.

### Cited Findings
- Stardew Valley 1.5.5 moved the game from XNA/.NET Framework 4.5.2 to MonoGame targeting .NET 5. The main branch is "MonoGame 3.8 with 64-bit .NET 5" — [Modding:Migrate to Stardew Valley 1.5.5](https://stardewvalleywiki.com/Modding:Migrate_to_64-bit_on_Windows); [Stardew Valley blog](https://www.stardewvalley.net/?p=1926)
- Stardew Valley 1.6 moves C# mods from .NET 5 to .NET 6. The wiki tells mod authors to change `TargetFramework` from `net5.0` to `net6.0`, and notes that SMAPI still loads .NET 5 mods — [Modding:Migrate to Stardew Valley 1.6](https://stardewvalleywiki.com/Modding:Migrate_to_Stardew_Valley_1.6)
- SMAPI "rewrites mods' compiled code before loading them so they work on Linux/macOS/Windows". It is "installed alongside the game's executable, and doesn't change any of your game files" — [SMAPI README via fork page](https://github.com/NRTnarathip/SMAPI-Android-1.6)
- SMAPI's `AssemblyLoader` works like this in the SMAPI 4.3.x codebase (inherited by the Android fork):
  - It reads mods with `AssemblyDefinition.ReadAssembly(..., new ReaderParameters(ReadingMode.Immediate){ InMemory = true, ReadSymbols = true ...})`.
  - It runs rewriters and finders. Rewriters include `HeuristicFieldRewriter`, `HeuristicMethodRewriter`, `ReplaceReferencesRewriter`, and version facades in `StardewValley_1_5` and `StardewValley_1_6`. Finders include `ReferenceToInvalidMemberFinder`, `TypeFinder`, and others.
  - It then writes the result to a stream and calls `Assembly.Load(bytes, symbols)` (AssemblyLoader.cs lines ~186–303).
  - Source: [SMAPI-Android-1.6 src/SMAPI/Framework/ModLoading](https://github.com/NRTnarathip/SMAPI-Android-1.6/tree/develop/src/SMAPI/Framework/ModLoading)
- SMAPI's project references Lib.Harmony, Mono.Cecil, Pintail, System.Reflection.Emit, DeepCloner, SkiaSharp, Platonymous.TMXTile and NVorbis — [SMAPI-Android-1.6 SMAPI.csproj](https://github.com/NRTnarathip/SMAPI-Android-1.6/blob/develop/src/SMAPI/SMAPI.csproj)
- Harmony 2.x is built on MonoMod.Core. 2.3.4 (5 Feb) added .NET 9 support with MonoMod.Core 1.2.3. 2.4 (17 Aug 2025) added "Full support for arm64 across all operating systems, including Apple Silicon". 2.4.2 (13 Nov) moved to MonoMod.Core 1.3.3 and supports .NET 10. 2.4.3 (11 Oct) uses MonoMod.Core 1.3.6. 3.0.0-rc.1 and rc.2 were pre-releases in October — [Harmony releases](https://github.com/pardeike/Harmony/releases); [Lib.Harmony on NuGet](https://packages.nuget.org/packages/Lib.Harmony)
- Mods turn Harmony on with `<EnableHarmony>true</EnableHarmony>` in the mod build config — [Migrate to 1.5.5 wiki](https://wiki.stardewvalley.net/Modding:Migrate_to_Stardew_Valley_1.5.5)

### Inferences
- The runtime features SMAPI depends on are:
  - (a) loading assemblies from byte arrays at runtime (`Assembly.Load(byte[])`);
  - (b) JIT compilation of newly loaded IL;
  - (c) `System.Reflection.Emit` / `DynamicMethod`, which Harmony uses for replacement methods and Pintail uses for proxies;
  - (d) native code detours, where MonoMod.Core overwrites the start of JIT-compiled methods. This needs W+X memory or a mprotect toggle, plus per-architecture (x64/ARM64) trampolines;
  - (e) unrestricted private-member reflection.
- The content API (`helper.GameContent` / `AssetRequested`) sits on top of MonoGame's `ContentManager`/`TitleContainer`. It does not need special runtime features, but it does need the game's asset paths and how it opens streams.
- The years for Harmony 2.4.2, 2.4.3 and 3.0 rc are inferred: the releases page shows day and month only. The ordering suggests Nov 2025 for 2.4.2 and Oct 2026 for 2.4.3 and the 3.0 RCs.

### Gaps
- I did not fetch Pathoschild's upstream `docs/technical/smapi.md` to quote its official architecture description.
- PC 1.6.15+ is assumed to still run on .NET 6. I found no source saying PC moved to .NET 8 or .NET 9.

## Q2. Android: runtime, packaging format, decompilability

### Takeaway
The Android game is a .NET for Android app (formerly Xamarin.Android) on the **Mono runtime** (`libmonosgen-2.0.so`, `libmonodroid.so`, `libxamarin-app.so`). Its game code is ordinary **IL assemblies**: StardewValley.dll, MonoGame.Framework.dll and StardewValley.GameData.dll. Those assemblies are stored in the .NET Android assembly store. Since 1.6.15 that store is format v2: an ELF-wrapped `lib/arm64-v8a/libassemblies.arm64-v8a.blob.so` with XALZ (LZ4) compression. It ships inside the Play Store **split APKs**:
- `base.apk`
- `split_config.arm64_v8a.apk`
- `split_content.apk`

The assemblies can be extracted and decompiled, and nothing indicates they are obfuscated: mods and the loader reference mobile class names such as `StardewValley.Mobile.MobileDisplay` and `MainActivity.CheckStorageMigration` directly.

### Cited Findings
- SMAPILoader's build doc claims that "The game (Stardew Valley 1.6.15+) is built against .NET 9. The loader must also target .NET 9 to reference the game DLLs" — [SMAPILoader docs/building.md](https://github.com/NRTnarathip/SMAPILoader/blob/master/docs/building.md)
- The same doc says: "Stardew Valley 1.6.15+ uses .NET Android's v2 assembly store format. Assemblies are no longer stored as `assemblies/*.blob` files inside the APK. Instead, they are wrapped in ELF binaries at `lib/{arch}/libassemblies.{arch}.blob.so`." It also gives a v1-vs-v2 table:
  - v2 has an XABA header with version 2;
  - a 12-byte hash index;
  - 28-byte local entries;
  - an inline name table;
  - assembly data that is always XALZ-compressed.
  - Source: [SMAPILoader docs/building.md](https://github.com/NRTnarathip/SMAPILoader/blob/master/docs/building.md)
- "The Play Store version of Stardew Valley uses split APKs":
  - `base.apk`: Java/Kotlin code, no .NET assemblies;
  - `split_config.arm64_v8a.apk`: native libs and the .NET assembly blob;
  - `split_content.apk`: game assets (Content/).
  - Source: [SMAPILoader docs/building.md](https://github.com/NRTnarathip/SMAPILoader/blob/master/docs/building.md)
- The loader finds the APK files through Android's `PackageInfo.ApplicationInfo.PublicSourceDir` and `SplitSourceDirs`, looking for entries containing "split_config.arm64" and "split_content". It supports the package names `com.chucklefish.stardewvalley` (Play) and `com.chucklefish.stardewvalleysamsung` (Galaxy Store), with a minimum game version of 1.6.15.3 — [SMAPILoader StardewApkTool.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Tool/StardewApkTool.cs)
- The game's Content folder ships as zip entries under `assets/Content/...` in `split_content.apk`. The loader copies them out to external app storage — [SMAPILoader GameAssetManager.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Game/GameAssetManager.cs)
- Earlier (1.5-era) builds used the v1 `assemblies/*.blob` store with an `assemblies.manifest`. ZaneYork's installer ships a parser for it (`AssemblyStoreAssembly.java`). Its injected file manifest targets `assemblies/` and `lib/<abi>/` paths for arm64-v8a, armeabi-v7a, x86 and x86_64 — [ZaneYork installer assets/apk_files_manifest.json](https://github.com/ZaneYork/SMAPI-Android-Installer)
- The runtime libraries in the Xamarin/.NET-Android-era game layout are `libmonosgen-2.0.so`, `libmonodroid.so`, `libxamarin-app.so`, `libmono-component-*.so`, `libSystem.Native.so` and `libSkiaSharp.so`. `Mono.Android.dll` and `Java.Interop.dll` are also present — [ZaneYork installer assets/apk.zip listing](https://github.com/ZaneYork/SMAPI-Android-Installer)
- The OBB was relevant in older versions: ZaneYork's code searches for `com.chucklefish.stardewvalley.obb` — [ZaneYork CommonLogic.kt](https://github.com/ZaneYork/SMAPI-Android-Installer)
- No obfuscation is evident. The SMAPI Android fork reflects over unobfuscated mobile types, for example `typeof(MainActivity).Assembly.GetType("StardewValley.Mobile.MobileDisplay")`, `MainActivity.instance` and `MainActivity.CheckStorageMigration` — [SMAPILoader SMAPIActivity.cs / MainActivityPatcher.cs](https://github.com/NRTnarathip/SMAPILoader/tree/master/SMAPIGameLoader/Game)

### Inferences
- The game's IL is preserved and loadable on Mono with JIT. The loader extracts the DLLs and calls `Assembly.LoadFrom` on them, which would not work if the code were only full-AOT native code. So the shipped Android game is at least not *IL-stripped* full AOT. It may still use profiled AOT for startup, but JIT/IL remains available.
- The ".NET 9" claim for mobile 1.6.15+ comes from a third-party build doc, and the PC game is .NET 6. The mobile build is therefore on a newer .NET than PC. Treat this as moderately reliable, since it is consistent with the loader targeting `net9.0-android35.0`.

### Gaps
- Chucklefish/ConcernedApe have published no official statement on mobile build settings: AOT mode, trimming, or whether the game ships as an AAB. That the Play Store delivers split APKs is consistent with AAB publishing, but I could not confirm it directly.
- Mobile 1.5.x build details (Xamarin.Android with Mono and .NET Framework profile?) were not confirmed. I found no primary source for the original 1.5 mobile architecture.

## Q3. iOS: full AOT, and why Harmony-based SMAPI is essentially blocked

### Takeaway
iOS .NET/Xamarin apps are AOT-compiled because Apple forbids runtime code generation. This removes JIT and `Reflection.Emit`, and with them Harmony/MonoMod detours and SMAPI's load-time rewriting of new IL. The Mono interpreter can execute IL that was not AOT-compiled, but it cannot be enabled on a shipped App Store binary without re-signing. No working iOS SMAPI is known.

### Cited Findings
- iOS forbids runtime code generation: dynamic code generation isn't allowed, so `System.Reflection.Emit` is unavailable. The Mono interpreter "overcomes these restrictions while abiding by platform restrictions", interpreting some code at runtime while AOT-compiling the rest, at a cost in speed — [Microsoft Learn: .NET MAUI Mono interpreter on iOS/Mac Catalyst](https://learn.microsoft.com/en-us/dotnet/maui/macios/interpreter?view=net-maui-8.0) (search snippet only; the page was unreachable here)
- One Xamarin.iOS write-up says truly transparent hotpatching on iOS "would likely require crazy runtime-level acrobatics", but rolling your own hotpatching on top of the interpreter is viable — search result summary, original URL not resolved ([cur.at link](https://cur.at/Mw2auli?m=web))
- SMAPI's official install guide lists Windows, macOS, Linux, Steam Deck and Android, with no iOS entry — [smapi.io/install](https://smapi.io/install)
- Forum moderators say iOS SMAPI is blocked by Apple's install restrictions, and that even a jailbreak only allows limited file-replacement modding — [SMAPI for iOS devices? forum thread](https://forums.stardewvalley.net/threads/smapi-for-ios-devices.11309)

### Inferences
- An iOS SMAPI would need four things:
  1. a re-signed app (jailbreak, TrollStore, or developer-certificate sideloading, or an EU alternative marketplace with Apple notarization);
  2. a runtime built with the interpreter enabled, which means rebuilding the game, impossible without source;
  3. replacing Harmony detours with interpreter-level method replacement;
  4. accepting that iOS W^X/code-signing enforcement blocks MonoMod's native trampolines entirely, except on jailbroken devices with relaxed code signing.
- A content-pack-only approach (asset replacement, Content Patcher JSON) is far more feasible on iOS than C# mods, but it would still need to hook asset loading.

### Gaps
- I found no source confirming whether HarmonyX or MonoMod.Core has any iOS/AOT-interpreter mode. I also found no evidence about the iOS game's exact build (Xamarin.iOS vs .NET iOS, interpreter flags).

## Q4. How the Android SMAPI ports work technically

### Takeaway
There are two generations of approach.

**ZaneYork, 1.4/1.5 era: repackaging.** The installer extracts the installed game APK and injects SMAPI plus modified runtime pieces: a patched `libmonosgen-2.0.so`, a patched `System.Private.CoreLib.dll`, `libAnd64InlineHook.so`, and a new `classes.dex`/`AndroidManifest.xml`. It **re-signs** the result with apksig and installs it as a separate package (`com.zane.stardewvalley`).

**NRTnarathip, 1.6 era: no repackaging.** A standalone launcher app (`abc.smapi.gameloader`) built with .NET 9 Android and a **custom-patched Mono runtime**:
1. reads the *installed* Play/Galaxy game's split APKs;
2. extracts IL from the v2 assembly store and the Content assets into its own external files dir;
3. rewrites `StardewValley.dll` with Mono.Cecil;
4. loads the game assemblies into its own process;
5. hosts the game's `MainActivity` logic in its own `SMAPIActivity : AndroidGameActivity`;
6. runs `StardewModdingAPI.Program.Main` through reflection.

Harmony and MonoMod run on ARM64 Mono with JIT.

### Cited Findings — NRTnarathip SMAPILoader + SMAPI-Android-1.6 (current, 2024–2026)
- The wiki credits the Android port history in sequence: MartyrPher (1.4), then ZaneYork (1.5), then NRTnarathip (1.6). It requires a 64-bit OS and Stardew Valley 1.6.15.1 or later from the Play Store or Galaxy Store, and calls SMAPI on Android "still experimental" — [Modding:Installing SMAPI on Android](https://stardewvalleywiki.com/Modding:Installing_SMAPI_on_Android) (search snippet; revisions differ between 1.6.15 and 1.6.15.1). The loader code itself requires ≥ 1.6.15.3 — [StardewApkTool.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Tool/StardewApkTool.cs)
- The README says: "No need install new game apk"; "Need to download game from Play Store only, not support game apks modify or pirate game"; "Support device 64bit only". It thanks "Eky-Team for creating guides and resources to patch .NET 8 to .NET 9" — [SMAPILoader README](https://github.com/NRTnarathip/SMAPILoader)
- Install flow: install the SMAPI Launcher APK, download `SMAPI.4.x.x-(xxxx).zip` from the SMAPI-Android-1.6 releases, choose "Install SMAPI From Zip", then "Start Game". The wiki page was last edited on 24 Dec 2024 — [How-To-Install-SMAPI wiki](https://github.com/NRTnarathip/SMAPILoader/wiki/How-To-Install-SMAPI)
- "The SMAPI Loader extracts game assemblies from the Stardew Valley APK, applies Harmony patches, loads SMAPI, and launches the game." The launcher builds as `net9.0-android` and is signed with a debug keystore (`abc.smapi.gameloader-Signed.apk`) — [building.md](https://github.com/NRTnarathip/SMAPILoader/blob/master/docs/building.md)
- Custom Mono runtime: "The stock .NET 9 Mono runtime (`libmonosgen-2.0.so`) restricts reflection access to private/protected members. SMAPI and Harmony require unrestricted reflection to patch game methods. A custom-built Mono runtime with these restrictions removed must be used." The patched file is copied into the SDK pack `Microsoft.NETCore.App.Runtime.Mono.android-arm64/9.0.14` before building — [building.md](https://github.com/NRTnarathip/SMAPILoader/blob/master/docs/building.md)
- The byte patches to `libmonosgen-2.0.so` (ARM64) are as follows — [LibPatcherArm64.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/LibPatcher/LibPatcherArm64.cs); [LibsPatch/NOTE.txt](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/LibsPatch/NOTE.txt)
  - NOP out the check in `mono_method_can_access_method` at +0x28 to fix MethodAccessException.
  - Force `mov w0,#1` in `mono_method_can_access_field` at +0x130 to fix FieldAccessException.
  - Patch `mono_class_from_mono_type_internal` at +0x23c to fix a crash in `GetParameters()` on some DynamicMethodDefinition (DMD) methods.
  - The patcher hash-checks a target lib labelled "8.0.21".
- Harmony on .NET 9: "The old Harmony 2.3.4 (fat ILRepack'd DLL with embedded MonoMod and Mono.Cecil) crashes on .NET 9 due to the `LocalBuilder` abstract class change". It was replaced with a thin .NET 9-compatible Harmony plus separate `MonoMod.Core` (which now includes RuntimeDetour), `MonoMod.Iced`, `MonoMod.Utils`, `MonoMod.Backports` and `MonoMod.ILHelpers`. The doc suggests taking the builds from "the slaythespire2mobile project" — [building.md](https://github.com/NRTnarathip/SMAPILoader/blob/master/docs/building.md)
- The launcher csproj sets `RunAOTCompilation=False`, `AndroidEnableProfiledAot=False`, `PublishTrimmed=False` and `IsAotCompatible=False`, so it runs on pure Mono JIT. It references Mono.Cecil 0.11.5 and the SharedLibs Harmony/MonoMod builds, and has `SupportedOSPlatformVersion` 28 (Android 9) — [SMAPIGameLoader.csproj](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/SMAPIGameLoader.csproj)
- `GameCloner.Setup()` works as follows — [GameCloner.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Launcher/GameCloner.cs); [GameAssemblyManager.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Game/GameAssemblyManager.cs)
  - It re-clones only when the launcher build or the game version changes.
  - It copies assets.
  - It extracts the game assemblies (from base.apk, falling back to the arm64 split) and the launcher's own untrimmed assemblies into `<ExternalFilesDir>/Stardew Assemblies`.
  - It loads MonoGame.Framework.dll via `Assembly.LoadFrom`.
  - It rewrites StardewValley.dll with Cecil.
- The Cecil rewrite of the game changes the `MainActivity.instance` field type from `MainActivity` to the loader's `SMAPIActivity` — [StardewGameRewriter.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Game/Rewriter/StardewGameRewriter.cs)
- `SMAPIActivity` extends MonoGame's `AndroidGameActivity`. It loads StardewValley.dll and sets `MainActivity.instance` by reflection. It applies a Harmony prefix that makes `MainActivity.CheckStorageMigration` return false. It then does `Assembly.LoadFrom(".../StardewModdingAPI.dll")` and invokes `StardewModdingAPI.Program.Main` — [SMAPIActivity.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Game/SMAPIActivity.cs); [MainActivityPatcher.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Game/MainActivityPatcher.cs)
- Content pipeline redirect: a Harmony prefix on MonoGame `TitleContainer.OpenStream` serves files from `<ExternalFilesDir>/Stardew Assets/Content/...`, which were copied out of `split_content.apk`. It also has an `OnOpenStream` hook for overrides — [GameAssetManager.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Game/GameAssetManager.cs)
- Native libs: the launcher bundles its own `libopenal32.so`, `liblwjgl_lz4.so` and `libstb_png_writer.so` for arm64-v8a — [SMAPIGameLoader/libs](https://github.com/NRTnarathip/SMAPILoader/tree/master/SMAPIGameLoader/libs/arm64-v8a)
- The mods folder is `<ExternalFilesDir>/Mods`, i.e. `Android/data/<launcher pkg>/files/Mods`. The app's own install/mod-manager UI handles installs — [ModTool.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Launcher/ModTool.cs); [FileTool.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Tool/FileTool.cs)
- The SMAPI fork targets `net9.0-android35.0`. It is at version 4.3.2.5 (April 2026) and tracks upstream SMAPI 4.3.2, released 14 July 2025 for game 1.6.14+ — [SMAPI-Android-1.6 SMAPI.csproj and release-notes.md](https://github.com/NRTnarathip/SMAPI-Android-1.6)
- The SMAPI fork adds about 3,900 lines of Android code under `src/SMAPI/Mobile/` — [SMAPI-Android-1.6/src/SMAPI/Mobile](https://github.com/NRTnarathip/SMAPI-Android-1.6/tree/develop/src/SMAPI/Mobile)
  - Core managers: `AndroidPatcher` (Harmony PatchAll), `AndroidGameLoopManager`, `AndroidContentLoaderManager`, `AndroidSaveLoaderManager`, `AndroidModLoaderManager`, `AndroidMainThread`.
  - Mobile UI and data patches: `MobileInputTool`, `MobileFarmChooserPatcher`, `Texture2DRewriter`, `CustomAudioCueModificationManager`.
  - Rewrite facades: `IClickableMenuFacade`, `SaveGameFacade`, `MenuWithInventoryPatcher`.
  - Per-mod fixes: `SpaceCoreFix`, `SveFix`, `FarmTypeManagerFix`, `GenericConfigMenuModFix`, `FashionSenseModFix`, `UnlockableBundlesModFix`.

### Cited Findings — ZaneYork SMAPI-Android-Installer (1.4/1.5 era; repo last commit July 2025)
- Its "How it Works" section lists four steps — [ZaneYork/SMAPI-Android-Installer README](https://github.com/ZaneYork/SMAPI-Android-Installer):
  1. "Extracts the original game."
  2. "Generates SMAPI dependencies."
  3. "Adds SMAPI launch code to the game's files."
  4. "Signs the modified game and calls the package installer."
  - The README also says the Google Play listing was removed and the developer account banned.
- The installed modded app uses package name `com.zane.stardewvalley` (Samsung: `com.zane.stardewvalleysamsung`), so it installs side by side with the original — [Constants.kt](https://github.com/ZaneYork/SMAPI-Android-Installer/blob/master/app/src/main/java/com/zane/smapiinstaller/constant/Constants.kt)
- It signs with Android's `apksig` (`DefaultApkSignerEngine`, v1+v2, v3 disabled) using a bundled debug keystore — [ApkPatcher.kt](https://github.com/ZaneYork/SMAPI-Android-Installer/blob/master/app/src/main/java/com/zane/smapiinstaller/logic/ApkPatcher.kt)
- The injected payload (`assets/apk.zip`, dated 2025-07-14) contains:
  - a replacement `System.Private.CoreLib.dll` per ABI;
  - `0Harmony.dll`, `MonoMod.Common.dll` and Mono.Cecil;
  - `StardewModdingAPI.dll`;
  - a replacement Mono runtime (`libmonosgen-2.0.so`, `libmonodroid.so`, `libxamarin-app.so`) for arm64, armv7, x86 and x86_64;
  - `libAnd64InlineHook.so`, an ARM64 native inline-hook library;
  - a smali patch for `MonoGameAndroidGameView`;
  - plus `classes.dex`, `AndroidManifest.xml` and `resources.arsc` replacements.
  - Source: [ZaneYork installer assets](https://github.com/ZaneYork/SMAPI-Android-Installer/tree/master/app/src/main/assets)
- It bundles REAndroid APKEditor ("AntiSplit") code to merge split APKs into one. If a split contains `lib/<abi>/libpairipcore.so`, it shows a "pairip_warning" and disables signing — [Merger.java](https://github.com/ZaneYork/SMAPI-Android-Installer/blob/master/app/src/main/java/com/reandroid/apkeditor/merge/Merger.java)

### Inferences
- The shift from repackaging (ZaneYork) to a launcher that loads the installed game in its own process (NRTnarathip) sidesteps three problems:
  - re-signing;
  - Play-delivered integrity protection (`libpairipcore.so` is Google Play's automatic anti-tamper/"pairip" library — this identification is my knowledge, not stated in the repo);
  - split-APK merging.
- The NRTnarathip launcher only reads APKs that are world-readable on Android, plus a copy of Content (~hundreds of MB), into its own sandbox.
- Both ports have to modify the Mono runtime to lift access checks, because Mono enforces member-access visibility that CoreCLR on PC doesn't enforce the same way for DynamicMethods. Harmony/MonoMod works on ARM64 Mono only with these patches and with the newer MonoMod.Core.
- Licensing: because the launcher runs game code under a different package/UID, any Google Play LVL or Play Integrity check bound to the game's package would need bypassing or would fail. I found no code in the loader addressing LVL. The game may simply not enforce it.

### Gaps
- I did not inspect MartyrPher's original 1.4 port.
- I did not verify whether Chucklefish's 1.6 APK includes pairip, LVL or Play Integrity calls.
- I did not verify how the custom libmonosgen is built for the 9.0.14 pack (the patcher hash targets 8.0.21, and the doc references 9.0.14, so there is a version inconsistency).

## Q5. Harmony/MonoMod on ARM64, and Mono vs CoreCLR on Android (state as of 2026)

### Takeaway
Upstream Harmony gained official ARM64 support in 2.4 (Aug 2025) via MonoMod.Core. On Android Mono, Harmony works in practice, demonstrated by the NRTnarathip loader and by LemonLoader/MelonLoader for Unity Android. It still needs a .NET 9-compatible thin build and Mono runtime access-check patches. .NET for Android still uses Mono by default; I found no shipping CoreCLR-for-Android Stardew build.

### Cited Findings
- Harmony 2.4: "Full support for arm64 across all operating systems, including Apple Silicon" (17 Aug 2025) — [Harmony releases](https://github.com/pardeike/Harmony/releases)
- In July 2025 a community fork existed because RimWorld on macOS ARM "is not currently supported by MonoMod/Harmony"; it relied on a pending MonoMod PR — [Harmony for Apple Silicon](https://catalogue.smods.ru/archives/371759)
- LemonLoader maintains a MonoMod fork "for ARM64, Android, and linux-bionic runtime support" (updated Oct 2024). MelonLoader credits a contributor with partial ARM64 support in MonoMod — [LemonLoader repos](https://github.com/orgs/LemonLoader/repositories); [LemonLoader/MelonLoader](https://github.com/LemonLoader/MelonLoader)
- On Android .NET 9 Mono, Harmony 2.3.4 crashes with `HarmonyException: Cannot create an instance of System.Reflection.Emit.LocalBuilder` (LocalBuilder became abstract in .NET 9). This needs newer thin Harmony + MonoMod.Core — [SMAPILoader building.md](https://github.com/NRTnarathip/SMAPILoader/blob/master/docs/building.md)
- Mono 6.14 (WineHQ-maintained framework Mono) shipped native ARM64 support in March 2025. This is desktop Mono, not .NET Android's Mono — [AlternativeTo news](https://alternativeto.net/news/2025/3/framework-mono-6-14-released-with-native-arm64-support-and-stability-boosts-under-winehq)

### Inferences
- A 2026 mobile SMAPI should use Harmony ≥ 2.4.x (MonoMod.Core ≥ 1.3) rather than the 2.3.4 fat build, which may make some runtime patches unnecessary. The DMD crash fix and access-check removal will likely still be needed on Mono.

### Gaps
- I found no MonoMod changelog confirming Android/Mono ARM64 detour support specifically, as opposed to CoreCLR ARM64. I also found no status on .NET 10 Android's CoreCLR option.

## Q6. Mobile-specific code differences and how much PC mods break

### Takeaway
The mobile StardewValley.dll diverges from PC:
- extra `StardewValley.Mobile.*` classes;
- `MainActivity`;
- different menu method signatures (e.g. `IClickableMenu.drawToolTip`/`drawHoverText` parameters);
- different save serialization (pre-generated XmlSerializers);
- different farm chooser and inventory menus;
- texture `GetData` behaviour differences;
- touch input instead of mouse/keyboard.

PC C# mods therefore need load-time rewrites (facades), per-mod fixes, or mobile-specific versions. Content-pack mods fare much better.

### Cited Findings
- "The Android version of the game is very custom compared to other platforms, so the official version of SMAPI isn't compatible" — [Installing SMAPI on Android wiki](https://stardewvalleywiki.com/Modding:Installing_SMAPI_on_Android) (snippet)
- The wiki notes that some mods don't work yet. It also says the latest SMAPI isn't always available on Android, so users may need older Android-compatible mod files — [same](https://stardewvalleywiki.com/Modding:Installing_SMAPI_on_Android)
- `IClickableMenuFacadeAndroid` rewrites PC calls to `drawToolTip` to map onto the mobile signature, which has an `additionalCraftMaterials` / `additional_craft_materials` parameter — [IClickableMenuFacade.cs](https://github.com/NRTnarathip/SMAPI-Android-1.6/blob/develop/src/SMAPI/Mobile/Facade/IClickableMenuFacade.cs)
- In `SaveGameFacade`, a code comment says: "on Android we don't use this, because use XmlSerialier Generator instead of dynamic serialization". The facade maps `SaveGame.serializer` / `farmerSerializer` to `SaveSerializer.GetSerializer(...)` — [SaveGameFacade.cs](https://github.com/NRTnarathip/SMAPI-Android-1.6/blob/develop/src/SMAPI/Mobile/Facade/SaveGameFacade.cs)
- The fork contains a `Texture2DRewriter` ("GetDataForPC" crop/resize fixes), `MobileInputTool`, `MobileFarmChooserPatcher`, `MenuWithInventoryPatcher`, `CustomAudioCueModificationManager`, `DisableSaveBackup`/`SaveBackupZip`, and hard-coded fixes for SpaceCore, SVE, Farm Type Manager, GMCM, Fashion Sense and Unlockable Bundles — [SMAPI-Android-1.6/src/SMAPI/Mobile](https://github.com/NRTnarathip/SMAPI-Android-1.6/tree/develop/src/SMAPI/Mobile)
- The loader patches display-cutout padding (`Game1.toolbarPaddingX`, `xEdge`) and uses `StardewValley.Mobile.MobileDisplay` — [SMAPIActivity.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Game/SMAPIActivity.cs)

### Inferences
- Pre-generated XmlSerializers suggest the mobile game avoids runtime codegen for saves, which is consistent with an AOT-friendly design. Mods that add custom serialized types, such as SpaceCore's serializer injection, therefore need special handling; this is why `SpaceCoreFix` exists.
- Version skew is another source of breakage. The mobile game lags PC point releases (mobile 1.6.15.x vs PC 1.6.15+), and SMAPI-Android lags upstream SMAPI (fork at 4.3.2.x).

### Gaps
- There is no quantitative compatibility rate (percentage of top Nexus mods working on Android). I also found no full diff of PC vs mobile APIs.

## Q7. Distribution constraints: signing, Play Integrity/LVL, split APKs, Android 14+, scoped storage, 2026 developer verification

### Takeaway
Repackaging requires re-signing and merging splits, and is blocked by Play's pairip anti-tamper. That pushed the 1.6 port to a separate launcher that reads the legit installed game. Mods live in the launcher's app-specific external storage, which avoids scoped-storage permission issues; users reach it through the launcher's own file-picker installer. A new 2026 risk is Google's **developer verification** for sideloaded apps. It starts **30 Sept 2026** in Brazil, Indonesia, Singapore and Thailand and expands globally in 2027, with ADB installs exempt. Any launcher APK distributed outside Play will need a verified developer identity, or users must install via ADB.

### Cited Findings
- ZaneYork's installer had to merge split APKs (AntiSplit/APKEditor), re-sign with a debug key, request `canRequestPackageInstalls`, and gave up signing when `libpairipcore.so` was present — [ZaneYork Merger.java / ApkPatcher.kt](https://github.com/ZaneYork/SMAPI-Android-Installer)
- The NRTnarathip launcher needs no new game APK and requires a genuine Play/Galaxy install — [SMAPILoader README](https://github.com/NRTnarathip/SMAPILoader)
- Mods and assets go under `Context.GetExternalFilesDir(null)`, i.e. `Android/data/<pkg>/files/` — [FileTool.cs](https://github.com/NRTnarathip/SMAPILoader/blob/master/SMAPIGameLoader/Tool/FileTool.cs)
- Developer verification requirements begin 30 September 2026 for users in Brazil, Indonesia, Singapore and Thailand, and expand globally to certified devices in 2027. The "Android Developer Verifier" system service started appearing in April 2026, ADB is exempt, and there is a lighter process for students and hobbyists — [Android Authority: sideloading changes timeline](https://www.androidauthority.com/android-sideloading-changes-timeline-3679204/); [Android Authority: rollout](https://www.androidauthority.com/android-developer-verification-rollout-sideloading-flow-3653395); [Bitdefender](https://www.bitdefender.com/en-us/blog/hotforsecurity/google-developer-verification-sideloaded-apps)

### Inferences
- Since Android 11, `Android/data/<other pkg>` is not browsable by other apps or the Files app without SAF tricks. This is why the 1.6 launcher ships its own mod installer and manager rather than relying on a shared `StardewValley/Mods` folder, which the older ZaneYork flow used.
- Android 14 blocks installing apps that target API levels below 23. That affects only very old repackaged APKs; current launchers target modern SDKs (min 28).

### Gaps
- I did not verify whether Stardew's Play build actually ships `libpairipcore.so`, LVL or Play Integrity calls.
- I found no primary source on Android 14/15-specific blocks (e.g. restricted settings for sideloaded apps) as they affect these launchers.
- I did not determine whether the NRTnarathip launcher is registered for developer verification.
