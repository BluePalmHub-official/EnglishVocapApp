import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class Analytics:
    def __init__(self, root, db, return_callback):
        self.root = root
        self.db = db
        self.return_callback = return_callback

        self.clear_window()
        self.setup_ui()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_ui(self):
        """Setup analytics UI"""
        container = ttk.Frame(self.root, padding="20")
        container.pack(fill='both', expand=True)

        # Header
        header_frame = ttk.Frame(container)
        header_frame.pack(fill='x', pady=(0, 20))

        ttk.Label(header_frame,
                  text="Performance Analytics",
                  font=('Arial', 20, 'bold')).pack()

        ttk.Button(header_frame,
                   text="← Back to Main Menu",
                   command=self.return_callback).pack(anchor='w', pady=10)

        # Get statistics
        stats = self.db.get_overall_stats()
        history = self.db.get_quiz_history(limit=50)  # Get more history for line graph

        if stats['total_quizzes'] == 0:
            ttk.Label(container,
                      text="No quiz data available yet.\nTake a quiz to see your statistics!",
                      font=('Arial', 14),
                      justify='center').pack(expand=True)
            return

        # Overall stats frame
        stats_frame = ttk.LabelFrame(container, text="Overall Statistics", padding="20")
        stats_frame.pack(fill='x', pady=10)

        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack()

        self.create_stat_box(stats_grid, "Total Quizzes",
                             str(stats['total_quizzes']), 0, 0)
        self.create_stat_box(stats_grid, "Average Score",
                             f"{stats['avg_percentage']:.1f}%", 0, 1)
        self.create_stat_box(stats_grid, "Best Score",
                             f"{stats['best_score']:.1f}%", 0, 2)
        self.create_stat_box(stats_grid, "Total Correct",
                             f"{stats['total_correct']}/{stats['total_attempted']}", 0, 3)

        # Notebook for tabs
        notebook = ttk.Notebook(container)
        notebook.pack(fill='both', expand=True, pady=20)

        # Recent history tab
        history_frame = self.create_history_frame(notebook, history[:10])  # Show only 10 in table
        notebook.add(history_frame, text="Recent Quizzes")

        # Charts tab
        charts_frame = self.create_charts_frame(notebook, history, stats)
        notebook.add(charts_frame, text="Performance Charts")

    def create_stat_box(self, parent, label, value, row, col):
        """Create a statistics display box"""
        frame = ttk.Frame(parent, relief='solid', borderwidth=1)
        frame.grid(row=row, column=col, padx=10, pady=5, sticky='nsew')

        ttk.Label(frame,
                  text=label,
                  font=('Arial', 10),
                  foreground='#7f8c8d').pack(pady=(10, 5))

        ttk.Label(frame,
                  text=value,
                  font=('Arial', 18, 'bold'),
                  foreground='#2c3e50').pack(pady=(0, 10), padx=20)

    def create_history_frame(self, parent, history):
        """Create frame showing quiz history"""
        frame = ttk.Frame(parent)

        # Create Treeview
        columns = ('Date', 'Type', 'Lists', 'Score', 'Percentage')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=12)

        # Define headings
        tree.heading('Date', text='Date')
        tree.heading('Type', text='Quiz Type')
        tree.heading('Lists', text='Lists Used')
        tree.heading('Score', text='Score')
        tree.heading('Percentage', text='Percentage')

        # Define column widths
        tree.column('Date', width=180)
        tree.column('Type', width=120)
        tree.column('Lists', width=150)
        tree.column('Score', width=100)
        tree.column('Percentage', width=100)

        # Add data
        for quiz in history:
            date = quiz['date_taken'].split('.')[0]  # Remove microseconds
            quiz_type = quiz['quiz_type'].capitalize()
            lists = f"Lists {quiz['lists_used']}"
            score = f"{quiz['score']}/{quiz['total_questions']}"
            percentage = f"{quiz['percentage']:.1f}%"

            # Color code by percentage
            tag = 'excellent' if quiz['percentage'] >= 90 else \
                'good' if quiz['percentage'] >= 70 else \
                    'fair' if quiz['percentage'] >= 50 else 'poor'

            tree.insert('', 'end', values=(date, quiz_type, lists, score, percentage),
                        tags=(tag,))

        # Configure tags
        tree.tag_configure('excellent', background='#d5f4e6')
        tree.tag_configure('good', background='#fff3cd')
        tree.tag_configure('fair', background='#ffe5cc')
        tree.tag_configure('poor', background='#f8d7da')

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10, padx=(0, 10))

        return frame

    def create_charts_frame(self, parent, history, stats):
        """Create frame with performance charts"""
        frame = ttk.Frame(parent)

        # Create figure with subplots (2 rows, 2 columns)
        fig = Figure(figsize=(10, 8), dpi=80)

        # Top Left: Pie chart - Overall performance
        ax1 = fig.add_subplot(221)
        correct = stats['total_correct']
        incorrect = stats['total_attempted'] - stats['total_correct']

        colors = ['#4CAF50', '#F44336']
        sizes = [correct, incorrect]
        labels = [f'Correct\n{correct}', f'Incorrect\n{incorrect}']

        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                startangle=90, textprops={'fontsize': 9, 'weight': 'bold'})
        ax1.set_title('Overall Performance', fontsize=11, weight='bold', pad=15)

        # Top Right: Bar chart - Recent quiz scores
        ax2 = fig.add_subplot(222)

        if history:
            recent = history[::-1][:10]  # Last 10 quizzes, chronological
            quiz_numbers = [f"Q{i + 1}" for i in range(len(recent))]
            percentages = [q['percentage'] for q in recent]

            # Color bars based on score
            bar_colors = ['#4CAF50' if p >= 70 else '#FFA726' if p >= 50 else '#F44336'
                          for p in percentages]

            bars = ax2.bar(quiz_numbers, percentages, color=bar_colors, alpha=0.8)

            ax2.set_xlabel('Quiz', fontsize=9, weight='bold')
            ax2.set_ylabel('Score (%)', fontsize=9, weight='bold')
            ax2.set_title('Recent Quiz Scores', fontsize=11, weight='bold', pad=15)
            ax2.set_ylim(0, 100)
            ax2.axhline(y=70, color='green', linestyle='--', alpha=0.3, linewidth=1)
            ax2.grid(axis='y', alpha=0.3)

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2., height,
                         f'{height:.0f}%',
                         ha='center', va='bottom', fontsize=7)

        # Bottom: Line graph - Progress over time (spans both columns)
        ax3 = fig.add_subplot(212)

        if history:
            # Reverse to get chronological order (oldest to newest)
            all_history = history[::-1]

            # Separate data by quiz type
            spelling_data = [(i + 1, q['percentage']) for i, q in enumerate(all_history)
                           if q['quiz_type'] == 'spelling']
            meaning_data = [(i + 1, q['percentage']) for i, q in enumerate(all_history)
                          if q['quiz_type'] == 'meaning']

            # Plot spelling quiz progression
            if spelling_data:
                spelling_x, spelling_y = zip(*spelling_data)
                ax3.plot(spelling_x, spelling_y,
                        marker='o',
                        linestyle='-',
                        linewidth=2,
                        markersize=6,
                        color='#2196F3',
                        label='Spelling Quiz',
                        alpha=0.8)

            # Plot meaning quiz progression
            if meaning_data:
                meaning_x, meaning_y = zip(*meaning_data)
                ax3.plot(meaning_x, meaning_y,
                        marker='s',
                        linestyle='-',
                        linewidth=2,
                        markersize=6,
                        color='#FF5722',
                        label='Meaning Quiz',
                        alpha=0.8)

            # Customize the line graph
            ax3.set_xlabel('Quiz Number (Chronological)', fontsize=10, weight='bold')
            ax3.set_ylabel('Score (%)', fontsize=10, weight='bold')
            ax3.set_title('Performance Progress Over Time', fontsize=12, weight='bold', pad=15)
            ax3.set_ylim(0, 100)
            ax3.grid(True, alpha=0.3, linestyle='--')
            ax3.axhline(y=70, color='green', linestyle='--', alpha=0.5, linewidth=1.5,
                       label='Target: 70%')
            ax3.legend(loc='lower right', fontsize=9, framealpha=0.9)

            # Add trend lines if enough data
            if len(spelling_data) >= 3:
                # Calculate moving average for spelling
                window = min(3, len(spelling_data))
                if window > 1:
                    spelling_avg = []
                    for i in range(len(spelling_y) - window + 1):
                        avg = sum(spelling_y[i:i+window]) / window
                        spelling_avg.append(avg)
                    avg_x = list(spelling_x[window-1:])
                    ax3.plot(avg_x, spelling_avg,
                            linestyle='--',
                            linewidth=1.5,
                            color='#2196F3',
                            alpha=0.4)

            if len(meaning_data) >= 3:
                # Calculate moving average for meaning
                window = min(3, len(meaning_data))
                if window > 1:
                    meaning_avg = []
                    for i in range(len(meaning_y) - window + 1):
                        avg = sum(meaning_y[i:i+window]) / window
                        meaning_avg.append(avg)
                    avg_x = list(meaning_x[window-1:])
                    ax3.plot(avg_x, meaning_avg,
                            linestyle='--',
                            linewidth=1.5,
                            color='#FF5722',
                            alpha=0.4)

        fig.tight_layout()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

        return frame
