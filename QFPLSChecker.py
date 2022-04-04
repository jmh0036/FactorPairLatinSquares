# -*- coding: utf-8 -*-
import math
import sys

FactorPairs = [[1,24],[24,1],[2,12],[12,2],[3,8],[4,6],[6,4]]

grid = [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
[13,14,15,16,17,18,19,20,21,22,23,24,1,2,3,4,5,6,7,8,9,10,11,12],
[7,8,9,10,11,12,1,2,3,4,5,6,19,20,21,22,23,24,13,14,15,16,17,18],
[19,20,21,22,23,24,13,14,15,16,17,18,7,8,9,10,11,12,1,2,3,4,5,6],
[6,18,12,24,3,4,9,10,7,19,1,13,5,17,11,23,15,16,21,22,8,20,2,14],
[5,17,11,23,15,16,21,22,8,20,2,14,6,18,12,24,3,4,9,10,7,19,1,13],
[3,4,1,2,7,8,5,6,11,12,9,10,15,16,13,14,19,20,17,18,23,24,21,22],
[15,16,13,14,19,20,17,18,23,24,21,22,3,4,1,2,7,8,5,6,11,12,9,10],
[9,10,7,8,1,2,11,12,5,6,3,4,21,22,19,20,13,14,23,24,17,18,15,16],
[21,22,19,20,13,14,23,24,17,18,15,16,9,10,7,8,1,2,11,12,5,6,3,4],
[12,24,6,18,9,10,3,4,1,13,7,19,11,23,5,17,21,22,15,16,2,14,8,20],
[11,23,5,17,21,22,15,16,2,14,8,20,12,24,6,18,9,10,3,4,1,13,7,19],
[2,1,4,3,6,5,8,7,10,9,12,11,14,13,16,15,18,17,20,19,22,21,24,23],
[14,13,16,15,18,17,20,19,22,21,24,23,2,1,4,3,6,5,8,7,10,9,12,11],
[8,7,10,9,12,11,2,1,4,3,6,5,20,19,22,21,24,23,14,13,16,15,18,17],
[20,19,22,21,24,23,14,13,16,15,18,17,8,7,10,9,12,11,2,1,4,3,6,5],
[18,6,24,12,4,3,10,9,19,7,13,1,17,5,23,11,16,15,22,21,20,8,14,2],
[17,5,23,11,16,15,22,21,20,8,14,2,18,6,24,12,4,3,10,9,19,7,13,1],
[4,3,2,1,8,7,6,5,12,11,10,9,16,15,14,13,20,19,18,17,24,23,22,21],
[16,15,14,13,20,19,18,17,24,23,22,21,4,3,2,1,8,7,6,5,12,11,10,9],
[10,9,8,7,2,1,12,11,6,5,4,3,22,21,20,19,14,13,24,23,18,17,16,15],
[22,21,20,19,14,13,24,23,18,17,16,15,10,9,8,7,2,1,12,11,6,5,4,3],
[24,12,18,6,10,9,4,3,13,1,19,7,23,11,17,5,22,21,16,15,14,2,20,8],
[23,11,17,5,22,21,16,15,14,2,20,8,24,12,18,6,10,9,4,3,13,1,19,7]]

#Size of Factor Pair Latin Square
n = len(grid)

#Find Factor pairs of n
#def FactorPairs(value):
    #if value < 1:
        #return []
    #factors = [[1, value]]
    #for i in xrange(2, int(math.sqrt(value))+1):
        #if value % i == 0:
            #factors.append([i, value / i])
    #return factors

#Declare Variables
    
#General Factor Pair Check (including Rows and columns
#Requires a list to be passed to it.  i.e. array[]
def Checker(list):
  for i in range(0,n-1):
    for j in range(i+1,n):
      if list[i] != 0 and list[i] == list[j]:
        return False
  return True

#General Factor Pair Checker
def GeneralChecker(position):
  # entry1 = 0
  # entry2 = 0
  # counter = 0
  #check a x b
  number1 = FactorPairs[position][0]
  number2 = FactorPairs[position][1]
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
      
#Print Stuff
print('Factor Pairs of order',n,'are:',FactorPairs)
for row in grid:
  print(row)
for i in range(0,len(FactorPairs)):
  if GeneralChecker(i) == False:
    print('This IS NOT a Factor Pair Latin Square')
    sys.exit()
print('This IS INDEED a Factor Pair Latin Square!')
