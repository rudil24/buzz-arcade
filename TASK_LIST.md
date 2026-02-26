# OPST Task List

__Project:__ buzz-arcade
__Phase:__ Quality Assurance & Test Initialization
__Assigned To:__ Vera (QA/DevOps)

## Overview
Test coverage is currently non-existent for the initial Python game logic (`Ice Out`) and the Vite wrapper. The Antigravity Browser tool natively works again (v1.19.5). Vera must establish baseline tests for stability, behavioral correctness, and browser integration.

## Testing Strategy & Coverage Goals

Per Vera's Core Directive #2: *Always identify the highest-risk component in the project... and ensure it receives the most test coverage. For UI-driven apps, this is typically the core interaction layer (input handlers, state machines, event flows), not the data layer.*

For an arcade game like this, striving for an arbitrary 100% line coverage is counter-productive because testing the Pygame `draw()` loops headless is flaky and provides low value.
__Vera's Coverage Goal: 100% of State Transitions and Data Logic.__ 
This means we will test the state machine (Start -> Playing -> Paused -> Game Over), the event handlers (keyboard inputs simulating gameplay/menu choices), and the data layer (high scores). We deliberately exclude the frame-by-frame rendering loops from strict coverage metrics.

## Tasks for Vera

- [x] __Task 1: Unit Test High Score & Initials Logic__
  - Create a Python test suite (e.g., `tests/test_scores.py` or `python_games/iceout/tests/`) using `unittest` or `pytest`.
  - Mock file I/O to verify `load_scores()` appropriately handles missing, corrupted, and valid `highscores.txt` files.
  - Verify `save_score(score)` strictly caps at the top 10 scores and sorts them in descending order.
  - **CRITICAL BUG HUNT:** Write a specific behavioral test that mocks entering 3 initials and pressing the `ENTER` / `RETURN` key. The current bug is that the game gets "stuck" and does not let the player past the "enter" state after the initials have been typed. Establish a failing test for this specific freeze before fixing it.

- [x] __Task 2: Behavioral Testing of Game State Transitions__
  - Utilize programmatic event simulation (as per Vera's directives) to test `main.py` state machines natively in Python without requiring a Pygame display head.
  - Send artificial `KEYDOWN` events for the `ESC` key during the `PLAYING` state to ensure the game correctly transitions to `PAUSED`.
  - Send artificial `SPACE` key events while `PAUSED` to ensure the game transitions back to `PLAYING`.

- [x] __Task 3: Automated Browser Testing (End-to-End)__
  - Utilize the functional Antigravity browser tool to launch the `vite` dev server locally.
  - Automate a process to open the browser, navigate to the `Ice Out` game wrapper iframe, and verify that the canvas element mounts without `ERR_BLOCKED_BY_RESPONSE` errors.
  - Verify visually (or via DOM state) that the WASM bundle successfully unpacks and launches the START screen.
  - This is the final verification step necessary before deploying to GitHub Pages.

- [x] __Task 4: Deliver Final Coverage Report__
  - Generate a formal coverage report (`coverage.py` or `pytest-cov`) for the Python backend.
  - Present the report, documenting what was tested (State, Logic, I/O) versus what was omitted (Rendering).
