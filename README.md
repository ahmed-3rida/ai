# Knight's Tour Problem Solver 🐴

> CS212 Artificial Intelligence — Spring 2025  
> HNU University

A Python desktop application that solves the **Knight's Tour** chess problem using two AI algorithms, with a fully interactive Tkinter GUI.

---

## 📖 Problem Description

The Knight's Tour is a classic combinatorial problem where a chess knight must visit **every square on an n×n board exactly once**, making only valid L-shaped moves.

---

## 🧠 Algorithms

### 1. Backtracking + Warnsdorff's Heuristic
- Recursively explores all possible knight paths
- Uses **Warnsdorff's Rule** to always move to the square with the fewest onward moves
- Near-instant for boards up to 12×12

### 2. Genetic Algorithm
- Evolves a population of knight-tour chromosomes over generations
- Uses **Tournament Selection** and **Segment-Restart Mutation**
- Configurable population size and generation count

---

## 🖥️ Features

- 🎨 Modern dark-themed desktop GUI (Tkinter)
- 📐 User-selectable board size: **5×5 to 12×12**
- 🖱️ Click any cell to set the **start position**
- ▶️ Step-by-step animated knight movement
- ⚡ Algorithms run in background threads — UI never freezes
- 📊 Live statistics: squares visited, coverage %, solve time

---

## 🗂️ Project Structure

```
knights_tour_project/
├── main.py                   # Entry point — run this!
├── constants.py              # Colours and shared config
├── algorithms/
│   ├── moves.py              # Knight move logic + Warnsdorff heuristic
│   ├── backtracking.py       # Backtracking algorithm
│   └── genetic.py            # Genetic Algorithm class
├── gui/
│   ├── app.py                # Main application window
│   ├── board.py              # Board rendering & interaction
│   ├── controls.py           # Left control panel
│   └── solver.py             # Threading, animation & results
└── docs/
    ├── 01_person1_overview_constants.md
    ├── 02_person2_knight_moves.md
    ├── 03_person3_backtracking.md
    ├── 04_person4_genetic_core.md
    ├── 05_person5_genetic_operators.md
    ├── 06_person6_gui_board.md
    ├── 07_person7_gui_controls.md
    ├── 08_person8_solver_animation.md
    └── 09_person9_main_app.md
```

---

## 🚀 How to Run

### Requirements
- Python 3.9+
- No external packages needed — only the standard library (`tkinter`, `random`, `time`, `threading`)

### Run
```bash
cd knights_tour_project
python main.py
```

---

## 🎮 How to Use

1. **Set board size** using the slider (5–12)
2. **Click any cell** on the board to set the start position
3. **Choose algorithm**: Backtracking or Genetic
4. *(For Genetic)* Tune population size and generations
5. Click **▶ SOLVE** and watch the knight move!
6. Click **↺ Replay Animation** to re-watch

---

## 📚 Development Platform

- **Language:** Python 3.9+
- **GUI Library:** `tkinter` (built-in)
- **IDE:** VS Code / PyCharm
- **OS:** Windows / Linux / macOS
