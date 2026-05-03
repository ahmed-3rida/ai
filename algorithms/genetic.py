# ─────────────────────────────────────────────
#  GENETIC ALGORITHM — CORE CLASS  (Person 4)
#  Knight's Tour Solver — CS212 AI Spring 2025
# ─────────────────────────────────────────────
import random
import time
from algorithms.moves import valid_moves, degree


class GeneticKnightsTour:
    """
    Genetic Algorithm for the Knight's Tour Problem.

    Representation
    --------------
    A **chromosome** is a list of (row, col) squares visited in order,
    starting from (start_x, start_y).  It is always a valid sequence of
    knight moves, built greedily.

    Fitness
    -------
    fitness(chromosome) = len(chromosome)
    The maximum possible fitness is n² (a complete tour).

    Parameters
    ----------
    n              : board size (n × n)
    start_x, start_y : fixed starting square (user-chosen)
    pop_size       : number of chromosomes in the population
    generations    : maximum number of evolution cycles
    mutation_rate  : probability of applying mutation to a child
    elite_frac     : fraction of top individuals kept unchanged each gen
    tournament_k   : competitors drawn for tournament selection
    """

    def __init__(self, n, start_x=0, start_y=0,
                 pop_size=200, generations=1000,
                 mutation_rate=0.15, elite_frac=0.1, tournament_k=5):
        self.n           = n
        self.start_x     = start_x
        self.start_y     = start_y
        self.pop_size    = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_size  = max(2, int(pop_size * elite_frac))
        self.tournament_k = tournament_k

    # ── Chromosome generation ──────────────────
    def random_tour(self):
        """
        Build one chromosome: a greedy random knight tour starting
        from (start_x, start_y).

        At each step we pick the neighbour with the lowest Warnsdorff
        degree, breaking ties randomly so different chromosomes diverge.
 
        Returns
        -------
        list of (row, col) – a valid (possibly partial) knight path
        """
        n = self.n
        visited = [[False] * n for _ in range(n)]
        x, y = self.start_x, self.start_y
        path = [(x, y)]
        visited[x][y] = True

        for _ in range(n * n - 1):
            moves = valid_moves(x, y, n, visited)
            if not moves:
                break
            # Warnsdorff + random tie-breaking → population diversity
            moves.sort(key=lambda p: (degree(p[0], p[1], n, visited),
                                       random.random()))
            x, y = moves[0]
            visited[x][y] = True
            path.append((x, y))

        return path

    # ── Fitness ────────────────────────────────
    def fitness(self, path):
        """Number of squares visited.  Higher is better (max = n²)."""
        return len(path)

    # ── Selection: Tournament ──────────────────
    def tournament_select(self, population):
        """
        Randomly pick `tournament_k` individuals and return the fittest.
        This creates selection pressure while keeping diversity.

        Returns
        -------
        list – the winning chromosome
        """
        sample = random.sample(population, min(self.tournament_k,
                                               len(population)))
        return max(sample, key=self.fitness)

    # ── Mutation: Segment restart ──────────────
    def mutate(self, path):
        """
        Cut the path at a random point, then re-grow the tail greedily.

        This preserves the start of a good path while exploring new
        continuations — a form of 'local search' inside the GA.

        Returns
        -------
        list – mutated chromosome (always starts from start_x, start_y)
        """
        if len(path) < 3:
            return self.random_tour()

        n = self.n
        cut = random.randint(1, len(path) - 1)
        new_path = list(path[:cut])

        visited = [[False] * n for _ in range(n)]
        for (x, y) in new_path:
            visited[x][y] = True

        x, y = new_path[-1]
        for _ in range(n * n - cut):
            moves = valid_moves(x, y, n, visited)
            if not moves:
                break
            moves.sort(key=lambda p: (degree(p[0], p[1], n, visited),
                                       random.random()))
            x, y = moves[0]
            visited[x][y] = True
            new_path.append((x, y))

        return new_path

    # ── Main GA loop ───────────────────────────
    def solve(self, callback=None, stop_flag=None):
        """
        Run the genetic algorithm.

        Each generation:
          1. Sort population by fitness (descending).
          2. Keep the elite (best elite_size individuals unchanged).
          3. Fill the rest via tournament selection + mutation.
          4. Check for a complete tour (fitness == n²).

        Parameters
        ----------
        callback  : callable(gen, best_fitness, best_path) – called each gen
        stop_flag : callable() → bool – if True, stop early

        Returns
        -------
        best_path : list of (row, col)
        elapsed   : float – seconds taken
        success   : bool – True if n² squares were visited
        """
        n      = self.n
        target = n * n

        population = [self.random_tour() for _ in range(self.pop_size)]
        best_path  = max(population, key=self.fitness)
        t0 = time.time()

        for gen in range(self.generations):
            if stop_flag and stop_flag():
                break

            population.sort(key=self.fitness, reverse=True)

            if self.fitness(population[0]) > self.fitness(best_path):
                best_path = population[0]

            if callback:
                callback(gen, self.fitness(best_path), best_path)

            if self.fitness(best_path) == target:
                break   # perfect solution found

            # ── Build next generation ──
            new_pop = population[:self.elite_size]   # elitism
            while len(new_pop) < self.pop_size:
                p1    = self.tournament_select(population)
                child = self.mutate(p1)
                new_pop.append(child)
            population = new_pop

        elapsed = time.time() - t0
        success = self.fitness(best_path) == target
        return best_path, elapsed, success
