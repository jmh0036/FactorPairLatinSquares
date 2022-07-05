from itertools import product
import copy

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

def IsOrthogonal(grid1,grid2):
    SetOfOrderedPairs = set()
    for i in range(len(grid1)):
        for j in range(len(grid1)):
            SetOfOrderedPairs.add((grid1[i][j],grid2[i][j]))
    if len(SetOfOrderedPairs) != len(grid1)**2:
        return False
    else:
        return True

def AreMutuallyOrthogonal(arrayOfarrays,testArray):
    # if arrayOfarrays == []:
    #     return True
    for i in arrayOfarrays:
        if IsOrthogonal(i,testArray) == False:
            return False
    return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    a = 2
    b = 4
    n = a*b

    grid = [
        [1,2,3,4,5,6,7,8],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
    ]

    numOfSoltns = 0
    
    MutOrthSet = [
    [
    [1, 2, 3, 4, 5, 6, 7, 8],
    [8, 7, 6, 5, 4, 3, 2, 1],
    [4, 3, 2, 1, 8, 7, 6, 5],
    [5, 6, 7, 8, 1, 2, 3, 4],
    [7, 8, 5, 6, 3, 4, 1, 2],
    [2, 1, 4, 3, 6, 5, 8, 7],
    [6, 5, 8, 7, 2, 1, 4, 3],
    [3, 4, 1, 2, 7, 8, 5, 6]
    ],

    [
    [1, 2, 3, 4, 5, 6, 7, 8],
    [6, 5, 8, 7, 2, 1, 4, 3],
    [8, 7, 6, 5, 4, 3, 2, 1],
    [3, 4, 1, 2, 7, 8, 5, 6],
    [4, 3, 2, 1, 8, 7, 6, 5],
    [7, 8, 5, 6, 3, 4, 1, 2],
    [5, 6, 7, 8, 1, 2, 3, 4],
    [2, 1, 4, 3, 6, 5, 8, 7]
    ],

    [
    [1, 2, 3, 4, 5, 6, 7, 8],
    [5, 6, 7, 8, 1, 2, 3, 4],
    [3, 4, 1, 2, 7, 8, 5, 6],
    [7, 8, 5, 6, 3, 4, 1, 2],
    [2, 1, 4, 3, 6, 5, 8, 7],
    [6, 5, 8, 7, 2, 1, 4, 3],
    [4, 3, 2, 1, 8, 7, 6, 5],
    [8, 7, 6, 5, 4, 3, 2, 1]
    ]
    ]

    for solution in solve_sudoku([(1,n),(n,1),(a,b),(b,a)],grid):
        if MutOrthSet == []:
            MutOrthSet.append(copy.deepcopy(solution))
            for i in solution:
                print(i)
            print('')
        else:
            if AreMutuallyOrthogonal(MutOrthSet,solution) == True:
                MutOrthSet.append(copy.deepcopy(solution))
                for i in solution:
                    print(i)
                print('')
        numOfSoltns += 1
        # for s in solution:
        #     print(s)
        WhenToPrint = 1000000
        if numOfSoltns%WhenToPrint == 0:
            print('There are over', numOfSoltns//WhenToPrint, 'million solutions')
        # print('')
    print('There are', numOfSoltns, 'solutions')