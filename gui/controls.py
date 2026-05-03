# ─────────────────────────────────────────────
#  GUI — CONTROLS MIXIN  (Person 6)
#  Left-panel widgets: sliders, buttons, stats
#  Knight's Tour Solver — CS212 AI Spring 2025
# ─────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk
from constants import (BG, SURFACE, SURFACE2, BORDER, ACCENT, ACCENT2,
                       ACCENT3, TEXT, MUTED, BOARD_MIN, BOARD_MAX,
                       BOARD_DEFAULT)


class ControlsMixin:
    """
    Mixin that builds the entire left-side control panel.

    The panel contains:
      • Board-size slider (5 – 12)
      • Algorithm selector (Backtracking | Genetic)
      • GA-specific parameters (population size, generations)
      • Start-position hint label
      • Solve / Replay buttons
      • Animation speed slider
      • 4-cell statistics grid (squares, coverage, time, result)
      • GA progress bar (shown only while GA runs)
    """

    # ── Helper label factory ──────────────────
    def _lbl(self, parent, text, size=10, color=MUTED, bold=False):
        """Create a styled label and return it (not packed)."""
        font = ("Courier", size, "bold") if bold else ("Courier", size)
        return tk.Label(parent, text=text, bg=SURFACE, fg=color, font=font)

    # ── Full panel build ───────────────────────
    def _build_controls(self, p):
        """
        Populate the left panel `p` with all controls.
        Called once from _build_ui().
        """
        pad = {"padx": 16, "pady": 6}

        # Section title
        self._lbl(p, "CONFIGURATION", 9, MUTED).pack(
            anchor="w", padx=16, pady=(14, 2))
        tk.Frame(p, bg=BORDER, height=1).pack(fill="x", padx=16, pady=(0, 10))

        # ── Board size ─────────────────────────
        self._lbl(p, "Board Size (n × n)", 10, TEXT).pack(anchor="w", **pad)
        size_row = tk.Frame(p, bg=SURFACE)
        size_row.pack(fill="x", padx=16, pady=(0, 4))

        # Live size label (right side)
        self._size_lbl = tk.Label(
            size_row, text=str(BOARD_DEFAULT),
            bg=SURFACE, fg=ACCENT,
            font=("Courier", 20, "bold"), width=3)
        self._size_lbl.pack(side="right")

        ttk.Scale(size_row, from_=BOARD_MIN, to=BOARD_MAX,
                  orient="horizontal", variable=self.n,
                  command=self._on_size_change).pack(
                      side="left", fill="x", expand=True)

        # ── Algorithm tabs ─────────────────────
        self._lbl(p, "Algorithm", 10, TEXT).pack(anchor="w", **pad)
        algo_row = tk.Frame(p, bg=SURFACE)
        algo_row.pack(fill="x", padx=16, pady=(0, 8))
        self._btn_bt = self._tab_btn(algo_row, "Backtracking", "backtracking")
        self._btn_ga = self._tab_btn(algo_row, "Genetic",      "genetic")
        self._btn_bt.pack(side="left", expand=True, fill="x", padx=(0, 4))
        self._btn_ga.pack(side="left", expand=True, fill="x")

        # ── GA parameters (hidden until GA selected) ──
        self._ga_frame = tk.Frame(p, bg=SURFACE)

        self._lbl(self._ga_frame, "Population Size", 10, TEXT).pack(
            anchor="w", padx=4)
        pop_row = tk.Frame(self._ga_frame, bg=SURFACE)
        pop_row.pack(fill="x", pady=(0, 6))
        self._pop_lbl = tk.Label(pop_row, text="200",
                                  bg=SURFACE, fg=ACCENT,
                                  font=("Courier", 14, "bold"), width=4)
        self._pop_lbl.pack(side="right")
        ttk.Scale(pop_row, from_=50, to=500, orient="horizontal",
                  variable=self.pop_size,
                  command=lambda v: self._pop_lbl.config(
                      text=str(int(float(v))))).pack(
                          side="left", fill="x", expand=True)

        self._lbl(self._ga_frame, "Generations", 10, TEXT).pack(
            anchor="w", padx=4)
        gen_row = tk.Frame(self._ga_frame, bg=SURFACE)
        gen_row.pack(fill="x")
        self._gen_lbl = tk.Label(gen_row, text="500",
                                  bg=SURFACE, fg=ACCENT,
                                  font=("Courier", 14, "bold"), width=5)
        self._gen_lbl.pack(side="right")
        ttk.Scale(gen_row, from_=100, to=2000, orient="horizontal",
                  variable=self.gens,
                  command=lambda v: self._gen_lbl.config(
                      text=str(int(float(v))))).pack(
                          side="left", fill="x", expand=True)

        # ── Hint label ─────────────────────────
        self._hint_var = tk.StringVar(value="Click a cell to set start position")
        tk.Label(p, textvariable=self._hint_var,
                 bg=SURFACE, fg=MUTED,
                 font=("Helvetica", 10, "italic")).pack(pady=(8, 4))

        # ── Solve button ───────────────────────
        self._run_btn = tk.Button(
            p, text="▶  SOLVE",
            bg=ACCENT, fg="white",
            font=("Courier", 12, "bold"),
            relief="flat", bd=0,
            activebackground="#8aa3ff", activeforeground="white",
            cursor="hand2",
            command=self._run_solver)
        self._run_btn.pack(fill="x", padx=16, pady=(4, 4), ipady=8)

        # ── Replay button ──────────────────────
        self._anim_btn = tk.Button(
            p, text="↺  Replay Animation",
            bg=SURFACE2, fg=MUTED,
            font=("Courier", 10),
            relief="flat", bd=0,
            cursor="hand2",
            state="disabled",
            command=self._replay)
        self._anim_btn.pack(fill="x", padx=16, pady=(0, 8), ipady=6)

        # ── Speed slider ───────────────────────
        tk.Frame(p, bg=BORDER, height=1).pack(fill="x", padx=16, pady=(4, 8))
        self._lbl(p, "Animation Speed", 9, MUTED).pack(anchor="w", padx=16)
        spd_row = tk.Frame(p, bg=SURFACE)
        spd_row.pack(fill="x", padx=16, pady=(2, 8))
        self._lbl(spd_row, "slow", 9).pack(side="left")
        ttk.Scale(spd_row, from_=20, to=300, orient="horizontal",
                  variable=self.anim_delay).pack(
                      side="left", fill="x", expand=True, padx=6)
        self._lbl(spd_row, "fast", 9).pack(side="right")

        # ── Statistics grid ─────────────────────
        tk.Frame(p, bg=BORDER, height=1).pack(fill="x", padx=16, pady=(0, 8))
        stats_frame = tk.Frame(p, bg=SURFACE)
        stats_frame.pack(fill="x", padx=16, pady=(0, 14))
        self._stat_squares = self._stat_card(stats_frame, "Squares",  "—", 0, 0)
        self._stat_cov     = self._stat_card(stats_frame, "Coverage", "—", 0, 1)
        self._stat_time    = self._stat_card(stats_frame, "Time",     "—", 1, 0)
        self._stat_result  = self._stat_card(stats_frame, "Result",   "—", 1, 1)
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)

        # ── GA progress bar (hidden initially) ─
        self._ga_progress_frame = tk.Frame(p, bg=SURFACE)
        self._ga_progress_frame.pack(fill="x", padx=16, pady=(0, 10))
        self._ga_prog_bar = ttk.Progressbar(
            self._ga_progress_frame, mode="determinate", maximum=100)
        self._ga_gen_var = tk.StringVar(value="")
        self._ga_gen_lbl = tk.Label(
            self._ga_progress_frame,
            textvariable=self._ga_gen_var,
            bg=SURFACE, fg=MUTED,
            font=("Courier", 9))

        # Set initial button states now that _ga_frame exists
        self._update_algo_buttons()

    # ── Stat card helper ───────────────────────
    def _stat_card(self, parent, label, val, row, col):
        """
        Create a small card widget showing a labelled value.

        Returns a tk.StringVar so the caller can update the value later.
        """
        f = tk.Frame(parent, bg=SURFACE2,
                     highlightbackground=BORDER, highlightthickness=1)
        f.grid(row=row, column=col, sticky="ew", padx=3, pady=3,
               ipadx=8, ipady=6)
        tk.Label(f, text=label.upper(), bg=SURFACE2, fg=MUTED,
                 font=("Courier", 8)).pack()
        var = tk.StringVar(value=val)
        tk.Label(f, textvariable=var, bg=SURFACE2, fg=ACCENT,
                 font=("Courier", 14, "bold")).pack()
        return var

    # ── Tab button helper ──────────────────────
    def _tab_btn(self, parent, text, algo_name):
        """Create an algorithm-selector tab button."""
        return tk.Button(
            parent, text=text,
            bg=SURFACE2, fg=MUTED,
            font=("Courier", 10),
            relief="flat", bd=0,
            cursor="hand2",
            command=lambda: self._select_algo(algo_name))

    # ── Logic callbacks ────────────────────────
    def _on_size_change(self, val):
        """Called when the board-size slider moves."""
        v = int(float(val))
        self.n.set(v)
        self._size_lbl.config(text=str(v))
        self.start_r = 0
        self.start_c = 0
        self._hint_var.set("Click a cell to set start position")
        self.full_path = []
        self._anim_btn.config(state="disabled")
        self._build_board()
        self._set_status("Board resized — click Solve to start", "idle")

    def _select_algo(self, name):
        """Switch the active algorithm and update button visuals."""
        self.algo.set(name)
        self._update_algo_buttons()

    def _update_algo_buttons(self):
        """Highlight the active algorithm button; show/hide GA params."""
        from constants import ACCENT, SURFACE2, MUTED
        algo = self.algo.get()
        if algo == "backtracking":
            self._btn_bt.config(bg=ACCENT,   fg="white")
            self._btn_ga.config(bg=SURFACE2, fg=MUTED)
            self._ga_frame.pack_forget()
        else:
            self._btn_ga.config(bg=ACCENT,   fg="white")
            self._btn_bt.config(bg=SURFACE2, fg=MUTED)
            self._ga_frame.pack(fill="x", padx=16, pady=(0, 8))
