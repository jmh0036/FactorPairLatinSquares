import math
import sys
# import time
# This is really just a git test.

#Size of Factor Pair Latin Square
n = 6

#Define the empty Array of size $n$
grid = [[0 for x in range(n)] for y in range(n)]

#construct the Factor Pair Latin Square
#name the first row $1 \ldots n$
for i in range(0,n):
  grid[0][i] = i+1
#Note:  You can enter a partially filled in FPLS by putting
#grid = $[[#,#,#,\ldots,#],[#,#,#,\ldots,#],\ldots,[#,#,#,...,#]]$
#Any unfilled cell, make 0
  
#Find Factor pairs of n
def FactorPairs(value):
    if value < 1:
      return []
    #Append $1 \times n$ factor pair
    factors = [[1, value]]
    #Append $n \times 1$ factor pair
    factors.append([value,1])
    for i in range(2, int(math.sqrt(value))+1):
        if value % i == 0:
          #Append $a \times b$ factor pair
          factors.append([i, value // i])
          #If $a \neq b$, append $b \times a$ factor pair
          if i != (value/i):
            factors.append([value//i, i])
    return factors

#Declare Variables
    
#General Factor Pair Check (including Rows and columns)
#Requires a list to be passed to it.  i.e. array[]
def Checker(list):
  for i in range(0,n-1):
    for j in range(i+1,n):
      if list[i] != 0 and list[i] == list[j]:
        return False
  return True

#General Factor Pair Checker
def GeneralChecker(position):
  #Check the a $\times$ b squares
  #It should be noted that we only need to check the a $\times b$ squares, 
  #since the $b \times a$ squares will be checked as the next (or previous)
  #factor pair in FactorPairs(n) 
  number1 = FactorPairs(n)[position][0]
  number2 = FactorPairs(n)[position][1]
  row = []
  for level in range(0,n,number1):
    for section in range(0,n,number2):
      for i in range(level,level+number1):
        for j in range(section,section+number2):
          row.append(grid[i][j])
          if len(row) == n:
            if Checker(row) == False:
              return False
            row = []
  return True

def OverallCheck(list):
  for i in range(0,len(FactorPairs(n))):
    if GeneralChecker(i) == False:
      return False
  return True
  
#Define Positions that are unchangeable (i.e. Fixed.)  
Forbidden = [[0 for x in range(n)] for y in range(n)]
for row in range(0,n):
  for column in range(0,n):
    if grid[row][column] != 0:
      Forbidden[row][column] = 1

#Solver
def Solve(row, column):
  #In case the cell passed to function is fixed, go to next non-fixed cell
  while (Forbidden[row][column] == 1):
    #Try next cell
    column = column + 1
    #Advance row if necessary
    if (column > (n-1)):
      column = 0
      row = row + 1
    if (row > (n-1)):
      return True
  
  #Once we have our cell coordinates, substitute in a number and check it
  for intGuess in range(1,n+1):
    intTryRow = 0
    intTryColumn = 0
    grid[row][column] = intGuess
    #Print each guess to see what's going on.
    for i in grid:
      print(i)
    print('-----------')
    #If good, Solve the next one
    if(OverallCheck(grid)):
      #Try the next square, preserving current values
      intTryColumn = column + 1
      intTryRow = row
      #Check if the tow needs to be advanced
      if (intTryColumn > (n-1)):
        intTryColumn = 0
        intTryRow = intTryRow + 1
      if (intTryRow > (n-1)):
	      return True
      #check if we're done
      if(Solve(intTryRow, intTryColumn)):
        return True
  #If none of the numbers we've checked are right, put this cell back to 0
  #and return False
  grid[row][column] = 0
  return False

# t = time.clock()  
Solve(0,0)
#Double Check
#print grid
for i in grid:
  print(i)
#Double check
print('Double Check:')
if OverallCheck(grid) == False:
    print('This IS NOT a Factor Pair Latin Square')
    sys.exit()
for i in range(0,n):
  for j in range(0,n):
    if grid[i][j] == 0:
      print('This IS NOT a Factor Pair Latin Square')
      sys.exit()
print('This IS INDEED a Factor Pair Latin Square!')
# print('Took %.3f seconds.' % (time.clock()-t))