from dataclasses import dataclass, field
import random
import string
from typing import List, Set, Tuple

MAX_LIVES = 7
MAX_HINTS = 3
MASKABLE = set(string.ascii_uppercase)

BASIC_WORDS = [
    "apple", "banana", "orange", "grape", "melon", "mango", "peach",
    "cherry", "lemon", "strawberry", "carrot", "tomato", "potato",
    "onion", "garlic", "pepper", "broccoli", "cabbage", "spinach",
    "bread", "milk", "cheese", "butter", "egg", "rice", "pasta",
    "soup", "coffee", "tea", "water", "juice", "cookie", "cake",
    "chocolate", "icecream", "sandwich", "pizza", "burger", "noodle",
    "train", "bus", "car", "bicycle", "motorbike", "airport", "station",
    "school", "office", "market", "hospital", "bank", "park", "library",
    "house", "apartment", "kitchen", "bedroom", "bathroom", "garden",
    "computer", "phone", "camera", "television", "radio", "clock",
    "watch", "umbrella", "pencil", "pen", "notebook", "book", "bag"
]

INTERMEDIATE_PHRASES = [
    "unit testing",
    "test driven development",
    "clean code",
    "object oriented programming",
    "software engineering",
    "data structures and algorithms",
    "exception handling",
    "continuous integration",
    "code review",
    "version control",
    "typing annotations",
    "random access memory",
    "graph traversal"
]

@dataclass
class GameState:
    answer: str
    lives: int = MAX_LIVES
    guessed_letters: Set[str] = field(default_factory=set)
    wrong_letters: List[str] = field(default_factory=list)
    won: bool = False
    lost: bool = False
    hints_used: int = 0
    points: int = 0  # for scoring

    def masked_answer(self) -> str:
        res = []
        for ch in self.answer:
            up = ch.upper()
            if up in MASKABLE:
                res.append(ch if up in self.guessed_letters else "_")
            else:
                res.append(ch)
        return "".join(res)

    def reveal_all_if_won(self):
        for ch in self.answer:
            up = ch.upper()
            if up in MASKABLE and up not in self.guessed_letters:
                return
        self.won = True

    def can_use_hint(self):
        return self.hints_used < MAX_HINTS and self.lives > 1

class HangmanEngine:
    def __init__(self, level: str = "basic", lives: int = MAX_LIVES, rng: random.Random | None = None):
        self.level = level.lower()
        self.lives = lives
        self.rng = rng or random.Random()

    def _choose_answer(self) -> str:
        if self.level == "basic":
            return self.rng.choice(BASIC_WORDS).upper()
        else:
            return self.rng.choice(INTERMEDIATE_PHRASES).upper()

    def start(self, preset_answer: str | None = None) -> GameState:
        ans = (preset_answer or self._choose_answer()).upper()
        return GameState(answer=ans, lives=self.lives)

    def guess_letter(self, state: GameState, letter: str) -> Tuple[GameState, bool]:
        if state.won or state.lost:
            return state, False
        up = letter.upper()
        if not up.isalpha() or len(up) != 1:
            return state, False  # ignore invalid
        if up in state.guessed_letters or up in (l for l in state.wrong_letters if len(l) == 1):
            return state, up in state.guessed_letters
        if up in state.answer:
            state.guessed_letters.add(up)
            state.reveal_all_if_won()
            if state.won:
                state.points += 1  # gain point for correct word
            return state, True
        else:
            state.lives -= 1
            state.wrong_letters.append(up)
            if state.lives <= 0:
                state.lost = True
            return state, False

    def hint(self, state: GameState) -> str | None:
        if not state.can_use_hint():
            return None
        hidden = [ch for ch in state.answer if ch.upper() in MASKABLE and ch.upper() not in state.guessed_letters]
        if not hidden:
            return None
        reveal = self.rng.choice(hidden)
        state.guessed_letters.add(reveal.upper())
        state.lives -= 1
        state.hints_used += 1
        state.reveal_all_if_won()
        return reveal
