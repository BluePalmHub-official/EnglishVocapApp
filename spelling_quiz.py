import tkinter as tk
from tkinter import ttk, messagebox
import random


class SpellingQuiz:
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

        # Clear window and setup UI
        self.clear_window()
        self.setup_ui()
        self.show_question()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_ui(self):
        """Setup spelling test UI"""
        # Main container
        self.container = ttk.Frame(self.root, padding="30")
        self.container.pack(fill='both', expand=True)

        # Header with Exit button
        header_frame = ttk.Frame(self.container)
        header_frame.pack(fill='x', pady=(0, 20))

        # Title on the left
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side='left', fill='x', expand=True)

        ttk.Label(title_frame,
                  text="Spelling Test",
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

        # Question frame
        question_frame = ttk.Frame(self.container)
        question_frame.pack(expand=True, fill='both', pady=20)

        ttk.Label(question_frame,
                  text="Definition:",
                  font=('Arial', 12, 'bold')).pack(pady=(0, 10))

        self.definition_label = ttk.Label(question_frame,
                                          text="",
                                          font=('Arial', 14),
                                          wraplength=700,
                                          justify='center')
        self.definition_label.pack(pady=20)

        self.pos_label = ttk.Label(question_frame,
                                   text="",
                                   font=('Arial', 11, 'italic'),
                                   foreground='#7f8c8d')
        self.pos_label.pack()

        # Answer frame
        answer_frame = ttk.Frame(self.container)
        answer_frame.pack(pady=20)

        ttk.Label(answer_frame,
                  text="Your Answer:",
                  font=('Arial', 12)).pack()

        self.answer_entry = ttk.Entry(answer_frame,
                                      font=('Arial', 16),
                                      width=30,
                                      justify='center')
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', lambda e: self.submit_answer())

        # Feedback label
        self.feedback_label = ttk.Label(self.container,
                                        text="",
                                        font=('Arial', 13, 'bold'))
        self.feedback_label.pack(pady=10)

        # Submit button (centered)
        self.submit_btn = ttk.Button(self.container,
                                     text="Submit Answer",
                                     command=self.submit_answer)
        self.submit_btn.pack(pady=10)

    def show_question(self):
        """Display current question"""
        if self.current_index < len(self.words):
            word = self.words[self.current_index]

            # Update progress
            progress_text = f"Question {self.current_index + 1} of {len(self.words)}"
            self.progress_label.config(text=progress_text)
            self.progress_bar['maximum'] = len(self.words)
            self.progress_bar['value'] = self.current_index

            # Display definition and part of speech
            self.definition_label.config(text=word['definition'])
            self.pos_label.config(text=f"({word['pos']})")

            # Clear entry and feedback
            self.answer_entry.delete(0, tk.END)
            self.feedback_label.config(text="")
            self.answer_entry.focus()
        else:
            self.show_results()

    def submit_answer(self):
        """Check answer and move to next question"""
        user_answer = self.answer_entry.get().strip()

        if not user_answer:
            self.feedback_label.config(text="⚠ Please enter an answer",
                                       foreground='orange')
            return

        current_word = self.words[self.current_index]
        correct_word = current_word['word']

        is_correct = user_answer.lower() == correct_word.lower()

        if is_correct:
            self.score += 1
            self.correct_answers.append(current_word)
            self.feedback_label.config(text="✓ Correct!",
                                       foreground='green')
        else:
            word_with_answer = current_word.copy()
            word_with_answer['user_answer'] = user_answer
            self.incorrect_answers.append(word_with_answer)
            self.feedback_label.config(
                text=f"✗ Incorrect. The correct answer is: {correct_word}",
                foreground='red')

        self.current_index += 1

        # Disable submit button temporarily
        self.submit_btn.config(state='disabled')
        self.root.after(2000, self.enable_submit)
        self.root.after(2000, self.show_question)

    def enable_submit(self):
        """Re-enable submit button"""
        self.submit_btn.config(state='normal')

    def show_results(self):
        """Display quiz results"""
        # Save to database
        self.db.save_quiz_result(
            'spelling',
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
                   command=lambda: SpellingQuiz(self.root, self.db,
                                                self.selected_lists,
                                                self.return_callback)).pack(side='left', padx=10)

    def create_results_frame(self, parent, words, is_correct):
        """Create frame showing word results"""
        frame = ttk.Frame(parent)

        # Create text widget with scrollbar
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

        # Populate with words
        for word in words:
            text_widget.insert('end', f"• {word['word']}", 'word')
            text_widget.insert('end', f" ({word['pos']})\n", 'pos')
            text_widget.insert('end', f"  {word['definition']}\n", 'def')

            if not is_correct and 'user_answer' in word:
                text_widget.insert('end', f"  Your answer: {word['user_answer']}\n", 'user')

            text_widget.insert('end', '\n')

        # Configure tags
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
