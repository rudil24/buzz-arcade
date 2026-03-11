# Retrospective: Truth Evaders (WebAssembly Arcade)

__Date:__ 2026-03-11
__Scope:__ Truth Evaders game development, WebAssembly integration, high score persistence, and Ice Out debugging.

## Summary
The OPST successfully developed the "Truth Evaders" space-invaders clone, integrated it into the React wrapper, and deployed it to GitHub Pages alongside "Ice Out", solving critical WASM data persistence and sprint loading bugs in the process.

## What Went Well
- **Stitch MCP Art:** High-quality pixel art generation was extremely smooth using the native Google Stitch MCP.
- **WASM Persistence:** Successfully engineered a Javascript `window.localStorage` bridge to fix the volatile High Score saving in Pygbag.
- **Audio Additions:** Added native macOS TTS audio and retro sound effects, vastly improving the game feel.
- **Ecosystem Cross-pollination:** Smoothly shared UX and architectural patterns between `iceout` and `truth-evaders`.

## What Could Be Improved
- **Process Adherence:** The conversation thread became too long, leading to persona degradation and skipping the official OPST Retro Skill steps.
- **Race Conditions:** Encountered silent Pygbag crashes due to asynchronous `.convert_alpha()` calls on images before MemFS properly loaded them.
- **Voice Tuning:** macOS TTS voices required phonetic string hacking ("Pahdon May") to simulate specific accents.

## Learnings Extracted
- L7: Google Stitch MCP for Pixel Art Integration
- L8: macOS Native TTS for Retro Audio
- L9: Knowledge Transfer Between Micro-Games
- L10: Thread Longevity and Persona Degradation
- L11: Pygbag Persistence Requirements
- L12: Pygbag MemFS Loading Race Conditions

See: `.agents/learnings/2026-03-11-truth-evaders.md`

## Action Items
- [ ] Incorporate `platform.window.localStorage` standard API wrappers into all future Pygbag prototypes.
- [ ] Start new conversation threads for future game modules to prevent persona context loss.
- [ ] Review the PO's new 10-item improvement list for the next version.
