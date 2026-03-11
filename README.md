# Buzz's All-American Arcade

A high-quality web arcade wrapper built with React, styled in "Democracy + Retro 80s Synthwave," and hosting custom Python/WASM arcade games.
Currently hosting the first two games in the series: "Ice Out" and "Truth Evaders"!

> This project serves as a portfolio piece showcasing frontend architecture, WebAssembly game integration, and retro design principles.

## To Run

Deployed to GitHub Pages at [https://rudil24.github.io/buzz-arcade/](https://rudil24.github.io/buzz-arcade/)

## Documentation

This project adheres to the OPST Kickoff framework. Please review the foundational documents:

- [Product Requirements Document (PRD)](./docs/PRD.md)
- [Design Document & Visual Mockups](./docs/Design.md)
- [Development Task List](./docsTASK_LIST.md)
- [Team Retro 1 iceout](./.agents/retros/2026-02-26-iceout.md)
- [Team Retro 2 truth-evaders](./.agents/retros/2026-03-11-truth-evaders.md)
- Team Learnings [iceout](./.agents/learnings/2026-02-26-iceout.md) [truth-evaders](./.agents/learnings/2026-03-11-truth-evaders.md)

## Development Setup

The application is structured into two main parts:

1. **React Wrapper**: Built using Vite.
2. **IceOut Game**: Built using Pygame CE and compiled via `pygbag`.

### Prerequisites

- Node.js (for React wrapper)
- Python 3.10+ (for Game building)
- `pygbag` (`pip install pygbag`)

### Quick Start (Local Wrapper)

```bash
git clone https://github.com/rudil24/buzz-arcade.git
cd buzz-arcade
npm install
npm run dev
```

Make sure `iceout.apk` and the Pygbag `index.html` bootloader are located in `public/games/iceout/` before accessing the emulation.

### Building the WASM Game (Ice Out)

We use a patched `index.html` bootloader that natively reads `.apk` (zipfile) formats rather than uncompressed `.tar` archives, as Vite's environments often reject the `untar` method. Wait for `pygbag` to finish compiling its dependencies on the first run.

```bash
cd python_games/iceout/
python3 package_apk.py
```

This script will bundle the `assets/` and `main.py` into `iceout.apk` and push it to the Vite `public/` directory.

### GitHub Pages Deployment

To enable `SharedArrayBuffer` threading for Pygame's WebAssembly canvas, the project uses `coi-serviceworker` to enforce Cross-Origin headers on GH Pages.
Deploy directly via npm:

```bash
npm run deploy
```

---
*Created per OPST Strategy Toolkit standard procedures.*
