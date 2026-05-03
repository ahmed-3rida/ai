# ─────────────────────────────────────────────
#  GUI — BOARD MIXIN  (Person 5)
#  Handles all Canvas drawing and click events
#  Knight's Tour Solver — CS212 AI Spring 2025
# ─────────────────────────────────────────────
from constants import (BORDER, MUTED, ACCENT, LIGHT_SQ, DARK_SQ,
                       VISITED, CURRENT, START_OUT)


class BoardMixin:
    """
    Mixin that adds board-drawing and interaction methods to KnightsTourApp.

    Attributes expected from the host class
    ----------------------------------------
    self._canvas   : tk.Canvas widget
    self.n         : tk.IntVar – current board size
    self.cells     : dict {(r,c): info_dict}  – built here
    self.start_r / self.start_c : currently selected start cell
    self.solving   : bool – True while algorithm is running
    self._hint_var : tk.StringVar – label shown above Solve button
    """

    # ── Build / Rebuild ────────────────────────
    def _build_board(self):
        """
        Clear the canvas and draw an n×n chessboard grid.

        The board is centred in the available canvas space.
        Each cell is stored in self.cells so other methods can
        look up its pixel coordinates by (row, col) key.
        """
        self._canvas.delete("all")
        self.cells = {}
        c = self._canvas
        W = c.winfo_width()
        H = c.winfo_height()
        if W < 10 or H < 10:
            return

        n = self.n.get()
        cell = min((W - 10) // n, (H - 10) // n)   # pixels per cell
        ox = (W - cell * n) // 2                    # horizontal offset
        oy = (H - cell * n) // 2                    # vertical offset

        for r in range(n):
            for col in range(n):
                x1 = ox + col * cell
                y1 = oy + r * cell
                x2 = x1 + cell
                y2 = y1 + cell

                # Alternating light / dark squares (chess pattern)
                color = LIGHT_SQ if (r + col) % 2 == 0 else DARK_SQ

                rect_id = c.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color, outline=BORDER, width=1,
                    tags=(f"cell-{r}-{col}", "cell")
                )
                text_id = c.create_text(
                    (x1 + x2) // 2, (y1 + y2) // 2,
                    text="",
                    fill=MUTED,
                    font=("Courier", max(7, cell // 5), "bold"),
                    tags=f"txt-{r}-{col}"
                )

                # Store all info needed to update this cell later
                self.cells[(r, col)] = {
                    "rect": rect_id, "text": text_id,
                    "x1": x1, "y1": y1,
                    "x2": x2, "y2": y2,
                    "color": color          # original colour (to reset)
                }

        self._mark_start()

    # ── User Interaction ───────────────────────
    def _on_canvas_click(self, event):
        """
        Detect which cell the user clicked and set it as the start position.
        Ignored while the solver is running.
        """
        if self.solving:
            return
        for (r, col), info in self.cells.items():
            if (info["x1"] <= event.x <= info["x2"] and
                    info["y1"] <= event.y <= info["y2"]):
                self.start_r = r
                self.start_c = col
                self._hint_var.set(f"Start: ({r + 1}, {col + 1})")
                self._reset_board()
                return

    # ── Visual State Helpers ───────────────────
    def _mark_start(self):
        """Draw a teal border around the current start cell."""
        c = self._canvas
        c.delete("start_outline")
        key = (self.start_r, self.start_c)
        if key in self.cells:
            info = self.cells[key]
            c.create_rectangle(
                info["x1"] + 2, info["y1"] + 2,
                info["x2"] - 2, info["y2"] - 2,
                outline=START_OUT, width=3,
                tags="start_outline"
            )

    def _reset_board(self):
        """Return all cells to their original colours and clear numbers."""
        c = self._canvas
        for (r, col), info in self.cells.items():
            c.itemconfig(info["rect"], fill=info["color"])
            c.itemconfig(info["text"], text="")
        c.delete("knight_icon")
        self._mark_start()

    def _render_path(self, path, up_to):
        """
        Render the first `up_to` steps of `path` on the board.

        - Visited squares: dark blue + step number
        - Current square (last in slice): accent blue + knight ♞ icon
        """
        self._reset_board()
        c = self._canvas
        slice_ = path[:up_to]

        for i, (r, col) in enumerate(slice_):
            info = self.cells.get((r, col))
            if not info:
                continue

            if i < len(slice_) - 1:
                # Already-visited square
                c.itemconfig(info["rect"], fill=VISITED)
                c.itemconfig(info["text"], text=str(i + 1), fill=ACCENT)
            else:
                # Current knight position
                c.itemconfig(info["rect"], fill=CURRENT)
                c.delete("knight_icon")
                mx = (info["x1"] + info["x2"]) // 2
                my = (info["y1"] + info["y2"]) // 2
                cell_h = info["y2"] - info["y1"]
                c.create_text(
                    mx, my, text="♞", fill="white",
                    font=("Helvetica", max(10, cell_h // 2), "bold"),
                    tags="knight_icon"
                )

        self._mark_start()
