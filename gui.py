import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from agent import RLAgent
from tracker import RouletteTracker
from strategies import StrategyEngine
from strategy_selector import choose_strategy
from performance_tracker import StrategyPerformanceTracker
from utils import ROULETTE_COLORS
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class RouletteApp:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style("darkly")
        self.root.title("Roulette Strategy Comparator")
        self.root.configure(background=self.style.colors.bg)

        self.tracker = RouletteTracker()
        self.agent = RLAgent()
        self.strategy_engine = StrategyEngine()
        self.performance_tracker = StrategyPerformanceTracker()

        self.last_rl_number = None
        self.last_alignment = False
        self.auto_mode = ttk.BooleanVar(value=True)
        self.chart_enabled = True

        self.bankroll = 100.0
        self.initial_bet = 1.0
        self.bankroll_history = [self.bankroll]

        self.buttons = {}
        self.recent_labels = []
        self.current_strategy_label = None
        self.last_highlight_state = {}

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True)

        self.game_tab = ttk.Frame(self.notebook)
        self.chart_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.game_tab, text="Gameplay")
        self.notebook.add(self.chart_tab, text="Charts")

        self.setup_gameplay_ui()
        self.setup_charts()

    def toggle_charts_tab(self):
        if self.chart_enabled:
            self.notebook.hide(self.chart_tab)
            self.chart_enabled = False
        else:
            self.notebook.add(self.chart_tab, text="Charts")
            self.chart_enabled = True

    def setup_gameplay_ui(self):
        top_frame = ttk.Frame(self.game_tab)
        top_frame.pack(pady=5)

        input_frame = ttk.LabelFrame(top_frame, text="Data Input")
        input_frame.grid(row=0, column=0, padx=5)
        self.entry = ttk.Entry(input_frame, width=5)
        self.entry.grid(row=0, column=0)
        ttk.Button(input_frame, text="Add Spin", command=self.add_spin).grid(row=0, column=1, padx=5)
        ttk.Button(input_frame, text="Undo Spin", command=self.undo_spin).grid(row=0, column=2, padx=5)
        ttk.Button(input_frame, text="Reset History", command=self.reset_history).grid(row=0, column=3, padx=5)
        ttk.Button(input_frame, text="Strategy Stats", command=self.show_strategy_stats).grid(row=0, column=4, padx=5)
        ttk.Button(input_frame, text="Toggle Charts Tab", command=self.toggle_charts_tab).grid(row=0, column=5, padx=5)

        bankroll_frame = ttk.LabelFrame(top_frame, text="Bankroll")
        bankroll_frame.grid(row=0, column=1, padx=5)
        ttk.Label(bankroll_frame, text="Bankroll:").grid(row=0, column=0)
        self.bankroll_entry = ttk.Entry(bankroll_frame, width=6)
        self.bankroll_entry.grid(row=0, column=1)
        self.bankroll_entry.insert(0, "100")
        ttk.Label(bankroll_frame, text="Bet:").grid(row=1, column=0)
        self.bet_entry = ttk.Entry(bankroll_frame, width=6)
        self.bet_entry.grid(row=1, column=1)
        self.bet_entry.insert(0, "1")

        auto_frame = ttk.LabelFrame(top_frame, text="Mode")
        auto_frame.grid(row=0, column=2, padx=5)
        self.auto_toggle = ttk.Checkbutton(auto_frame, text="Auto Mode", variable=self.auto_mode, command=self.toggle_auto_mode)
        self.auto_toggle.pack(anchor="w")
        self.current_strategy_label = ttk.Label(auto_frame, text="Strategy: Flat")
        self.current_strategy_label.pack(anchor="w")

        self.output = ttk.Text(self.game_tab, width=100, height=25)
        self.output.tag_configure("green", foreground="lightgreen")
        self.output.tag_configure("orange", foreground="orange")
        self.output.tag_configure("red", foreground="tomato")
        self.output.pack(padx=10, pady=5)

        pad_frame = ttk.LabelFrame(self.game_tab, text="Quick Number Pad")
        pad_frame.pack(padx=10, pady=5)
        for i in range(37):
            btn = ttk.Button(pad_frame, text=str(i), width=3, command=lambda i=i: self.add_spin_direct(i))
            btn.grid(row=i//6, column=i%6, padx=2, pady=2)
            self.buttons[i] = btn

        recent_frame = ttk.LabelFrame(self.game_tab, text="Last 10 Spins")
        recent_frame.pack(pady=5)
        self.recent_labels = [ttk.Label(recent_frame, text="--", width=4, font=("Arial", 12)) for _ in range(10)]
        for i, label in enumerate(self.recent_labels):
            label.grid(row=0, column=i, padx=2)

    def setup_charts(self):
        self.fig, (self.ax_profit, self.ax_bankroll) = plt.subplots(2, 1, figsize=(6, 5))
        self.chart_canvas = FigureCanvasTkAgg(self.fig, master=self.chart_tab)
        self.chart_canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        self.update_chart()

    def update_chart(self):
        self.ax_profit.clear()
        summary = self.performance_tracker.get_summary()
        strategies = [row['strategy'] for row in summary]
        profits = [row['profit'] for row in summary]
        self.ax_profit.bar(strategies, profits, color=['green' if p > 0 else 'red' if p < 0 else 'orange' for p in profits])
        self.ax_profit.set_title("Strategy Profit")
        self.ax_profit.axhline(0, color='gray', linewidth=0.8)
        self.ax_profit.set_ylabel("Profit ($)")

        self.ax_bankroll.clear()
        self.ax_bankroll.plot(self.bankroll_history, marker='o', linestyle='-', color='cyan')
        self.ax_bankroll.set_title("Bankroll Over Time")
        self.ax_bankroll.set_ylabel("Bankroll ($)")
        self.ax_bankroll.set_xlabel("Spins")

        self.chart_canvas.draw()

    def toggle_auto_mode(self):
        if self.auto_mode.get():
            self.insert_tagged("Auto Mode ENABLED", "green")
        else:
            self.insert_tagged("Auto Mode DISABLED", "red")
