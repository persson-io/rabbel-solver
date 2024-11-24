# app.py
from flask import Flask, render_template, request

from rabbel_solver.solver2 import solve_word_matrix

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        size = int(request.form.get("size", 4))  # Default to 4x4
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                cell_value = request.form.get(f"cell_{i}_{j}", "").upper()
                row.append(cell_value)
            matrix.append(row)

        solutions = solve_word_matrix(matrix)
        # Group solutions by word length
        grouped_solutions = {}
        for word in solutions:
            length = len(word)
            if length not in grouped_solutions:
                grouped_solutions[length] = []
            grouped_solutions[length].append(word)

        # Sort groups
        sorted_groups = dict(sorted(grouped_solutions.items()))
        total_words = len(solutions)
        # Debugging
        # print("Debug - Template variables:")
        # print(f"grouped_solutions: {bool(sorted_groups)}")
        # print(f"total_words: {total_words}")
        # print(f"matrix: {bool(matrix)}")
        return render_template(
            "results.html",
            grouped_solutions=sorted_groups,
            total_words=total_words,
            matrix=matrix,
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
