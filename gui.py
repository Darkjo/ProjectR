import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tracker import RouletteTracker
from strategies import StrategyEngine
from strategy_selector import choose_strategy
from performance_tracker import StrategyPerformanceTracker
from agent import RLAgent

class RouletteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roulette Strategy Analyzer")
        self.style = ttk.Style("darkly")
        self.root.configure(background=self.style.colors.bg)

        self.tracker = RouletteTracker()
        self.strategy_engine = StrategyEngine()
        self.performance_tracker = StrategyPerformanceTracker()
        self.agent = RLAgent()
        self.auto_mode = ttk.BooleanVar(value=True)

        self.bankroll = 100.0
        self.initial_bet = 1.0
        self.bankroll_history = [self.bankroll]

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True)

        self.game_tab = ttk.Frame(self.notebook)
        self.chart_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.game_tab, text="Gameplay")
        self.notebook.add(self.chart_tab, text="Charts")

        self.setup_game_ui()
        self.setup_chart_tab()

    def setup_game_ui(self):
        bankroll_frame = ttk.LabelFrame(self.game_tab, text="Bankroll")
        bankroll_frame.pack(padx=10, pady=5)
        ttk.Label(bankroll_frame, text="Bankroll:").grid(row=0, column=0)
        self.bankroll_entry = ttk.Entry(bankroll_frame, width=6)
        self.bankroll_entry.grid(row=0, column=1)
        self.bankroll_entry.insert(0, "100")
        ttk.Label(bankroll_frame, text="Bet:").grid(row=1, column=0)
        self.bet_entry = ttk.Entry(bankroll_frame, width=6)
        self.bet_entry.grid(row=1, column=1)
        self.bet_entry.insert(0, "1")

        mode_frame = ttk.LabelFrame(self.game_tab, text="Mode")
        mode_frame.pack(padx=10, pady=5)
        self.auto_toggle = ttk.Checkbutton(mode_frame, text="Auto Mode", variable=self.auto_mode, command=self.toggle_auto_mode)
        self.auto_toggle.pack(anchor="w")
        self.strategy_label = ttk.Label(mode_frame, text="Strategy: Flat")
        self.strategy_label.pack(anchor="w")

        input_frame = ttk.LabelFrame(self.game_tab, text="Data Input")
        input_frame.pack(padx=10, pady=10)

        self.entry = ttk.Entry(input_frame, width=5)
        self.entry.grid(row=0, column=0, padx=5)
        ttk.Button(input_frame, text="Add Spin", command=self.add_spin).grid(row=0, column=1, padx=5)
        ttk.Button(input_frame, text="Undo Spin", command=self.undo_spin).grid(row=0, column=2, padx=5)
        ttk.Button(input_frame, text="Reset History", command=self.reset_history).grid(row=0, column=3, padx=5)
        ttk.Button(input_frame, text="Strategy Stats", command=self.show_strategy_stats).grid(row=0, column=4, padx=5)
        ttk.Button(input_frame, text="Spin Stats", command=self.show_spin_stats).grid(row=0, column=5, padx=5)
        ttk.Button(input_frame, text="Agent Stats", command=self.show_agent_stats).grid(row=0, column=6, padx=5)

        ttk.Label(input_frame, text="Bet Type:").grid(row=1, column=0, pady=5)
        self.bet_type = ttk.Combobox(input_frame, values=["Mixed", "Number", "Dozen", "Column"], width=10)
        self.bet_type.grid(row=1, column=1, pady=5)
        self.bet_type.set("Mixed")

        self.output = ttk.Text(self.game_tab, width=100, height=25)
        self.output.pack(padx=10, pady=10)

    def setup_chart_tab(self):
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_tab)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def update_chart(self):
        self.ax.clear()
        summary = self.performance_tracker.get_summary()
        strategies = [row['strategy'] for row in summary]
        profits = [row['profit'] for row in summary]
        colors = ['green' if p > 0 else 'red' if p < 0 else 'gray' for p in profits]
        self.ax.bar(strategies, profits, color=colors)
        self.ax.set_title("Strategy Profit")
        self.ax.set_ylabel("Profit ($)")
        self.ax.axhline(0, color='black', linewidth=0.8)
        self.canvas.draw()

    def toggle_auto_mode(self):
        if self.auto_mode.get():
            self.output.insert("end", "Auto Mode ENABLED\n")
        else:
            self.output.insert("end", "Auto Mode DISABLED\n")
        self.output.see("end")

    def show_strategy_stats(self):
        summary = self.performance_tracker.get_summary()
        self.output.insert("end", "\n📊 Strategy Performance Summary:\n")
        for row in summary:
            self.output.insert("end", f"{row['strategy']}: {row['wins']}W / {row['losses']}L, Profit: ${row['profit']}, Win Rate: {row['win_rate']}%\n")
        self.output.see("end")

    def show_agent_stats(self):
        summary = self.agent.get_summary()
        self.output.insert("end", "\n🤖 Agent Strategy Summary:\n")
        for row in summary:
            self.output.insert("end", f"{row['strategy']}: {row['wins']}W / {row['losses']}L, Profit: ${row['profit']}, Win Rate: {row['win_rate']}%\n")
        self.output.insert("end", f"Agent Accuracy: {self.agent.get_accuracy()*100:.2f}%\n")
        self.output.see("end")

    def add_spin(self):
        try:
            number = int(self.entry.get())
            if 0 <= number <= 36:
                self.tracker.predict_next()
                self.tracker.add_spin(number)

                bankroll = float(self.bankroll_entry.get())
                strategy = self.agent.get_recommendation(bankroll, confidence=self.tracker.confidence)
                self.strategy_label.config(text=f"Strategy: {strategy}")
                self.output.insert("end", f"🧠 Suggested Strategy: {strategy}\n")

                self.output.insert("end", f"🎯 Recommended Dozen: {self.tracker.predicted_dozen}\n")
                self.output.insert("end", f"🎯 Recommended Column: {self.tracker.predicted_column}\n")
                self.output.insert("end", f"🔥 Top 5 Frequent Numbers: {self.tracker.predicted_numbers}\n")
                self.output.insert("end", f"📈 Confidence Level: {self.tracker.confidence * 100:.1f}%\n")

                bet_type = self.bet_type.get()
                win = self.tracker.evaluate_prediction(number, bet_type)

                bet_amount = float(self.bet_entry.get())
                self.bankroll += bet_amount if win else -bet_amount
                self.bankroll_entry.delete(0, 'end')
                self.bankroll_entry.insert(0, f"{self.bankroll:.2f}")
                self.performance_tracker.update(strategy, win, bet_amount if win else -bet_amount)
                self.agent.record_result(number, strategy, win, bet_amount if win else -bet_amount)
                self.update_chart()
                self.agent.record_alignment(win)
                self.output.insert("end", f"Added spin: {number} | {'✅ WIN' if win else '❌ LOSS'} | Bet: ${bet_amount:.2f}\n")
                self.output.see("end")
            else:
                self.output.insert("end", "Invalid number! Enter 0-36.\n")
        except ValueError:
            self.output.insert("end", "Invalid input!\n")

    def undo_spin(self):
        if self.tracker.history:
            removed = self.tracker.history.pop()
            self.output.insert("end", f"Removed spin: {removed}\n")
        else:
            self.output.insert("end", "No spin to undo.\n")
        self.output.see("end")

    def show_spin_stats(self):
        color_counts = self.tracker.get_color_counts()
        dozen_counts = self.tracker.get_dozen_counts()
        column_counts = self.tracker.get_column_counts()

        self.output.insert("end", "\n🎯 Spin Stats Summary:\n")
        self.output.insert("end", f"Colors → Red: {color_counts['red']}, Black: {color_counts['black']}, Green: {color_counts['green']}\n")
        self.output.insert("end", f"Dozens → 1st: {dozen_counts['1st']}, 2nd: {dozen_counts['2nd']}, 3rd: {dozen_counts['3rd']}, Zero: {dozen_counts['zero']}\n")
        self.output.insert("end", f"Columns → 1st: {column_counts['1st']}, 2nd: {column_counts['2nd']}, 3rd: {column_counts['3rd']}\n")
        self.output.see("end")

    def reset_history(self):
        self.performance_tracker.reset()
        self.update_chart()
        self.tracker.reset()
        for strat in self.strategy_engine.get_strategy_names():
            self.strategy_engine.reset_strategy(strat)
        self.output.insert("end", "🗑️ History reset. Strategies reset.\n")
        self.output.see("end")
