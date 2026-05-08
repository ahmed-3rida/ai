# ─────────────────────────────────────────────
#  GUI — SOLVER & ANIMATION MIXIN  (Person 7)
#  Runs algorithms in threads, drives animation
#  Knight's Tour Solver — CS212 AI Spring 2025
# ─────────────────────────────────────────────
import threading
from constants import ACCENT2, ACCENT3, MUTED


class SolverMixin:
    """
    Mixin that handles:
      • Launching solvers in background threads (so the GUI never freezes)
      • Receiving results back on the main thread via `self.after()`
      • Driving the step-by-step animation
      • Updating the statistics panel when solving finishes

    Attributes expected from the host class
    ----------------------------------------
    self.solving       : bool flag – True while a solver thread runs
    self._stop         : bool flag – set True to abort GA early
    self.full_path     : list – the path returned by the last solver
    self.algo          : tk.StringVar – "backtracking" or "genetic"
    self.n / pop_size / gens : tk.IntVar parameters
    self.start_r / start_c  : int – user-chosen start cell
    self.anim_delay    : tk.IntVar – controls animation speed
    self._anim_after   : after-handle or None
    """

    # ── Status bar ──────────────────────────────
    def _set_status(self, msg, state="idle"):
        """
        Update the bottom status bar text and colour.

        state values: "idle" | "running" | "ok" | "fail"
        """
        colors = {
            "idle":    MUTED,
            "running": "#fbbf24",   # yellow
            "ok":      ACCENT3,     # teal
            "fail":    ACCENT2,     # red
        }
        self._status_var.set(msg)
        self._status_bar.config(fg=colors.get(state, MUTED))

    # ── Animation ───────────────────────────────
    def _replay(self):
        """Replay the last computed tour from the beginning."""
        if self.full_path:
            self._animate(self.full_path)

    def _animate(self, path):
        """
        Animate `path` step by step using tkinter's `after()` scheduler.

        Each tick renders one more step and re-schedules itself.
        The delay between steps is controlled by `self.anim_delay`.
        """
        if self._anim_after:
            self.after_cancel(self._anim_after)

        self._step = 0
        self._path_to_anim = path

        def tick():
            self._step += 1
            self._render_path(self._path_to_anim, self._step)
            if self._step < len(self._path_to_anim):
                # Schedule next tick (delay = 350 - slider value, min 20 ms)
                delay = max(20, 350 - self.anim_delay.get())
                self._anim_after = self.after(delay, tick)
            else:
                n = self.n.get()
                self._set_status(
                    f"Tour complete — {len(self._path_to_anim)}/{n*n} squares",
                    "ok")

        tick()

    # ── Entry point ─────────────────────────────
    def _run_solver(self):
        """
        Called when the user clicks ▶ SOLVE.

        Validates state, disables UI, resets the board, then
        launches the selected algorithm in a daemon thread.
        """
        if self.solving:
            return
        self.solving = True
        self._stop = False
        self._run_btn.config(state="disabled", text="⏳ Solving…")
        self._anim_btn.config(state="disabled")
        self._reset_board()

        # Reset stats to "…" while solving
        for var in [self._stat_squares, self._stat_cov,
                    self._stat_time, self._stat_result]:
            var.set("…")

        if self.algo.get() == "backtracking":
            self._set_status("Running Backtracking + Warnsdorff…", "running")
            threading.Thread(target=self._run_bt, daemon=True).start()
        else:
            self._set_status("Running Genetic Algorithm…", "running")
            self._ga_prog_bar.pack(fill="x", pady=(2, 2))
            self._ga_gen_lbl.pack(anchor="w")
            threading.Thread(target=self._run_ga, daemon=True).start()

    # ── Backtracking thread ──────────────────────
    def _run_bt(self):
        """
        Worker thread for Backtracking.

        Runs in a separate thread so tkinter's event loop stays
        responsive. Results are posted back via `self.after(0, …)`.
        """
        from algorithms import backtracking_solve
        n = self.n.get()
        path, elapsed, success = backtracking_solve(n, self.start_r, self.start_c)
        # Post result to main thread (thread-safe)
        self.after(0, lambda: self._finish(path, elapsed, success))

    # ── GA thread ───────────────────────────────
    def _run_ga(self):
        """
        Worker thread for the Genetic Algorithm.

        A callback is passed to GA.solve() to push generation progress
        to the main thread via `self.after(0, …)` (thread-safe).
        """
        from algorithms import GeneticKnightsTour
        n    = self.n.get()
        pop  = self.pop_size.get()
        gens = self.gens.get()

        def cb(gen, best_fit, best_path):
            pct = int((gen / gens) * 100)
            self.after(0, lambda: self._update_ga_progress(gen, best_fit,
                                                            n * n, pct))

        ga = GeneticKnightsTour(
            n, start_x=self.start_r, start_y=self.start_c,
            pop_size=pop, generations=gens)
        path, elapsed, success = ga.solve(
            callback=cb, stop_flag=lambda: self._stop)
        self.after(0, lambda: self._ga_done(path, elapsed, success))

    # ── GA progress update (main thread) ────────
    def _update_ga_progress(self, gen, best, target, pct):
        """Update the progress bar and generation label."""
        self._ga_prog_bar["value"] = pct
        self._ga_gen_var.set(f"Gen {gen} | Best: {best}/{target}")

    def _ga_done(self, path, elapsed, success):
        """Hide GA progress bar then hand off to _finish()."""
        self._ga_prog_bar.pack_forget()
        self._ga_gen_lbl.pack_forget()
        self._finish(path, elapsed, success)

    # ── Finish (main thread) ─────────────────────
    def _finish(self, path, elapsed, success):
        """
        Called on the main thread after any solver completes.

        Updates statistics, re-enables UI, and starts the animation.
        """
        n = self.n.get()
        self.full_path = path
        total = n * n
        cov = round(len(path) / total * 100) if total else 0

        self._stat_squares.set(f"{len(path)}/{total}")
        self._stat_cov.set(f"{cov}%")
        self._stat_time.set(f"{elapsed:.4f}s")
        self._stat_result.set("✓" if success else "Partial")

        self._run_btn.config(state="normal", text="▶  SOLVE")
        self._anim_btn.config(state="normal")
        self.solving = False

        if success:
            self._set_status(f"Complete tour found in {elapsed:.4f}s!", "ok")
        else:
            self._set_status(
                f"Partial tour: {len(path)}/{total} squares in {elapsed:.4f}s",
                "fail")

        self._animate(path)
