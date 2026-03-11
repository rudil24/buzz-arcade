# Team Retro: Truth Evaders

**Date:** 2026-03-11

## 1. What went well

**Cap (Lead Architect / Team Lead):**
- **WASM High Score Persistence:** Successfully identified that Python flat-file I/O only targets temporary MemFS in Pygbag. Engineered a Javascript bridge using `platform.window.localStorage` that flawlessly persists High Scores into the browser cache for both games.
- **Architecture Reuse:** Seamlessly matched `iceout`'s asynchronous state machine loop for the new `truth-evaders` mechanics. This resulted in a much cleaner, more predictable Pygbag deployment process overall.
- **Audio Integration:** Successfully added custom sound effects and macOS TTS generated villain phrases natively into Pygame without crashing the WebAssembly canvas.

**Stella (UI/UX):**
- **Art Direction & Workflow:** Leveraged the `Stitch MCP` to generate accurate, custom 16-bit pixel-art busts for the villains (Pam Bondi, Ghislaine Maxwell) directly inside Antigravity. This completely resolved the art generation bottleneck and quality issues experienced during the Ice Out project!

**Vera (QA/DevOps):**
- **State Flow Parity:** Mirrored the `iceout` Game Over / High Score transition sequence to ensure both games have a unified UX flow. The player is always returned to a central Start screen displaying the Top 5 scores.

__Rudi (Owner):__

- The graphic creation was much smoother in the implementation plan, and I credit Google Stitch MCP integration for that but correct me if i'm wrong
- The audio creation using native macos tools was perfect for this retro game, thanks team for finding that!
- The sharing of techniques between the two games was great, the team was able to learn and apply things to this game from the first game, and vice versa


## 2. What went wrong

**Cap (Lead Architect / Team Lead):**
- **Asset Loading Race Conditions:** The initial Pygbag asset loader crashed silently due to nested asynchronous yields mixed with `.convert_alpha()`. It turns out synchronous loading is absolutely required for reliability in the Pygbag MemFS pipeline.
- **Linting vs. Typing:** We encountered numerous Pyre2 lint errors related to object types and Pygame attribute inferring. We spent time looking at them but they cluttered the IDE feedback without providing critical blocking issues.

**Vera (QA/DevOps):**
- **Incomplete Top 10 Display:** Initially, `truth-evaders` only displayed the #1 high score despite asking for top 10 tracking. We had to go back and explicitly loop through the array on the UI layer.

__Rudi (owner)__

- we kept losing Cap persona in the agent window (he would revert to AG Agent) and even when Cap was there he was skipping steps on skills he usually nails, like retro skill. 
- admittedly this was a long thread we probably should be compounding / starting new threads when we get this long

## 3. What did we discover

**Cap (Lead Architect / Team Lead):**
- **Browser Persistence:** `platform.window.localStorage` is the only reliable way to persist data between sessions in Pygbag. The local `open('file', 'w')` method writes strictly to session-volatile memory.
- **Pygbag MemFS Loading:** The `.apk` memory filesystem provided by Pygbag requires synchronous `pygame.image.load()` calls. Trying to yield via `asyncio.sleep(0)` during loading causes race conditions and canvas crashes if surface methods like `.convert_alpha()` are called before the data is ready.

__Rudi (Owner):__
- adding audio to games is a big improvement and not that hard to do with the team.
- british speaking voices weren't really british from the macos tools, i had to put in sounds-like words to make that work "Pahdon May"
- games always need fixing / improving i have a new list of like 10 things we can improve for a next version!