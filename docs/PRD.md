# Product Requirements Document: Buzz's All-American Arcade & IceOut

## 1. Executive Summary

- **Problem Statement**: There is a need for a high-quality portfolio piece that simultaneously demonstrates professional frontend architecture, cross-technology integration (React + Python/WASM), and delivers an entertaining political statement via engaging gameplay.
- **Proposed Solution**: A web app wrapper called "Buzz's All-American Arcade" featuring a retro 80s / American Democracy theme, hosting embedded WebAssembly (WASM) games. The inaugural game is "IceOut", a custom Python Pygame CE module similar to Breakout with a political/family twist.
- **Success Criteria**:
  - The arcade wrapper is deployed to GitHub Pages successfully.
  - The embedded IceOut game maintains stable Framerates (targeting 30-60 FPS) via WASM.
  - No visual glitching or freezing during gameplay or navigation.
  - The project serves as an effective, high-quality portfolio link for hiring managers and investors.

## 2. User Experience & Functionality

### User Personas
1. **The Hiring Manager / Tech Lead ("Sarah")**: Looking to gauge technical stack proficiency, architecture, and deployment knowledge. Needs the app to load quickly, handle responsiveness well, and clearly demonstrate code structure.
2. **The Casual Player / Political Observer ("Marcus")**: Seeking light entertainment and a quick nostalgia hit. Wants immediate, intuitive gameplay without reading complex instructions.

### User Stories
- **As "Sarah"**, I want to navigate the arcade UI seamlessly and inspect the code architecture so that I can evaluate the developer's skill in integrating React and Python/WASM.
  - **AC**: The codebase is cleanly separated between React wrapper and Python module; GitHub Pages deployment performs without console errors.
- **As "Marcus"**, I want to play a responsive retro breakout game so that I am entertained by the theme and gameplay.
  - **AC**: The game loads instantly into an iframe, the paddle controls are tight, melting ice physics work correctly, and points are scored by hitting villains or freeing family members. 

### Game Rules (IceOut)
- **Player objective**: Use a paddle and ball to break translucent ice blocks.
- **Level Design**: 4 total levels.
- **Mechanics**: 
  - Instead of a traditional logo at the top during gameplay, a latino/latina family member "lives" above the ice cubes.
  - The ice cubes must be broken to free the family member.
  - When the ice breaks through to the family member, they escape down and off the screen for bonus points.
  - Every level contains a specific villain running across the mid-screen. Hitting the villain with the ball awards bonus points.
  - The ICEOUT logo is only shown during the "Attract" or "Game Over" mode, not during active gameplay.

### Non-Goals
- We are NOT building server-side logic (e.g., Node.js backend, PostGres databases, global leaderboards). All state must be client-side and ephemeral.
- We are NOT optimizing for mobile touch controls initially (Desktop-first approach).

## 3. Technical Specifications

- **Architecture Overview**:
  - **Frontend Wrapper**: React (via Vite), deployed as static files.
  - **Styling**: Vanilla CSS, relying on modern variable design systems to achieve glassmorphism and retro CRT effects.
  - **Game Engine**: Python 3 / Pygame CE compiled using `pygbag` into a WebAssembly (WASM) payload.
  - **Integration**: The compiled WASM game will be presented within an isolated `<iframe>` element inside the React wrapper. The iframe path will point to `/python_games/iceout/build/web/index.html`.
  
- **Integration Points**: 
  - The React app simply hosts static Pygame CE WASM output. There is no two-way data binding between the React parent and WASM child in the MVP.
  
- **Security & Privacy**:
  - No user data stored. The architecture requires 0 authentication or PII retention.

## 4. Risks & Roadmap

### Phased Rollout
- **MVP (Tonight)**: 
  - Basic React wrapper with Democracy/80s Retro theming.
  - Playable IceOut game built in Pygame CE (1 level functioning with ice blocks, one family member, one villain) loaded via Wasm.
  - Deployed to GitHub Pages.
- **v1.1**: Add remaining 3 levels (4 total), progressive difficulty (faster ball, more ice). 
- **v2.0**: High score local storage, sound effects, and adding extra game cabinets to the arcade.

### Technical Risks
- **WASM Performance**: The payload size of Python/Pygame WASM can lead to slow initial loads.
- **GitHub Pages Limits**: We need to ensure the correct relative routing for Vite builds (`base: "/buzz-arcade"`) combined with correctly referencing the WASM asset bundle paths.
