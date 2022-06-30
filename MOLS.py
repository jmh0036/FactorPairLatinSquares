from itertools import product
import copy

def solve_sudoku(grid):
    # """ An efficient Sudoku solver using Algorithm X.
    # R, C = size
    N = len(grid)
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] )
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n))]
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

def IsOrthogonal(grid1,grid2):
    SetOfOrderedPairs = set()
    for i in range(len(grid1)):
        for j in range(len(grid1)):
            SetOfOrderedPairs.add((grid1[i][j],grid2[i][j]))

    # print(grid1, grid2, SetOfOrderedPairs)
    # for i in range(len(grid1)):
    #     print(grid1[i], grid2[i])
    # print(SetOfOrderedPairs)
    # print(grid2)

    if len(SetOfOrderedPairs) != len(grid1)**2:
        return False
    else:
        return True

def AreMutuallyOrthogonal(arrayOfarrays,testArray):
    # print(arrayOfarrays, testArray)

    # diagonal = set()
    # for i in range(len(testArray)):
    #     diagonal.add(testArray[i][i])
    # if len(diagonal) in [len(testArray),1]:
    #     idempotent = True
    # else:
    #     idempotent = False
    
    if len(arrayOfarrays) == 0:
        # if idempotent == True:
        #     return True
        # else:
        #     return False
        return True
    for i in arrayOfarrays:
        # for j in range(len(i)):
        #     print(i[j], testArray[j])
        # print('')
        if IsOrthogonal(i,testArray) == False:
            return False
    return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    grid = [
        [1,2,3,4,5,6,7],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ]

    numOfSoltns = 0
    MutOrthLst = []
    # print(type(solve_sudoku(grid)))
    for solution in solve_sudoku(grid):
        # print(MutOrthLst, solution, AreMutuallyOrthogonal(MutOrthLst, solution[:]))
        # print(MutOrthLst, solution)
        if AreMutuallyOrthogonal(MutOrthLst, solution[:]) == True:
            MutOrthLst.append(copy.deepcopy(solution))
            for i in solution:
                print(i)
            print('')
        numOfSoltns += 1
        
        # for s in solution:
        #     print(s)
        # print('solution number', numOfSoltns)
        # print('')
    print('There are', numOfSoltns, 'solutions')

    print(MutOrthLst, len(MutOrthLst))

# print(AreMutuallyOrthogonal([[[1, 2, 3], [3, 1, 2], [2, 3, 1]]], [[1, 2, 3],[2, 3, 1],[3, 1, 2]]))

# print(IsOrthogonal([[1, 2, 3], [3, 1, 2], [2, 3, 1]],[[1, 2, 3],[2, 3, 1],[3, 1, 2]]))