import cProfile
import pstats

from rabbel_solver.solver import solve_word_matrix as solve_word_matrix_1
from rabbel_solver.solver2 import solve_word_matrix as solve_word_matrix_2

matrix_1 = [
    ["K", "L", "L", "N", "F"],
    ["A", "D", "M", "S", "E"],
    ["R", "V", "B", "S", "P"],
    ["A", "E", "L", "S", "L"],
    ["N", "S", "E", "O", "R"],
]

matrix_2 = [
    ["D", "A", "E", "A"],
    ["I", "A", "O", "K"],
    ["A", "R", "D", "Ö"],
    ["E", "I", "A", "V"],
]


def profile_solver_1():
    profiler = cProfile.Profile()
    profiler.enable()

    # Your test code here
    solve_word_matrix_1(matrix_1)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats("cumulative")
    stats.print_stats(20)  # Show top 20 time-consuming functions


def profile_solver_2():
    profiler = cProfile.Profile()
    profiler.enable()

    # Your test code here
    solve_word_matrix_2(matrix_1)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats("cumulative")
    stats.print_stats(20)  # Show top 20 time-consuming functions


# Run with profiler
# profile_solver_1()

# Run with profiler
profile_solver_2()
