import csv
from pathlib import Path

# Load words into a set at module level for efficiency
VALID_WORDS = set()


def load_words(filename="lemmatization_cleaned.csv"):
    """Load words from CSV into global set."""
    global VALID_WORDS
    csv_path = Path(filename)

    if csv_path.exists():
        with open(csv_path, "r") as f:
            reader = csv.reader(f)
            VALID_WORDS = {row[0].lower() for row in reader}


# Load words when module is imported
load_words()


def is_valid_word(word):
    """Check if word exists in loaded dictionary."""
    return word.lower() in VALID_WORDS


def find_words(matrix, max_length=8):
    rows = len(matrix)
    cols = len(matrix[0])
    words = set()

    def valid_position(x, y, visited):
        return 0 <= x < rows and 0 <= y < cols and (x, y) not in visited

    def dfs(x, y, visited, current_word):
        if len(current_word) >= max_length:
            return

        # Early validation check
        if len(current_word) >= 3 and is_valid_word(current_word):
            words.add(current_word.lower())

        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if valid_position(new_x, new_y, visited):
                dfs(
                    new_x,
                    new_y,
                    visited | {(new_x, new_y)},
                    current_word + matrix[new_x][new_y],
                )

    # Start DFS from each position
    for i in range(rows):
        for j in range(cols):
            dfs(i, j, {(i, j)}, matrix[i][j])

    return list(words)


def solve_word_matrix(matrix, max_length=8):
    # Initialize if not done
    if len(VALID_WORDS) == 0:
        load_words()

    words = find_words(matrix, max_length)
    return sorted(words, key=len, reverse=True)


# matrix_1 = [
#     ["K", "L", "L", "N", "F"],
#     ["A", "D", "M", "S", "E"],
#     ["R", "V", "B", "S", "P"],
#     ["A", "E", "L", "S", "L"],
#     ["N", "S", "E", "O", "R"],
# ]

# matrix_2 = [
#     ['D', 'A', 'E', 'A'],
#     ['I', 'A', 'O', 'K'],
#     ['A', 'R', 'D', 'Ö'],
#     ['E', 'I', 'A', 'V']
# ]
# print(solve_word_matrix(matrix_1))
