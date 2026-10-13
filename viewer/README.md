# Offline Book Reader (Windows x64)

A dedicated Chromium/Electron reader for **self-contained HTML books**. Includes Algebra Adventure. No address bar, web search, external-link launcher, login, analytics, or updater.

## Use the packaged Windows application

1. Download the `OfflineBookReader-Windows-x64` artifact from a successful **Windows reader** run in this repository's GitHub Actions tab. Extract the entire ZIP to its permanent local folder. Do not run it inside the ZIP.
2. Right-click `Enable-Network-Block.cmd` and select **Run as administrator**. This adds inbound and outbound Windows Firewall block rules for this reader executable only. It does not disable your computer's internet access or change the firewall's profile settings.
3. Confirm the script says `VERIFIED`, then start `OfflineBookReader.exe` normally (not as administrator).
4. Use **Book > Open HTML book** to select another local `.html` or `.htm` file, or use the included Algebra Adventure.

The app refuses to open books unless the rules and enabled firewall profiles are verified. It rechecks every 30 seconds and closes if verification fails. Moving the application folder requires running setup again for the new executable path. Windows may warn because this initial build is unsigned; no code-signing identity is bundled.

The ZIP must contain the executable, Chromium DLLs/resources, the `resources` folder, and the setup/check commands. The executable alone is not portable.

## Reader controls

- Ctrl+O: open book; recent books are in the Book menu.
- Ctrl+D: save the current scroll position as a bookmark.
- Ctrl++ / Ctrl+- / Ctrl+0: zoom in, out, or reset.
- Ctrl+R: reload the book from disk.
- Ctrl+P: normal print dialog, including installed PDF printers.
- F11: full screen; the same shortcut exits full screen.
- Book > Open Algebra Adventure: return to the bundled course.

Books can save their own progress using localStorage or IndexedDB. Each canonical file path gets a separate persistent browser partition and origin; reopening the same path restores that data. Moving or renaming a book creates a new identity. Bookmarks save page scroll positions, not an application's internal lesson state. The algebra course itself remembers the lesson and learner. Reader settings live in Electron's per-user application data directory.

## What it supports

Inline JavaScript/CSS, DOM events, SVG/canvas, and embedded `data:` images/fonts/media. Files must be UTF-8 `.html`/`.htm`, at most 25 MiB, on a local drive. All bytes for a book must be in that one file. External sibling CSS, images, scripts, fonts, fetched assets, workers, WebAssembly compilation requiring relaxed CSP, frames, plugins, form submissions and downloads are intentionally unsupported in v0.1. The included algebra course meets these restrictions.

Each opened book is read into memory and served through a custom local protocol. No localhost server or exposed listening port is used. Reload explicitly to pick up edits made on disk.

## Security boundary and limits

- Windows Firewall supplies the process-level inbound/outbound network block. All three profiles must be enabled. Application request blocking alone is not presented as a total networking guarantee.
- The reader checks effective ActiveStore rules, their application path, direction, action, profile, protocol, address, port, service, and interface scope. Enterprise policies that prevent verification cause a closed failure.
- All browser sessions deny network URLs, device permissions and downloads. Books run sandboxed, without Node integration, preload bridges, developer tools, popups, subframes, external navigation or file-protocol access.
- Reader-enforced CSP blocks network resources and connections, independent of a book's own CSP. JavaScript can run locally but cannot call native Node APIs.
- Packaging disables Electron's RunAsNode, NODE_OPTIONS and inspector fuses, limits application loading to ASAR and removes extra file-protocol privileges.
- Development mode explicitly skips OS network verification and displays a warning in the window title. Packaged builds ignore the development and smoke-test bypass arguments.
- Firewall setup needs administrator rights; daily reading does not. An administrator can change firewall settings or replace this unsigned application. This is not a tamper-proof kiosk, a device-wide parental-control system, or a claim that Chromium's networking code has been removed. It does not prevent a child opening another application.
- Printing is an explicit user action: a network printer or PDF-provider driver may communicate through Windows spooler/other processes, outside this executable's firewall rules. Use a local PDF printer for an entirely local workflow.
- Network paths and mapped network drives are rejected. Browser-engine vulnerabilities are still possible: use books from sources you trust, and rebuild with maintained Electron releases. No automatic internet updater is included.

To remove rules after uninstalling, use Windows Defender Firewall with Advanced Security and delete only the `Offline Book Reader` rules for the removed executable. Leaving them in place is harmless. The reader itself never weakens firewall protections.

## Build from source

Requires Node.js 22.12+ and npm. Initial dependency installation and packaging downloads require internet access **on the build computer**; the packaged reader requires none.

```powershell
cd viewer
npm ci
npm run setup:electron
npm test
npm run package:win
```

The Windows folder is written to `viewer/dist/OfflineBookReader-win32-x64`. Keep all files together. The packager pins Electron 44.7.0 and a committed dependency lockfile. Its Chromium version is supplied by that pinned Electron release.

For source development only:

```powershell
npm run dev
```

This is deliberately labeled as **not OS-network-verified**. It is not the children's protected launch mode.

For actual Electron integration checks on Windows, first run the guard as administrator for `node_modules/electron/dist/electron.exe`, then run `npm run test:electron`. CI does this on a temporary Windows runner and tests the normal verification gate, real DOM interaction, persistence across reopen, book isolation, blocked network fetches, blocked remote scripts, navigation, popups, and a rendered image. Tests use a separate disposable user-data directory.

Local Node checks cover the URL allowlist, path validation, bounds, and CSP. The workbook has its own 800-case arithmetic checks. Consult the Actions run for actual Windows integration/build results; a successful Node policy test alone does not validate Windows Firewall or Chromium rendering.
