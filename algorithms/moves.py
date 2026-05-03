# ─────────────────────────────────────────────
#  KNIGHT MOVES & HELPERS  (Person 2)
#  Knight's Tour Solver — CS212 AI Spring 2025
# ─────────────────────────────────────────────

# All 8 L-shaped moves a knight can make (row_delta, col_delta)
MOVES = [
    ( 2,  1), ( 2, -1),
    (-2,  1), (-2, -1),
    ( 1,  2), ( 1, -2),
    (-1,  2), (-1, -2),
]


def valid_moves(x, y, n, visited):
    """
    Return all valid, unvisited squares reachable by a knight
    from position (x, y) on an n×n board.

    Parameters
    ----------
    x, y    : current row and column (0-indexed)
    n       : board size
    visited : 2-D boolean list – True means the square was already visited

    Returns
    -------
    list of (nx, ny) tuples – each is a legal next position
    """
    return [
        (x + dx, y + dy)
        for dx, dy in MOVES
        if 0 <= x + dx < n
        and 0 <= y + dy < n
        and not visited[x + dx][y + dy]
    ]


def degree(x, y, n, visited):
    """
    Warnsdorff's heuristic value for square (x, y):
    the number of onward moves available from that square.

    A lower degree means the square is harder to reach later,
    so we prefer to visit it sooner (greedy heuristic).

    Parameters
    ----------
    x, y    : row and column
    n       : board size
    visited : 2-D boolean list

    Returns
    -------
    int – count of unvisited neighbours
    """
    return len(valid_moves(x, y, n, visited))
