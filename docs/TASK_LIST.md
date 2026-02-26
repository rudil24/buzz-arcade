# Buzz-Arcade Development Task List

## Documentation
- [x] Verify project intent with PO (Discovery Phase).
- [x] Define User Personas.
- [x] Generate UI mockups and establish aesthetic direction.
- [x] Write PRD (`docs/PRD.md`).
- [x] Write Design Doc (`docs/Design.md`).

## Phase 1: Arcade Wrapper (React)
- [ ] Initialize Vite/React project base (Done previously but reset).
- [ ] Apply global CSS matching the "Democracy/Retro" theme (`index.css` & `App.css`).
- [ ] Implement Concourse UI components (Header, Game Selector, Cabinet Cards).
- [ ] Implement generic Game Screen iframe shell with CRT CSS effects.

## Phase 2: Game Logic ("IceOut")
- [ ] Initialize Pygame CE environment.
- [ ] Set up main game loop (`main.py`) matching vertical aspect ratio (e.g., 600x800).
- [ ] Load and integrate asset paths (Villains from `assets/iceout/`).
- [ ] Implement Paddle logic and Ball physics.
- [ ] Implement translucent melting ice blocks array.
- [ ] Implement Family Member entity (walking above ice, falling when ice breaks).
- [ ] Implement Villain entity (random horizontal run, ball collision logic).
- [ ] Score and level management logic (4 progressive levels).

## Phase 3: WebAssembly (WASM) Compilation
- [ ] Set up `pygbag` build step.
- [ ] Compile Python module to WASM web format.
- [ ] Validate WASM payload runs properly under local environment serving.
- [ ] Integrate WASM payload folder into React `public/` directory so the iframe resolves correctly during Vite builds.

## Phase 4: Production Deployment
- [ ] Configure `vite.config.js` with correct `base: "/buzz-arcade/"`.
- [ ] Add deployment scripts (`gh-pages`) to `package.json`.
- [ ] Run build and deploy wrapper + game to GitHub Pages.
- [ ] Perform final manual testing and FPS verification on live URL.
