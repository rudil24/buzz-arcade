# Learning: Google Stitch MCP for Pixel Art Integration

__ID__: L7
__Category__: ui/ux
__Confidence__: high

## What We Learned

Integrating Google Stitch MCP directly inside the Antigravity IDE is a highly effective, low-friction method for generating pristine 16-bit pixel-art assets (like the character busts) without relying on external art tools or clunky image filters.

## Why It Matters

It drastically speeds up the art pipeline for retro games and ensures consistent, authentic aesthetic quality out-of-the-box.

## Source

Truth Evaders retro, implementing Pam Bondi and Ghislaine Maxwell graphics.

---

# Learning: macOS Native TTS for Retro Audio

__ID__: L8
__Category__: audio
__Confidence__: high

## What We Learned

Using the native macOS `say` command is a fast, effective tool for generating retro-sounding vocal audio clips. Achieving specific accents (like British) requires phonetic spelling (e.g., "Pahdon May") rather than standard text.

## Why It Matters

Adding audio drastically improves the retro arcade "vibe" and can be accomplished smoothly without needing professional voice actors or complex audio software.

## Source

Truth Evaders retro, adding voice lines to villain targets.

---

# Learning: Knowledge Transfer Between Micro-Games

__ID__: L9
__Category__: process
__Confidence__: high

## What We Learned

Architectural fixes and UX patterns established in one mini-game (like Ice Out's Pygbag async loop or Truth Evaders' localStorage bridge) must be systematically shared and enforced across all games in the arcade ecosystem.

## Why It Matters

It ensures a unified user experience and prevents solving the same WebAssembly bugs multiple times.

## Source

Truth Evaders retro, transferring Pygbag knowledge between `iceout` and `truth-evaders`.

---

# Learning: Thread Longevity and Persona Degradation

__ID__: L10
__Category__: process
__Confidence__: high

## What We Learned

Extremely long context threads lead to AI persona degradation (losing the "Cap" persona) and missed procedural steps (like failing to automatically run the OPST Retro skill). 

## Why It Matters

To maintain high-quality OPST orchestration and strict skill adherence, large projects must be broken into multiple, smaller Antigravity conversation threads.

## Source

Truth Evaders retro, Product Owner feedback on missing retro steps.

---

# Learning: Pygbag Persistence Requirements

__ID__: L11
__Category__: architecture
__Confidence__: high

## What We Learned

Standard Python `open()` commands write to a volatile MemFS in Pygbag. To persist save data (like high scores) across browser sessions, the game must use a `platform.window.localStorage.setItem()` Javascript bridge.

## Why It Matters

Without this bridge, all user progress is lost upon browser refresh, ruining the arcade experience.

## Source

Truth Evaders retro, debugging High Score amnesia.

---

# Learning: Pygbag MemFS Loading Race Conditions

__ID__: L12
__Category__: architecture
__Confidence__: high

## What We Learned

Pygbag's Memory File System requires assets to be loaded synchronously (`pygame.image.load`). Attempting to use `asyncio.sleep(0)` within the asset loader causes race conditions that crash `.convert_alpha()` operations.

## Why It Matters

Ensures WebAssembly arcade games successfully mount their sprites without silent crashes or black-square artifacts.

## Source

Truth Evaders retro, fixing Ice Out's initialization freeze.
