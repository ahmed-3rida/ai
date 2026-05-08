"""
Knight's Tour Problem Solver — Version 2
CS212 Artificial Intelligence — Spring 2025

Entry point (Person 9).
Run:
    python main.py
"""
import tkinter as tk
from tkinter import ttk
from constants import (SURFACE, SURFACE2, BORDER, ACCENT)
from gui import KnightsTourApp


def apply_theme(app: KnightsTourApp) -> None:
    """
    Apply a dark ttk theme so Scales and ProgressBars match the colour scheme.

    We use the built-in 'clam' theme as a base (closest to a flat dark look)
    and override the colours that matter most.
    """
    style = ttk.Style(app)
    style.theme_use("clam")

    style.configure("TScale",
                    background=SURFACE,
                    troughcolor=SURFACE2,
                    sliderlength=16)

    style.configure("Horizontal.TProgressbar",
                    troughcolor=SURFACE2,
                    background=ACCENT,
                    bordercolor=BORDER,
                    lightcolor=ACCENT,
                    darkcolor=ACCENT)


if __name__ == "__main__":
    app = KnightsTourApp()
    apply_theme(app)
    app.mainloop()
