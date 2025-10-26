import tkinter as tk
from tkinter import ttk, messagebox
from table import VocabDatabase
import spelling_quiz
import meaning_quiz
import analytics


class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulary Master - 11th Grade")
        self.root.geometry("900x700")  # Changed from 650 to 700
        self.root.resizable(False, False)

        # Initialize database
        self.db = VocabDatabase()

        # Configure style
        self.setup_style()

        # Show main menu
        self.show_main_menu()

    def setup_style(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure button style
        style.configure('Large.TButton',
                        font=('Arial', 14, 'bold'),
                        padding=20)

        style.configure('Title.TLabel',
                        font=('Arial', 24, 'bold'),
                        foreground='#2c3e50')

        style.configure('Subtitle.TLabel',
                        font=('Arial', 12),
                        foreground='#7f8c8d')

    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        """Display main dashboard"""
        self.clear_window()

        # Main container
        container = ttk.Frame(self.root, padding="40")
        container.pack(fill='both', expand=True)

        # Title
        title = ttk.Label(container,
                          text="Vocabulary Master",
                          style='Title.TLabel')
        title.pack(pady=(0, 10))

        subtitle = ttk.Label(container,
                             text="11th Grade Vocabulary Builder",
                             style='Subtitle.TLabel')
        subtitle.pack(pady=(0, 40))

        # Button frame
        btn_frame = ttk.Frame(container)
        btn_frame.pack(expand=True)

        # Spelling Test Button
        spelling_btn = ttk.Button(btn_frame,
                                  text="📝 Spelling Test",
                                  style='Large.TButton',
                                  command=self.start_spelling_test)
        spelling_btn.pack(pady=15, ipadx=30)

        # Meaning Test Button
        meaning_btn = ttk.Button(btn_frame,
                                 text="🎯 Meaning Test",
                                 style='Large.TButton',
                                 command=self.start_meaning_test)
        meaning_btn.pack(pady=15, ipadx=30)

        # Analytics Button
        analytics_btn = ttk.Button(btn_frame,
                                   text="📊 View Analytics",
                                   style='Large.TButton',
                                   command=self.show_analytics)
        analytics_btn.pack(pady=15, ipadx=30)

        # Footer
        footer = ttk.Label(container,
                           text=f"Total Words: {self.get_word_count()} | Lists: 1-20",
                           style='Subtitle.TLabel')
        footer.pack(side='bottom', pady=20)

    def get_word_count(self):
        """Get total number of words in database"""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM words')
        count = cursor.fetchone()[0]
        self.db.close()
        return count

    def select_lists(self, callback):
        """Show list selection dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Lists")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        ttk.Label(dialog,
                  text="Select Vocabulary Lists",
                  font=('Arial', 16, 'bold')).pack(pady=20)

        ttk.Label(dialog,
                  text="Choose one or more lists to include in your quiz:",
                  font=('Arial', 10)).pack(pady=(0, 20))

        # Scrollable frame for checkboxes
        canvas = tk.Canvas(dialog, height=350)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Get available lists
        available_lists = self.db.get_all_list_numbers()

        # Checkbox variables
        list_vars = {}
        for list_num in available_lists:
            var = tk.BooleanVar()
            list_vars[list_num] = var

            cb = ttk.Checkbutton(scrollable_frame,
                                 text=f"List {list_num}",
                                 variable=var)
            cb.pack(anchor='w', padx=40, pady=5)

        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")

        # Select All / Deselect All buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)

        def select_all():
            for var in list_vars.values():
                var.set(True)

        def deselect_all():
            for var in list_vars.values():
                var.set(False)

        ttk.Button(btn_frame, text="Select All",
                   command=select_all).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Deselect All",
                   command=deselect_all).pack(side='left', padx=5)

        # Start Quiz button
        def start_quiz():
            selected = [num for num, var in list_vars.items() if var.get()]

            if not selected:
                messagebox.showwarning("No Selection",
                                       "Please select at least one list!")
                return

            dialog.destroy()
            callback(selected)

        ttk.Button(dialog,
                   text="Start Quiz",
                   command=start_quiz,
                   style='Large.TButton').pack(pady=20)

    def start_spelling_test(self):
        """Launch spelling test module"""
        self.select_lists(lambda lists:
                          spelling_quiz.SpellingQuiz(self.root, self.db, lists, self.show_main_menu))

    def start_meaning_test(self):
        """Launch meaning test module"""
        self.select_lists(lambda lists:
                          meaning_quiz.MeaningQuiz(self.root, self.db, lists, self.show_main_menu))

    def show_analytics(self):
        """Launch analytics module"""
        analytics.Analytics(self.root, self.db, self.show_main_menu)


def main():
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()