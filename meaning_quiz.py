import tkinter as tk
from tkinter import ttk, messagebox
import random


class MeaningQuiz:
    def __init__(self, root, db, selected_lists, return_callback):
        self.root = root
        self.db = db
        self.selected_lists = selected_lists
        self.return_callback = return_callback

        # Quiz state
        self.words = self.db.get_lists(selected_lists)
        random.shuffle(self.words)
        self.current_index = 0
        self.score = 0
        self.correct_answers = []
        self.incorrect_answers = []

        # UI elements
        self.choice_buttons = []
        self.current_correct_letter = None

        # Clear window and setup UI
        self.clear_window()
        self.setup_ui()
        self.show_question()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_ui(self):
        """Setup meaning test UI"""
        self.container = ttk.Frame(self.root, padding="30")
        self.container.pack(fill='both', expand=True)

        # Header with Exit button
        header_frame = ttk.Frame(self.container)
        header_frame.pack(fill='x', pady=(0, 20))

        # Title on the left
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side='left', fill='x', expand=True)

        ttk.Label(title_frame,
                  text="Meaning Test",
                  font=('Arial', 20, 'bold')).pack(anchor='w')

        self.progress_label = ttk.Label(title_frame,
                                        text="",
                                        font=('Arial', 12))
        self.progress_label.pack(anchor='w', pady=5)

        # Exit button on the right
        ttk.Button(header_frame,
                   text="✕ Exit Quiz",
                   command=self.exit_quiz).pack(side='right')

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.container,
                                            length=400,
                                            mode='determinate')
        self.progress_bar.pack(pady=10)

        # Word display
        word_frame = ttk.Frame(self.container)
        word_frame.pack(pady=20)

        ttk.Label(word_frame,
                  text="Word:",
                  font=('Arial', 12, 'bold')).pack()

        self.word_label = ttk.Label(word_frame,
                                    text="",
                                    font=('Arial', 24, 'bold'),
                                    foreground='#2c3e50')
        self.word_label.pack(pady=10)

        self.pos_label = ttk.Label(word_frame,
                                   text="",
                                   font=('Arial', 12, 'italic'),
                                   foreground='#7f8c8d')
        self.pos_label.pack()

        # Choices frame
        self.choices_frame = ttk.Frame(self.container)
        self.choices_frame.pack(expand=True, fill='both', pady=15)

        ttk.Label(self.choices_frame,
                  text="Select the correct definition:",
                  font=('Arial', 12)).pack(pady=(0, 10))

        # Feedback label
        self.feedback_label = ttk.Label(self.container,
                                        text="",
                                        font=('Arial', 13, 'bold'))
        self.feedback_label.pack(pady=5)

    def show_question(self):
        """Display current question with multiple choices"""
        if self.current_index < len(self.words):
            word = self.words[self.current_index]

            # Update progress
            progress_text = f"Question {self.current_index + 1} of {len(self.words)}"
            self.progress_label.config(text=progress_text)
            self.progress_bar['maximum'] = len(self.words)
            self.progress_bar['value'] = self.current_index

            # Display word
            self.word_label.config(text=word['word'])
            self.pos_label.config(text=f"({word['pos']})")

            # Generate choices
            choices = self.generate_choices(word)

            # Clear previous choices
            for widget in self.choices_frame.winfo_children()[1:]:  # Keep the label
                widget.destroy()
            self.choice_buttons = []

            # Create choice buttons
            for letter, definition, is_correct in choices:
                btn = ttk.Button(self.choices_frame,
                                 text=f"{letter}. {definition}",
                                 command=lambda l=letter: self.check_answer(l))
                btn.pack(fill='x', pady=5, padx=50)
                self.choice_buttons.append(btn)

                if is_correct:
                    self.current_correct_letter = letter

            # Bind keyboard shortcuts
            self.root.bind('a', lambda e: self.check_answer('A'))
            self.root.bind('b', lambda e: self.check_answer('B'))
            self.root.bind('c', lambda e: self.check_answer('C'))
            self.root.bind('d', lambda e: self.check_answer('D'))

            # Clear feedback
            self.feedback_label.config(text="")
        else:
            self.show_results()

    def generate_choices(self, correct_word):
        """Generate 4 multiple choice options"""
        # Get 3 random incorrect options
        incorrect_options = [w for w in self.words if w['id'] != correct_word['id']]
        wrong_choices = random.sample(incorrect_options, min(3, len(incorrect_options)))

        # Combine and shuffle
        all_choices = [correct_word] + wrong_choices
        random.shuffle(all_choices)

        # Assign letters
        choices = []
        for i, choice in enumerate(all_choices):
            letter = chr(65 + i)  # A, B, C, D
            is_correct = choice['id'] == correct_word['id']
            choices.append((letter, choice['definition'], is_correct))

        return choices

    def check_answer(self, selected_letter):
        """Check if selected answer is correct"""
        # Unbind keyboard
        self.root.unbind('a')
        self.root.unbind('b')
        self.root.unbind('c')
        self.root.unbind('d')

        # Disable all buttons
        for btn in self.choice_buttons:
            btn.config(state='disabled')

        current_word = self.words[self.current_index]
        is_correct = selected_letter == self.current_correct_letter

        if is_correct:
            self.score += 1
            self.correct_answers.append(current_word)
            self.feedback_label.config(text="✓ Correct!",
                                       foreground='green')
        else:
            word_with_answer = current_word.copy()
            word_with_answer['user_answer'] = selected_letter
            self.incorrect_answers.append(word_with_answer)
            self.feedback_label.config(
                text=f"✗ Incorrect. The correct answer was {self.current_correct_letter}",
                foreground='red')

        self.current_index += 1
        self.root.after(2000, self.show_question)

    def show_results(self):
        """Display quiz results"""
        # Save to database
        self.db.save_quiz_result(
            'meaning',
            self.selected_lists,
            self.score,
            len(self.words),
            self.correct_answers,
            self.incorrect_answers
        )

        self.clear_window()

        container = ttk.Frame(self.root, padding="30")
        container.pack(fill='both', expand=True)

        # Results title
        ttk.Label(container,
                  text="Quiz Complete!",
                  font=('Arial', 24, 'bold')).pack(pady=(0, 10))

        # Score display
        percentage = (self.score / len(self.words) * 100) if len(self.words) > 0 else 0
        score_text = f"{self.score} / {len(self.words)} ({percentage:.1f}%)"

        ttk.Label(container,
                  text=score_text,
                  font=('Arial', 32, 'bold'),
                  foreground='#27ae60' if percentage >= 70 else '#e74c3c').pack(pady=(0, 15))

        # Results notebook
        notebook = ttk.Notebook(container)
        notebook.pack(fill='both', expand=True, pady=(0, 10))

        # Correct answers tab
        if self.correct_answers:
            correct_frame = self.create_results_frame(notebook, self.correct_answers, True)
            notebook.add(correct_frame, text=f"✓ Correct ({len(self.correct_answers)})")

        # Incorrect answers tab
        if self.incorrect_answers:
            incorrect_frame = self.create_results_frame(notebook, self.incorrect_answers, False)
            notebook.add(incorrect_frame, text=f"✗ Incorrect ({len(self.incorrect_answers)})")

        # Buttons - FIXED LAYOUT
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=10, side='bottom')

        ttk.Button(btn_frame,
                   text="← Return to Main Menu",
                   command=self.return_callback).pack(side='left', padx=10)

        ttk.Button(btn_frame,
                   text="↻ Take Another Quiz",
                   command=lambda: MeaningQuiz(self.root, self.db,
                                               self.selected_lists,
                                               self.return_callback)).pack(side='left', padx=10)

    def create_results_frame(self, parent, words, is_correct):
        """Create frame showing word results"""
        frame = ttk.Frame(parent)

        text_frame = ttk.Frame(frame)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)

        text_widget = tk.Text(text_frame,
                              wrap='word',
                              font=('Arial', 11),
                              height=15)
        scrollbar = ttk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        for word in words:
            text_widget.insert('end', f"• {word['word']}", 'word')
            text_widget.insert('end', f" ({word['pos']})\n", 'pos')
            text_widget.insert('end', f"  {word['definition']}\n", 'def')

            if not is_correct and 'user_answer' in word:
                text_widget.insert('end', f"  Your answer: {word['user_answer']}\n", 'user')

            text_widget.insert('end', '\n')

        text_widget.tag_config('word', font=('Arial', 12, 'bold'))
        text_widget.tag_config('pos', font=('Arial', 10, 'italic'), foreground='#7f8c8d')
        text_widget.tag_config('def', font=('Arial', 10))
        text_widget.tag_config('user', font=('Arial', 10, 'italic'), foreground='#e74c3c')

        text_widget.config(state='disabled')

        return frame

    def exit_quiz(self):
        """Confirm and exit quiz"""
        if messagebox.askyesno("Exit Quiz",
                               "Are you sure you want to exit? Your progress will be lost."):
            self.return_callback()
