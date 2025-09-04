# hangman.py
import string

MAX_LIVES = 7
MASKABLE = set(string.ascii_lowercase)

class Hangman:
    def __init__(self, answer, lives=MAX_LIVES):
        self.answer = answer.lower()
        self.lives = lives
        self.guessed_letters = set()
        self.wrong_letters = []

    def guess(self, letter):
        letter = letter.lower()
        if not letter.isalpha() or len(letter) != 1:
            return False
        if letter in self.guessed_letters or letter in self.wrong_letters:
            return True
        if letter in self.answer:
            self.guessed_letters.add(letter)
            return True
        else:
            self.lives -= 1
            if self.lives < 0:
                self.lives = 0
            self.wrong_letters.append(letter)
            return False

    def get_display_word(self):
        return "".join(
            ch if ch in self.guessed_letters or ch not in MASKABLE else "_"
            for ch in self.answer
        )

    def is_won(self):
        return all(ch in self.guessed_letters or ch not in MASKABLE for ch in self.answer)

    def is_game_over(self):
        return self.lives == 0 or self.is_won()
