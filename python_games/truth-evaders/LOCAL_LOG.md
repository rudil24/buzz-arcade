# LOCAL_LOG.md

## Scope & Design

- **Concepting**: Generated visual mockups for Truth Evaders to identify the art direction.
- **Villains**: Iterated and finalized head/bust pixel artwork for "Pam Bondi" and "Ghislaine Maxwell" assets to function as top-row bonus targets.
- **Kickoff**: Agent Cap initialized OPST protocol. Tech Stack identified as Python/Pygame (WASM compatible, mimicking existing Pygbag `iceout` architecture).
- **Environment**: Google Antigravity (IDE).
- **Process**: Adhering to OPST Review-Driven Development.

## Development & Testing

- **Core Loop**: Established Pygame scaffolding, `asyncio` main loop, and player inputs.
- **Graphic Polish**: Replaced initial sketch-style aliens with distinct procedural classic 8-bit pixel-art aliens (Squid, Crab, Octopus). Added custom red, white, and blue pixel sprite for the player's tank.
- **Villain Pass**: Finalized villain "bobbing" animation and scrolling behavior across the top channel, resolving clipping issues with text bubbles.
- **Placard Mechanics**: Alien objects read from `assets/names.md`. Upon taking a hit from a player bullet, they drop their black redaction bar and reveal an Epstein list name in crisp, bold sans-serif font, moving alongside the pack indefinitely.
- **Combat Physics**: Enforced a 1-bullet-max constraint on the player. Integrated random enemy return fire logic.
- **Environment**: Added 4 destructible bases for the player to hide under. Resolved path loading logic so the `assets/` can be fetched accurately regardless of the terminal's working directory.
- **Audio Output**: Created a procedural python synthesizer to generate retro square/sine wave sound effects (`shot`, `rip`, `march`, `boss_hit`). Piped macOS's native `say` TTS engine through pitch-modulation flags to generate custom voices for the villain taunts. Introduced rigid state pacing delays to let the audio breathe.
- **End of Game**: Migrated persistent High Score memory architecture via `truth-evaders-scores.txt` and an `ENTER_INITIALS` state overlay loop. Fixed a cascading death bug by lifting the alien formation 150px away from the player's base upon respawning a new life.

## Deployment & Retro

- *Awaiting execution...*
