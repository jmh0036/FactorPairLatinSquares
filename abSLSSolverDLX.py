#!/usr/bin/env python3

# Author: Ali Assaf <ali.assaf.mail@gmail.com>
# Copyright: (C) 2010 Ali Assaf
# License: GNU General Public License <http://www.gnu.org/licenses/>

from itertools import product

def solve_sudoku(size, grid):
    # """ An efficient Sudoku solver using Algorithm X.
    R, C = size
    N = R * C
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
         [("bn", bn) for bn in product(range(N), range(1, N + 1))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C) # Box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #Good Example
    # grid = [
    # [5, 3, 4, 6, 7, 8, 9, 1, 2],
    # [6, 7, 2, 1, 9, 5, 3, 4, 8],
    # [1, 9, 8, 3, 0, 0, 5, 6, 7],
    # [8, 5, 9, 7, 6, 1, 4, 2, 3],
    # [4, 2, 6, 8, 5, 3, 7, 9, 1],
    # [7, 1, 3, 9, 0, 0, 8, 5, 6],
    # [9, 6, 1, 5, 3, 7, 2, 8, 4],
    # [2, 8, 7, 4, 1, 9, 6, 3, 5],
    # [3, 4, 5, 2, 8, 6, 1, 7, 9]]
    # for solution in solve_sudoku((3, 3), grid):
    #     for s in solution:
    #         print(s)
    #     print('')

    # grid = [
    # [1,2,3,4,5,6],
    # [4,5,6,1,2,3],
    # [3,6,2,5,1,4],
    # [0,0,0,0,0,0],
    # [0,0,0,0,0,0],
    # [0,0,0,0,0,0]
    # ]
    a = 2
    b = 3
    n = a*b
    grid2 = [ [0 for i in range(n)] for j in range(n) ]
    # for solution in solve_sudoku((2,3),grid):
    #     if solution in solve_sudoku((3,2),grid2):
    #         for s in solution:
    #             print(s)
    #         print('')

    for solutions in solve_sudoku((a,b),grid2):
        for s in solutions:
            print(s)
        print('')
