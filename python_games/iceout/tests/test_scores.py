import os
import pygame
import pytest
from unittest.mock import patch, mock_open

# We have to mock pygame.init and font loading before importing main, 
# otherwise pygame tries to open a display head.
with patch('pygame.init'), patch('pygame.display.set_mode'), patch('pygame.font.Font'), patch('pygame.image.load'):
    import main

@pytest.fixture
def mock_scores_file(tmp_path):
    """Fixture to provide a temporary file path for highscores."""
    test_file = tmp_path / "test_highscores.txt"
    with patch('main.SCORES_FILE', str(test_file)):
        yield test_file

def test_load_scores_empty(mock_scores_file):
    assert main.load_scores() == []

def test_load_scores_corrupted(mock_scores_file):
    mock_scores_file.write_text("AAA,100\nGARBAGE_LINE\nBBB,50\n")
    scores = main.load_scores()
    assert len(scores) == 2
    assert scores[0] == ("AAA", 100)
    assert scores[1] == ("BBB", 50)

def test_load_scores_sorts_descending(mock_scores_file):
    mock_scores_file.write_text("AAA,100\nCCC,300\nBBB,200\n")
    scores = main.load_scores()
    assert scores == [("CCC", 300), ("BBB", 200), ("AAA", 100)]

def test_save_score_caps_at_10(mock_scores_file):
    # Populate 10 scores
    lines = [f"A{i},{i*10}\n" for i in range(10)]
    mock_scores_file.write_text("".join(lines))
    
    # Save a new high score
    main.save_entry("NEW", 999)
    
    scores = main.load_scores()
    assert len(scores) == 10
    assert scores[0] == ("NEW", 999)
    # The lowest score (A0, 0) should have been pushed out
    assert ("A0", 0) not in scores

def test_is_top_10(mock_scores_file):
    assert main.is_top_10(500) == True  # Empty list -> True
    
    lines = [f"A{i},{i*100}\n" for i in range(1, 11)] # 100 to 1000
    mock_scores_file.write_text("".join(lines))
    
    assert main.is_top_10(50) == False   # Less than min (100)
    assert main.is_top_10(150) == True   # Greater than min (100)
