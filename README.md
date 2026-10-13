# AlgebraIntro

An interactive introduction to algebra for children around age nine. The course starts with equality and connects pictures, words, and equations. It is designed for short sessions with an adult.

## Open the course

Download `Algebra_Adventure.html` and open it in a desktop browser. When downloading from GitHub, use **Download raw file**, or download the repository ZIP and extract it first.

The HTML file contains every lesson, style, and script. No installation, server, account, dependency download, or internet connection is required to use it. Some mobile file-preview applications do not execute JavaScript; use a browser that supports local HTML files.

## Lessons

1. What equals means: both sides have the same value.
2. Keep it balanced: apply the same operation to both sides.
3. Meet the mystery: letters represent numbers.
4. Undo addition: solve simple equations by subtraction.
5. Undo subtraction and equal groups: addition and division.
6. Use what you know: substitute a known value into another equation.
7. Turn stories into algebra: two clues, two unknowns, matching bars.
8. Be an answer detective: check whether a numerical answer fits the story.

Includes live balance and equation activities, generated practice, hints, incremental worked solutions, a printable parent guide, and a paper worksheet with answers. Bar models provide a bridge to schoolwork; this is not tied to a particular Singapore Math textbook or edition.

The room example uses thirteen people with five more adults than children: four children and nine adults. The twelve-person variation deliberately shows an impossible whole-person answer.

## Progress and teaching

The Quinn, Reagan, and Guest profiles store separate progress in browser local storage when available. Copying the file, changing browsers, privacy settings, or clearing browser data may reset progress. Lessons are never locked. Badges count completed practice, including practice completed with hints; they are not mastery assessments.

Use 10–15 minute sessions as a starting point. Ask the child to explain a step and check an answer before moving on. Lesson 5 and the story lesson can be split over multiple sessions.

## Offline behavior and its limits

The course has no external assets, analytics, network calls, or third-party scripts. Its Content Security Policy includes `connect-src 'none'` and restrictive resource rules.

This is a standalone HTML course, **not a network-disabled Chromium application**. The browser itself, other tabs, and extensions may still use the network. Disconnect the computer or enforce an operating-system network restriction if you need the browser process to have no network access. A dedicated network-disabled book reader is a possible future project and is not implemented here.

## Checks

With Node.js installed:

```sh
node tests/check-course.cjs
```

No npm packages are needed. Checks cover 800 generated problems using independent arithmetic, the eight lesson render paths with a DOM stub, answer feedback, duplicate-credit prevention, selected balance/equation operations, invalid zero operations, story calculations, separate profiles, and an offline-resource audit.

**Verification limit:** these checks use a DOM stub, not a real browser. They do not verify visual layout, browser event behavior, printing, or persistence under every browser's local-file rules. Manual desktop and mobile browser testing remains outstanding.

## Files

- `Algebra_Adventure.html` — complete application and printable teaching guide.
- `tests/check-course.cjs` — dependency-free logic checks.

No build step is needed. Edit the HTML directly and rerun the checks.
