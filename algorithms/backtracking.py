# ─────────────────────────────────────────────
#  BACKTRACKING  (Person 3)
#  Knight's Tour Solver — CS212 AI Spring 2025
# ─────────────────────────────────────────────
import time
# pyrefly: ignore [parse-error]
from algorithms import valid_moves , degree


def backtracking_solve(n, sx, sy):
    """
    Solve the Knight's Tour using standard Backtracking.

    Algorithm Steps
    ---------------
    1. Start at (sx, sy) and mark it visited.
    2. At each step, list all valid unvisited neighbours.
    3. Recurse into the first valid neighbour.
    4. If all n² squares are visited → SUCCESS.
    5. If stuck → backtrack (un-mark current square, pop from path).
    
    Solve the Knight's Tour using Backtracking with Warnsdorff's heuristic.
    Algorithm Steps
    ---------------
    1. Start at (sx, sy) and mark it visited.
    2. At each step, list all valid unvisited neighbours.    
    3. Sort them by Warnsdorff's degree (fewest onward moves first).
    4. Recurse into the best neighbour.
    5. If all n² squares are visited → SUCCESS.
    6. If stuck → backtrack (un-mark current square, pop from path).
    Parameters
    ----------
    n        : board size (n × n)
    sx, sy   : starting row and column (0-indexed)

    Returns
    -------
    path     : list of (row, col) in visit order  (empty if no solution)
    elapsed  : time taken in seconds (float)
    success  : True if a complete tour was found
    """
    visited = [[False] * n for _ in range(n)]
    path = []

    def bt(x, y, step):
        """Recursive backtracking helper."""
        visited[x][y] = True
        path.append((x, y))

        # Base case: all squares visited
        if step == n * n:
            return True

        # Generate valid neighbours
        neighbours = valid_moves(x, y, n, visited)
        # Generate neighbours and sort by Warnsdorff's degree
        neighbours.sort(key=lambda p: degree(p[0], p[1], n, visited))

        for nx, ny in neighbours:
            if bt(nx, ny, step + 1):
                return True  # solution found down this branch

        # Backtrack: undo the move
        visited[x][y] = False
        path.pop()
        return False

    t0 = time.time()
    success = bt(sx, sy, 1)
    elapsed = time.time() - t0

    return path, elapsed, success
