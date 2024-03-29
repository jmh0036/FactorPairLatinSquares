from itertools import product, islice
import copy
import random as rnd
import json

def solve_sudoku(sizes, grid):
    N = len(grid)
    # """ An efficient Sudoku solver using Algorithm X.
    X = ([("rc", rc) for rc in product(range(N), range(N))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        Y[(r, c, n)] = [("rc", (r, c))]
    for size in sizes:
        R, C = size
        # N = R * C
        X += [("r%s"%str(size), rn) for rn in product(range(N), range(1, N + 1))]
        for r, c, n in product(range(N), range(N), range(1, N + 1)):
            Y[(r, c, n)] += [("r%s"%str(size), ((r // R) * R + (c // C), n))]
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))
    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        yield grid

def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y

def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

class Cell:
    def __init__(self, value: str, id: int, row: int, col: int, value_start: vars, value_correct: int) -> None:
        self.value = value
        self.id = id
        self.row = row
        self.col = col
        self.value_start = value_start
        self.value_correct = value_correct

if __name__ == "__main__":
    # Let's define the list of things to be latin so we can reuse it.
    LatinList = ((1,6),(6,1),(2,3),(3,2))

    Order = LatinList[0][0]*LatinList[0][1]

    # Creating a random first row
    RemainingChoices = list(range(1,Order+1))
    FirstRow = []
    while RemainingChoices != []:
        NextElement = rnd.choice(RemainingChoices)
        FirstRow.append(NextElement)
        RemainingChoices.remove(NextElement)

    # Initial Puzzle
    TestPuzzle = [FirstRow]
    for i in range(Order-1):
        TestPuzzle.append([0 for i in range(Order)])

    UniquePuzzle = []

    # Pick a solution to trim from.
    WhichSol = rnd.randint(0,1935)
    TestPuzzle = solution = list(islice(solve_sudoku(LatinList,TestPuzzle),WhichSol,WhichSol+1))[0]
    
    # print('TestPuzzle Chosen:')
    # for i in TestPuzzle:
    #     print(i)
    # print('')

    numOfSolutions = 1
    while numOfSolutions == 1:
        UniquePuzzle = copy.deepcopy(TestPuzzle)
        randomRow = rnd.randint(0,Order-1)
        randomCol = rnd.randint(0,Order-1)
        TestPuzzle[randomRow][randomCol] = 0
        solution = solve_sudoku(LatinList,copy.deepcopy(TestPuzzle))
        numOfSolutions = 0 
        for sol in solution:
            numOfSolutions += 1
            if numOfSolutions > 1:
                break

    # print('Puzzle before trimming:')
    # for p in UniquePuzzle:
    #     print(p)

    # Minimize clues in the puzzle
    TestPuzzle = copy.deepcopy(UniquePuzzle)
    for row in range(len(TestPuzzle)):
        for col in range(len(TestPuzzle)):
            TestPuzzle[row][col] = 0
            numOfSolutions = 0
            for sol in solve_sudoku(LatinList,copy.deepcopy(TestPuzzle)):
                numOfSolutions += 1
            if numOfSolutions == 1:
                UniquePuzzle = copy.deepcopy(TestPuzzle)
            else:
                TestPuzzle = copy.deepcopy(UniquePuzzle)

    print('')

    print('Puzzle after trimming:')
    for p in UniquePuzzle:
        print(p)

    print('')

    CorrectAnswer = list(solve_sudoku(LatinList,copy.deepcopy(UniquePuzzle)))[0]

    print('solutions')
    for s in CorrectAnswer:
        print(s)
    print('')

    # Construct List of cell objects
    ListOfCells = []
    idNo = -1
    for i in range(len(UniquePuzzle)):
        for j in range(len(UniquePuzzle)):
            idNo += 1
            ListOfCells.append(Cell(None,idNo,i,j,None if UniquePuzzle[i][j] == 0 else UniquePuzzle[i][j],CorrectAnswer[i][j]))

    # Write to JSON file
    jsonStr = json.dumps([ob.__dict__ for ob in ListOfCells], indent=4)

    jsonFile = open("test_square_data.json", "w")
    jsonFile.write(jsonStr)
    jsonFile.close()
