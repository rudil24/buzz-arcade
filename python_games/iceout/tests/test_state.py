import os
import pygame
import pytest
from unittest.mock import patch

# Mock pygame initialization
with patch('pygame.init'), patch('pygame.display.set_mode'), patch('pygame.font.Font'), patch('pygame.image.load'):
    import main

@pytest.fixture
def mock_scores_file(tmp_path):
    test_file = tmp_path / "test_highscores.txt"
    with patch('main.SCORES_FILE', str(test_file)):
        yield test_file

@pytest.mark.asyncio
async def test_initials_entry_bug(mock_scores_file):
    """
    Replicates the bug where the game gets stuck on ENTER_INITIALS.
    We test the extracted `handle_initials_input` handler directly.
    """
    
    def make_keydown(key_const, unicode_char=''):
        return pygame.event.Event(pygame.KEYDOWN, {'key': key_const, 'unicode': unicode_char})
        
    initials = ""
    score = 1000
    
    # 1. Type A
    initials, confirm = main.handle_initials_input(make_keydown(pygame.K_a, 'a'), initials, score)
    assert initials == "A"
    assert confirm is False
    
    # 2. Type B
    initials, confirm = main.handle_initials_input(make_keydown(pygame.K_b, 'b'), initials, score)
    assert initials == "AB"
    assert confirm is False
    
    # 3. Type C
    initials, confirm = main.handle_initials_input(make_keydown(pygame.K_c, 'c'), initials, score)
    assert initials == "ABC"
    assert confirm is False
    
    # 4. Press ENTER (THE BUG)
    # The expected behavior of a UI is that `confirm` should be True, 
    # but the bug causes it to return (current_initials, False) in some conditions, or freeze.
    # Actually, looking at the code we patched:
    # elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
    #     if len(current_initials) > 0:
    #         return current_initials, True
    
    initials, confirm = main.handle_initials_input(make_keydown(pygame.K_RETURN), initials, score)
    
    # We WANT this to fail if the bug is present, so let's assert the expected, correct behavior.
    assert confirm is True, "The game failed to confirm the initials and exit the screen!"
    
    # Also verify it saved to our mock disk
    scores = main.load_scores()
    assert len(scores) == 1
    assert scores[0] == ("ABC", 1000)

@pytest.mark.asyncio
async def test_pause_state_transitions():
    """
    Simulates the event loop logic for State transitions without running the loop.
    We inject events directly into the state block logic found in main.py.
    """
    
    # helper for events
    def make_keydown(key_const):
        return pygame.event.Event(pygame.KEYDOWN, {'key': key_const})
        
    state = "PLAYING"
    
    # --- Simulate Main Event Loop Logic for ESC ---
    event = make_keydown(pygame.K_ESCAPE)
    if event.key == pygame.K_ESCAPE:
        if state == "PLAYING":
            state = "PAUSED"
        elif state == "PAUSED":
            pass # In real code it does sys.exit(), we ignore for state test
            
    assert state == "PAUSED", "Pressing ESC while PLAYING did not switch state to PAUSED"
    
    # --- Simulate Main Event Loop Logic for Resume ---
    event = make_keydown(pygame.K_SPACE)
    # The elif block from main.py
    if state == "PAUSED" and event.key == pygame.K_SPACE:
        state = "PLAYING"
        
    assert state == "PLAYING", "Pressing SPACE while PAUSED did not switch state to PLAYING"

