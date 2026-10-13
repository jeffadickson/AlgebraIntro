# AlgebraIntro

An interactive introduction to algebra for children around age nine. The course starts with equality and connects pictures, words, and equations. It is designed for short sessions with an adult.

## Open the course

Download `Algebra_Adventure.html` and open it in a desktop browser. When downloading from GitHub, use **Download raw file**, or download the repository ZIP and extract it first.

The HTML file contains every lesson, style, and script. No installation, server, account, dependency download, or internet connection is required to use it. Some mobile file-preview applications do not execute JavaScript; use a browser that supports local HTML files.

## Teaching sequence

The runnable course implements the [reviewed outline](docs/curriculum/OUTLINE.md): 11 core episodes and one optional extension. The [review record](docs/curriculum/REVIEW.md) preserves the AI review history; it is not a human teacher endorsement.

1. Equals means same value.
2. Change both sides.
3. A letter names a number.
4. Undo addition, including zero and reversed equations.
5. Undo subtraction.
6. Equal groups and repeated unknowns.
7. Replace a known value.
8. Undo two steps.
9. Translate “more than.”
10. Two clues find two quantities.
11. Choose a method and check.
12. Optional answer detective.

Includes brief animated robot gestures, live activities, generated practice, hints, worked solutions, checkpoints, and a printable standalone teaching guide. Story bars begin with unknown counts. Bar models provide a bridge to schoolwork without assuming a particular textbook edition.

## Progress and teaching

Quinn, Reagan, and Guest save separate progress in local storage. Older eight-lesson counts remain intact in a legacy record; they do not become independent evidence. New progress distinguishes practice with help from answers without in-page hints. An adult records explored / supported / independent / revisited observations after an explanation. No lessons are locked and no number of clicks awards mastery.

Use 10–15 minute sessions as a starting point. Episodes 6 and 10 have explicit pause points. Copying the file, changing browsers, or clearing browser storage may reset local progress.

## 200-page illustrated coursebook

The expanded self-contained book has matching color and ink-friendly monochrome editions. Each is exactly 200 pages: eight introductory pages, twelve 12-page episodes, sixteen mixed-review pages, eight references, and twenty-four answer-key pages. There are 376 numbered exercises. The same content and pagination appear in both editions.

Each episode now includes five teaching pages: an introduction, a concrete model, detailed symbol explanations, and two fully worked examples. Practice includes error repair, guided questions, partly completed reasoning, independent work, short stories, checkpoints, and later revisits. The offline HTML includes the expanded models and explanations under “More detail.”

Generated Pip artwork has separate color and black-outline versions. The monochrome PDF uses grayscale image data, black text, and open diagrams; no task requires color. Art sources and prompts are in `workbook/art/`. Exact mathematical diagrams are drawn programmatically.

To reproduce the books, install Python packages from `workbook/requirements.txt`, install DejaVu Sans (or set `ALGEBRA_FONT_DIR` to its folder), then run:

```sh
python tools/build-workbook.py
python tests/check-workbook.py
```

Outputs: `workbook/Algebra_Adventure_200_Color.pdf` and `workbook/Algebra_Adventure_200_Monochrome.pdf`. Use `--edition color` or `--edition mono` for one edition. `tools/build-workbook-100.py` preserves the earlier layout. Generated PDF/ZIP files are distributed as downloadable artifacts; the source, artwork, exercise manifests, and answer keys are in the repository.

The builds verify page count, matching edition text, content bounds, exercise/key coverage, and monochrome color use. Rendered pages are visually reviewed during production. These are publishing checks, not evidence of classroom effectiveness.

## Offline behavior and its limits

The course has no external assets, analytics, network calls, or third-party scripts. Its Content Security Policy includes `connect-src 'none'` and restrictive resource rules.

When opened in a regular browser, the HTML file cannot prevent the browser itself, other tabs, or extensions from using the network. For a dedicated Windows application with enforced network-block rules, use the [Offline Book Reader](viewer/README.md). The reader includes the course, a local HTML file picker, bookmarks, zoom, and separate saved data for each book. See its guide and GitHub Actions build results before installing.

## Build and checks

The delivered HTML needs no build or dependencies. To edit the course sources and rebuild it:

```sh
python tools/build-course.py
node tests/check-course.cjs
```

Sources are `course/lessons.json`, `course/shell.html`, and `course/runtime.js`. Tests check 2,400 generated problems, all twelve render paths and checkpoints, help tracking, profile migration, subtraction and two-step activities, unknown story bars, and offline resources. Windows CI also runs real Chromium interactions under the reader's firewall rules and packages the updated reader.

The PDF is rendered and visually inspected during production. These checks do not establish classroom effectiveness or cover every browser's local-file storage behavior.

## Dedicated Windows reader

See [viewer/README.md](viewer/README.md) for the application, first-run firewall setup, supported HTML features, build instructions, and security limits. The Windows reader workflow builds a downloadable application artifact after its checks pass.

## Pip, the robot helper

The lessons include a small inline SVG robot with brief CSS gestures at lesson starts, worked steps, hints, and answer checks. Pip makes no sound and uses no external assets or network services. The motion toggle is saved locally; system reduced-motion settings also stop the animation.

## Open work

Use [GitHub Issues](https://github.com/jeffadickson/AlgebraIntro/issues) to track unfinished work. [Issue #1](https://github.com/jeffadickson/AlgebraIntro/issues/1) records the reviewed curriculum implementation. Commits record completed changes.
