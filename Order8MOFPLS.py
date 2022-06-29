from itertools import product

def solve_sudoku(size, grid):
    # """ An efficient Sudoku solver using Algorithm X.
    R, C = size
    N = R * C
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
         [("bn", bn) for bn in product(range(N), range(1, N + 1))] + 
         [("dn", bn) for bn in product(range(N), range(1, N + 1))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C) # a \times b Box number
        d = (r // C) * C + (c // R) # b \times a Box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n)),
            ("dn", (d, n))]
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

    solutions = 0

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
    MutOrthSet = []
    for solutions in solve_sudoku((a,b),grid):
        if MutOrthSet == []:
            MutOrthSet.append(solutions)
            for i in solutions:
                print(i)
            print('')
        else:
            if AreMutuallyOrthogonal(MutOrthSet,solutions) == True:
                MutOrthSet.append(solutions)
                for i in solutions:
                    print(i)
                print('')
        numOfSoltns += 1
        # for s in solutions:
        #     print(s)
        # print('solution numbe/r', numOfSoltns)
        # print('')
    print('There are', numOfSoltns, 'solutions')