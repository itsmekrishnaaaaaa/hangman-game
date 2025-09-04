# 🎯 Hangman Game (Python)

A **fun and interactive Hangman game** implemented in Python with **Tkinter**. Features multiple difficulty levels, hints, a timer, scoring, and a graphical display of the Hangman. Tested thoroughly with **Pytest** for reliability.

---

## ⚡ Features

- **Difficulty Levels:**  
  - **Basic:** Common words  
  - **Intermediate:** Phrases and longer words  

- **Interactive GUI:**  
  - Animated hangman scaffold  
  - Lives displayed as hearts  
  - Wrong letters highlighted  
  - Timer countdown per guess  

- **Hints:**  
  - Reveal letters automatically  
  - Limited per round depending on word length  

- **Scoring System:**  
  - Points for correctly guessed words  
  - Lives decrease on wrong guesses or timeouts  

- **Tested Game Logic:**  
  - Unit tests using **Pytest**  
  - HTML test report generation  

---

## 📂 File Structure

```
hangman/
│
├── hangman.py          # Core Hangman logic
├── hangman_engine.py   # Advanced engine with scoring, hints, phrases
├── hangman_gui.pyw     # Tkinter GUI interface
├── test_hangman.py     # Unit tests with Pytest
├── report.html         # HTML test report(you can get yours by running the (pytest test_hangman.py))
└── README.md           # Project documentation
```

---

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/hangman-game.git
cd hangman-game
```

2. Install required Python packages:

```bash
pip install pytest
```

> Tkinter is included with standard Python distributions, no extra installation needed.

---

## 🎮 How to Play

1. Run the GUI:

```bash
python hangman_gui.pyw
```

2. Select **Basic** or **Intermediate** level.  
3. Enter a letter in the input box and press **Enter** or click **Guess**.  
4. Use the **Hint** button (limited per round) to reveal letters.  
5. Timer counts down from 15 seconds per guess; losing time costs a life.  
6. Win by guessing all letters, or lose when all lives are gone.  
7. Track your **score** on the side panel.  

---

## 🧪 Testing

Run unit tests with **Pytest**:

```bash
pytest test_hangman.py --html=report.html --self-contained-html -v
```

- Generates a **detailed HTML report** (`report.html`)  
- Verifies correct game logic for guesses, lives, hints, and win/lose conditions  

---

## 🔍 Game Logic Overview

| File | Purpose |
|------|---------|
| `hangman.py` | Basic Hangman class for guessing letters and tracking lives |
| `hangman_engine.py` | Advanced game engine: scoring, hints, phrases, win/loss tracking |
| `hangman_gui.pyw` | Tkinter GUI: visual scaffold, input, timer, score, and hints |
| `test_hangman.py` | Unit tests for game logic using Pytest |

---

## 💻 Dependencies

- Python 3.10+  
- Tkinter (standard in Python)  
- Pytest (for unit testing)  

---

## 🌟 Contribution

1. Fork the repository  
2. Create a branch: `git checkout -b feature-name`  
3. Make your changes  
4. Commit your changes: `git commit -m "Add feature"`  
5. Push to the branch: `git push origin feature-name`  
6. Open a Pull Request  

---

## 👤 Author

**Krishna Sapkota**  
- GitHub:https://github.com/itsmekrishnaaaaaa
- Email: Krishnasap547@gmail.com