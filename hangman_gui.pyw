# hangman_gui.pyw
import tkinter as tk
from tkinter import messagebox
from hangman_engine import HangmanEngine, MAX_LIVES
import random

# Colors
BG_COLOR = "#f0f4f8"
WORD_COLOR = "#1b263b"
WRONG_COLOR = "#d62828"
CANVAS_BG = "#ffffff"
ACCENT_COLOR = "#0077b6"
LIMB_COLOR = "#264653"
HEAD_COLOR = "#ffcd94"
HEART_COLOR = "#e63946"

PARTS_ORDER = ["head", "torso", "left_arm", "right_arm", "left_leg", "right_leg"]


class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.config(bg=BG_COLOR)
        self.root.geometry("1100x600")
        self.root.minsize(900, 500)
        self.engine = None
        self.state = None
        self.level = None
        self.hangman_parts = {}
        self.score = 0
        self.time_left = 15
        self.timer_id = None
        self.used_hints = 0
        self.max_hints = 3
        self.create_start_screen()

    def create_start_screen(self):
        self.clear_root()
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(expand=True, fill="both")

        title = tk.Label(frame, text="🎯 Hangman Game", font=("Arial", 48, "bold"),
                         bg=BG_COLOR, fg=ACCENT_COLOR)
        title.pack(pady=30)

        tk.Label(frame, text="Select Level:", font=("Arial", 24),
                 bg=BG_COLOR, fg=WORD_COLOR).pack(pady=20)

        btn_frame = tk.Frame(frame, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Basic", font=("Arial", 20),
                  bg="#2a9d8f", fg="white",
                  command=lambda: self.start_game("basic"), width=12).pack(side=tk.LEFT, padx=20)

        tk.Button(btn_frame, text="Intermediate", font=("Arial", 20),
                  bg="#e76f51", fg="white",
                  command=lambda: self.start_game("intermediate"), width=15).pack(side=tk.LEFT, padx=20)

    def start_game(self, level):
        self.level = level
        self.engine = HangmanEngine(level=level, lives=MAX_LIVES)
        self.state = self.engine.start()
        self.hangman_parts.clear()

        # --- Hints setup ---
        if len(self.state.answer) <= 4:  # very short words -> only 1 hint
            self.max_hints = 1
        else:
            self.max_hints = 3
        self.used_hints = 0

        self.create_game_screen()
        self.draw_scaffold()
        self.draw_lives()
        self.update_display()
        self.time_left = 15
        self.update_timer()

    def create_game_screen(self):
        self.clear_root()
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left: Canvas for hangman
        self.canvas = tk.Canvas(main_frame, width=400, height=500,
                                bg=CANVAS_BG, highlightthickness=2,
                                highlightbackground=ACCENT_COLOR)
        self.canvas.pack(side=tk.LEFT, padx=20, fill="y")

        # Right: Word + input + wrong letters
        right_frame = tk.Frame(main_frame, bg=BG_COLOR)
        right_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=20)

        # Level indicator
        self.level_label = tk.Label(right_frame, text=f"Level: {self.level.capitalize()}",
                                    font=("Arial", 20, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR)
        self.level_label.pack(pady=10)

        # Word label
        self.word_label = tk.Label(right_frame, text="",
                                   font=("Arial", 40, "bold"),
                                   fg=WORD_COLOR, bg=BG_COLOR)
        self.word_label.pack(pady=40)

        # Wrong letters
        self.wrong_label = tk.Label(right_frame, text="",
                                    font=("Arial", 18, "italic"),
                                    fg=WRONG_COLOR, bg=BG_COLOR)
        self.wrong_label.pack(pady=10)

        # Input frame with Guess and Hint buttons
        input_frame = tk.Frame(right_frame, bg=BG_COLOR)
        input_frame.pack(pady=20)
        tk.Label(input_frame, text="Enter a Letter:", font=("Arial", 18),
                 bg=BG_COLOR, fg=WORD_COLOR).pack(side=tk.LEFT)

        self.guess_entry = tk.Entry(input_frame, font=("Arial", 22),
                                    width=2, justify="center")
        self.guess_entry.pack(side=tk.LEFT, padx=10)
        self.guess_entry.bind("<Return>", self.make_guess)
        self.guess_entry.bind("<KeyRelease>", self.limit_entry)
        self.guess_entry.focus()

        tk.Button(input_frame, text="Guess", font=("Arial", 18),
                  bg=ACCENT_COLOR, fg="white", command=self.make_guess).pack(side=tk.LEFT, padx=10)
        tk.Button(input_frame, text="Hint", font=("Arial", 18),
                  bg="#f4a261", fg="white", command=self.use_hint).pack(side=tk.LEFT, padx=10)

        # Timer and score
        self.timer_label = tk.Label(right_frame, text=f"Time left: {self.time_left}s",
                                    font=("Arial", 18), bg=BG_COLOR)
        self.timer_label.pack(pady=10)

        self.score_label = tk.Label(right_frame, text=f"Score: {self.score}",
                                    font=("Arial", 18), bg=BG_COLOR)
        self.score_label.pack(pady=10)

        self.hint_label = tk.Label(right_frame, text=f"Hints left: {self.max_hints - self.used_hints}",
                                   font=("Arial", 18), bg=BG_COLOR, fg="#6a4c93")
        self.hint_label.pack(pady=5)

        # Play Again and Go Back buttons
        self.play_again_btn = tk.Button(right_frame, text="Continue",
                                        font=("Arial", 20), bg="#06d6a0",
                                        fg="white", command=self.play_next)
        self.play_again_btn.pack(pady=20)
        self.play_again_btn.pack_forget()

        self.go_back_btn = tk.Button(right_frame, text="Go Back to Menu",
                                     font=("Arial", 16), bg="#ef476f",
                                     fg="white", command=self.go_back_to_menu)
        self.go_back_btn.pack(pady=10)

    def limit_entry(self, event):
        text = self.guess_entry.get()
        if len(text) > 1:
            self.guess_entry.delete(1, tk.END)

    def make_guess(self, event=None):
        guess = self.guess_entry.get().strip().upper()
        self.guess_entry.delete(0, tk.END)
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Enter only one letter A-Z!")
            return

        _, correct = self.engine.guess_letter(self.state, guess)
        if not correct:
            self.draw_next_part()
        self.update_display()
        self.check_game_over()
        self.time_left = 15  # reset timer after valid guess

    # --- Hint button ---
    def use_hint(self):
        if self.state.lives <= 0:
            messagebox.showwarning("No Lives", "You have no lives left to use a hint!")
            return

        if self.used_hints >= self.max_hints:
            messagebox.showinfo("Hint Limit", f"You can only use {self.max_hints} hint(s) this round!")
            return

        remaining_letters = [ch for ch in self.state.answer if ch not in self.state.guessed_letters]
        if not remaining_letters:
            messagebox.showinfo("Hint", "No letters left to reveal!")
            return

        # Reveal one letter randomly
        hint_letter = random.choice(remaining_letters)
        self.engine.guess_letter(self.state, hint_letter)
        self.state.lives -= 1
        self.used_hints += 1

        messagebox.showinfo("Hint Used", f"Hint revealed: {hint_letter}\nHints used: {self.used_hints}/{self.max_hints}")

        self.draw_next_part()
        self.update_display()
        self.check_game_over()
        self.time_left = 15  # reset timer after hint

    # --- Timer function ---
    def update_timer(self):
        if self.state.won or self.state.lost:
            return

        self.timer_label.config(text=f"Time left: {self.time_left}s")

        if self.time_left <= 0:
            # Lose 1 life instead of instant game over
            self.state.lives -= 1
            self.draw_next_part()
            self.update_display()

            if self.state.lives <= 0:
                self.state.lost = True
                self.check_game_over()
                return
            else:
                messagebox.showinfo("⏰ Time's Up!", "You ran out of time! One life lost.")
                self.time_left = 15  # reset timer
        else:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)

    def update_display(self):
        self.word_label.config(text=" ".join(self.state.masked_answer()))
        wrong_text = "Wrong: " + ", ".join(self.state.wrong_letters) if self.state.wrong_letters else "Wrong: None"
        self.wrong_label.config(text=wrong_text)
        self.score_label.config(text=f"Score: {self.score}")
        self.hint_label.config(text=f"Hints left: {self.max_hints - self.used_hints}")
        self.draw_lives()

    def draw_scaffold(self):
        c = self.canvas
        c.delete("all")
        c.create_line(50, 480, 350, 480, width=4)
        c.create_line(100, 480, 100, 50, width=4)
        c.create_line(100, 50, 250, 50, width=4)
        c.create_line(250, 50, 250, 120, width=4)

    def draw_lives(self):
        self.canvas.delete("hearts")
        lives = self.state.lives
        if lives < 0:
            lives = 0

        self.root.update_idletasks()
        canvas_width = max(int(self.canvas.winfo_width()), 400)
        spacing = max(canvas_width // (MAX_LIVES + 1), 50)
        y = 30

        for i in range(lives):
            x = (i + 1) * spacing
            self.canvas.create_oval(x - 10, y - 10, x, y, fill=HEART_COLOR,
                                    outline=HEART_COLOR, tags="hearts")
            self.canvas.create_oval(x, y - 10, x + 10, y, fill=HEART_COLOR,
                                    outline=HEART_COLOR, tags="hearts")
            self.canvas.create_polygon(x - 10, y, x + 10, y, x, y + 15,
                                       fill=HEART_COLOR, outline=HEART_COLOR, tags="hearts")

    def draw_next_part(self):
        c = self.canvas
        index = MAX_LIVES - self.state.lives - 1
        if index < 0 or index >= len(PARTS_ORDER):
            return
        part = PARTS_ORDER[index]

        if part == "head":
            self.hangman_parts["head"] = c.create_oval(215, 120, 285, 190,
                                                       fill=HEAD_COLOR, outline=LIMB_COLOR, width=2)
            self.hangman_parts["eye1"] = c.create_oval(235, 140, 245, 150, fill="black")
            self.hangman_parts["eye2"] = c.create_oval(255, 140, 265, 150, fill="black")
            self.hangman_parts["mouth"] = c.create_line(235, 170, 265, 170, width=3)
        elif part == "torso":
            self.hangman_parts["torso"] = c.create_line(250, 190, 250, 310, width=8, fill=LIMB_COLOR)
        elif part == "left_arm":
            self.hangman_parts["left_arm"] = c.create_line(250, 210, 200, 260, width=6, fill=LIMB_COLOR)
        elif part == "right_arm":
            self.hangman_parts["right_arm"] = c.create_line(250, 210, 300, 260, width=6, fill=LIMB_COLOR)
        elif part == "left_leg":
            self.hangman_parts["left_leg"] = c.create_line(250, 310, 210, 390, width=6, fill=LIMB_COLOR)
        elif part == "right_leg":
            self.hangman_parts["right_leg"] = c.create_line(250, 310, 290, 390, width=6, fill=LIMB_COLOR)

    def check_game_over(self):
        if self.state.won:
            self.score += 1
            self.canvas.delete(self.hangman_parts.get("mouth"))
            self.canvas.create_arc(230, 160, 270, 190, start=180, extent=180,
                                   style="arc", width=3)
            messagebox.showinfo("🎉 Victory!", f"You saved the little guy!\nWord: {self.state.answer}\nScore: {self.score}")
            self.play_again_btn.pack()
        elif self.state.lost:
            self.canvas.delete(self.hangman_parts.get("mouth"))
            self.canvas.create_arc(230, 170, 270, 190, start=0, extent=180,
                                   style="arc", width=3)
            messagebox.showinfo("💀 Game Over", f"Time's up or lives finished!\nWord: {self.state.answer}\nScore: {self.score}")
            self.play_again_btn.pack()
            if self.timer_id:
                self.root.after_cancel(self.timer_id)

    def play_next(self):
        self.play_again_btn.pack_forget()
        self.start_game(self.level)

    def go_back_to_menu(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.create_start_screen()

    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
