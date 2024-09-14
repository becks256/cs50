import sys

from crossword import *


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        # print(self.crossword)
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
        constraints; in this case, the length of the word.)
        """
        # print(self.domains)
        for x in self.domains:
            # Get the word length constraint from the variable tuple (e.g., 5 in (0, 1) down: 5)
            word_length = x.length
            # print("word length", word_length)
            # print("y before", self.domains[x])
            self.domains[x] = {
                word for word in self.domains[x] if len(word) == word_length
            }
            # print("y after", self.domains[x])

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        to_remove = []

        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False  # No overlap means no need to revise

        i, j = overlap

        # Iterate over each value in the domain of x
        for word_x in self.domains[x]:
            is_consistent = False

            # Check if there exists a word_y in y's domain such that word_x and word_y match at the overlap position
            for word_y in self.domains[y]:
                if word_x[i] == word_y[j]:
                    is_consistent = True
                    break

            # If no consistent word_y was found, mark word_x for removal
            if not is_consistent:
                to_remove.append(word_x)

        # Remove all inconsistent values from x's domain after iteration
        if to_remove:
            for word in to_remove:
                self.domains[x].remove(word)
            revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs is None:
            arcs = []
            for x in self.domains:
                for y in self.domains:
                    if x != y:
                        arcs.append((x, y))

        queue = list(arcs)

        while queue:
            (x, y) = queue.pop(0)

            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.domains:
                    # if z is not x (what we just revised) and z is not y (what we just revised against); ie all neighbors of x exclusive of those we just looked at
                    if z != x and z != y:
                        queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        return set(assignment.keys()) == self.crossword.variables

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for var in assignment:
            word = assignment[var]

            # ensure the word matches the length of the variable
            if len(word) != var.length:
                return False

            # ensure the word does not conflict with neighboring variables
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    other_word = assignment[neighbor]
                    overlap = self.crossword.overlaps[var, neighbor]

                    if overlap is not None:
                        i, j = overlap
                        if word[i] != other_word[j]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        def count_ruled_out_values(value):
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    for neighbor_value in self.domains[neighbor]:
                        if not self.consistent({var: value, neighbor: neighbor_value}):
                            count += 1
            return count

        return sorted(self.domains[var], key=count_ruled_out_values)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        unassigned = [var for var in self.crossword.variables if var not in assignment]

        # Minimum Remaining Values (MRV) heuristic
        mrv = min(unassigned, key=lambda var: len(self.domains[var]))

        # Degree heuristic (if there’s a tie)
        mrv_with_degree = [
            var
            for var in unassigned
            if len(self.domains[var]) == len(self.domains[mrv])
        ]
        if len(mrv_with_degree) > 1:
            return max(
                mrv_with_degree, key=lambda var: len(self.crossword.neighbors(var))
            )

        return mrv

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
