from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# does kb entail alpha
# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Implication(AKnight, AKnave),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

# We are both knaves => AKnave && BKnave
AStatement1 = And(AKnave, BKnave)
knowledge1 = And(
    Implication(AKnave, Not(AStatement1)),  # If A is a knave, A is lying
    Implication(AKnight, AStatement1),  # If A is a knight, A is tellign the truth
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
AStatement2 = Or(And(AKnight, BKnight), And(AKnave, BKnave))
BStatement2 = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    Implication(AKnave, Not(AStatement2)),  # If A is a knave, A is lying
    Implication(AKnight, AStatement2),  # If A is a knight, A is tellign the truth
    Implication(BKnave, Not(BStatement2)),  # If B is a knave, B is lying
    Implication(BKnight, BStatement2),  # If B is a knight, B is telling the truth
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
AStatement3 = Or(AKnight, AKnave)
BStatement3 = And(AKnave, CKnave)
CStatement3 = AKnight
Statements3 = [
    (AKnight, AKnave, AStatement3),
    (BKnight, BKnave, BStatement3),
    (CKnight, CKnave, CStatement3),
]

knowledge3 = And()

# dynamically add implications stating if a knave said the thing, its a lie and if a knight said it, its the truth
for knight, knave, statement in Statements3:
    knowledge3.add(Implication(knave, Not(statement)))
    knowledge3.add(Implication(knight, statement))

shared_knowledge = [
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
]

# dynamically add common knowledge for the puzzle
for k in shared_knowledge:
    for kb in [knowledge0, knowledge1, knowledge2, knowledge3]:
        kb.add(k)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
