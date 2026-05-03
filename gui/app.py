# ─────────────────────────────────────────────
#  GUI — MAIN APPLICATION  (Person 8)
#  Assembles all mixins into one Tk window
#  Knight's Tour Solver — CS212 AI Spring 2025
# ─────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk

from constants import (BG, SURFACE, SURFACE2, BORDER, ACCENT, MUTED, TEXT,
                       BOARD_DEFAULT)
from gui.board    import BoardMixin
from gui.controls import ControlsMixin
from gui.solver   import SolverMixin


class KnightsTourApp(BoardMixin, ControlsMixin, SolverMixin, tk.Tk):
    """
    Main application window.

    Inherits from three mixins:
      BoardMixin    – canvas drawing & board interaction   (Person 5)
      ControlsMixin – left-panel widgets & callbacks       (Person 6)
      SolverMixin   – threading, animation & stats         (Person 7)

    This class only handles:
      1. Tkinter window configuration
      2. Shared application state (tk.Vars)
      3. Top-level layout (header, panel, canvas, status bar)
    """

    def __init__(self):
        super().__init__()

        # ── Window setup ───────────────────────
        self.title("Knight's Tour Solver — CS212 AI Spring 2025")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(900, 620)

        # ── Shared state ───────────────────────
        self.n         = tk.IntVar(value=BOARD_DEFAULT)
        self.algo      = tk.StringVar(value="backtracking")
        self.pop_size  = tk.IntVar(value=200)
        self.gens      = tk.IntVar(value=500)
        self.start_r   = 0
        self.start_c   = 0
        self.full_path = []
        self.cells     = {}
        self.anim_delay = tk.IntVar(value=120)
        self.solving   = False
        self._stop     = False
        self._anim_after = None

        # ── Build the UI then draw initial board ─
        self._build_ui()
        self._build_board()

    # ── Top-level layout ───────────────────────
    def _build_ui(self):
        """
        Create the window skeleton:
          • Header (badge + title + subtitle)
          • Divider line
          • Body (left panel + right canvas)
          • Status bar at the bottom
        """
        # Header
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=24, pady=(18, 0))

        tk.Label(hdr,
                 text="CS212 · AI Project · Spring 2025",
                 bg="#1a1f35", fg=ACCENT,
                 font=("Courier", 10), padx=10, pady=4).pack()

        tk.Label(hdr,
                 text="Knight's Tour Solver",
                 bg=BG, fg=TEXT,
                 font=("Helvetica", 22, "bold")).pack(pady=(6, 2))

        tk.Label(hdr,
                 text="Backtracking + Warnsdorff's Heuristic  |  Genetic Algorithm",
                 bg=BG, fg=MUTED,
                 font=("Helvetica", 11)).pack()

        # Divider
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=24, pady=12)

        # Body (two-column grid: panel | canvas)
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=24, pady=(0, 18))
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # Left panel
        self._panel = tk.Frame(body, bg=SURFACE, bd=1, relief="flat",
                               highlightbackground=BORDER,
                               highlightthickness=1)
        self._panel.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        self._build_controls(self._panel)   # → ControlsMixin

        # Right: canvas frame
        board_frame = tk.Frame(body, bg=BG)
        board_frame.grid(row=0, column=1, sticky="nsew")

        self._canvas = tk.Canvas(board_frame, bg=BG, highlightthickness=0)
        self._canvas.pack(fill="both", expand=True)
        self._canvas.bind("<Configure>", lambda e: self._build_board())
        self._canvas.bind("<Button-1>",  self._on_canvas_click)

        # Status bar (bottom strip)
        self._status_var = tk.StringVar(
            value="Ready — select board size and click Solve")
        self._status_bar = tk.Label(
            self,
            textvariable=self._status_var,
            bg=SURFACE2, fg=MUTED,
            font=("Courier", 10), anchor="w",
            padx=12, pady=6)
        self._status_bar.pack(fill="x", padx=24, pady=(0, 12))
