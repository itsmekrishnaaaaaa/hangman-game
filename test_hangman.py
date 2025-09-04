# test_hangman.py
import pytest
from hangman import Hangman

def test_correct_guess_reveals_letter():
    game = Hangman("apple")
    result = game.guess("a")
    assert result is True
    assert game.get_display_word() == "a____"

def test_wrong_guess_reduces_life():
    game = Hangman("apple")
    result = game.guess("z")
    assert result is False
    assert game.lives == 6

def test_guess_reveals_multiple_occurrences():
    game = Hangman("apple")
    game.guess("p")
    assert game.get_display_word() == "_pp__"

def test_phrase_with_spaces():
    game = Hangman("hello world")
    assert game.get_display_word() == "_____ _____"
    game.guess("o")
    assert game.get_display_word() == "____o _o___"

def test_invalid_input_does_not_change_state():
    game = Hangman("apple")
    game.guess("1")
    assert game.get_display_word() == "_____"
    assert game.lives == 7

def test_repeated_guess_does_not_penalize():
    game = Hangman("apple")
    game.guess("a")
    lives_before = game.lives
    game.guess("a")
    assert game.lives == lives_before

def test_game_won_condition():
    game = Hangman("hi")
    game.guess("h")
    game.guess("i")
    assert game.is_won() is True
    assert game.is_game_over() is True

def test_game_over_condition():
    game = Hangman("hi")
    wrong_letters = ["z", "x", "q", "v", "b", "m", "n"]
    for letter in wrong_letters:
        game.guess(letter)
    assert game.lives == 0
    assert game.is_game_over() is True

if __name__ == "__main__":
    # Run pytest and generate HTML report
    pytest.main([
        "test_hangman.py",      # file to test
        "-v",                   # verbose output in terminal
        "--html=report.html",   # generate HTML report
        "--self-contained-html" # include CSS in HTML for portability
    ])
