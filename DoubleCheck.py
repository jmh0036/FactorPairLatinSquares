import copy

def IsOrthogonal(grid1,grid2):
    SetOfOrderedPairs = set()
    for i in range(len(grid1)):
        for j in range(len(grid1)):
            SetOfOrderedPairs.add((grid1[i][j],grid2[i][j]))
    if len(SetOfOrderedPairs) != len(grid1)**2:
        return False
    else:
        return True

def AreMutuallyOrthogonal(arrayOfarrays):
    if arrayOfarrays == []:
        return True
    for i in range(len(arrayOfarrays)-1):
        for j in range(i+1,len(arrayOfarrays)):
            if IsOrthogonal(arrayOfarrays[i],arrayOfarrays[j]) == False:
                return False
    return True

def Normalize(arr):
    LocalDict = dict()
    for i in range(len(arr)):
        LocalDict[arr[0][i]] = i
    LocalArray = copy.deepcopy(arr)
    for i in range(len(LocalArray)):
        for j in range(len(LocalArray)):
            LocalArray[i][j] = LocalDict[LocalArray[i][j]] + 1 
    return LocalArray

array1 = [
    [0,1,3,2,6,7,5,4],
    [4,5,7,6,2,3,1,0],
    [2,3,1,0,4,5,7,6],
    [6,7,5,4,0,1,3,2],
    [5,4,6,7,3,2,0,1],
    [1,0,2,3,7,6,4,5],
    [7,6,4,5,1,0,2,3],
    [3,2,0,1,5,4,6,7]
]

array2 = [
    [0,1,2,3,5,4,7,6],
    [4,5,6,7,1,0,3,2],
    [6,7,4,5,3,2,1,0],
    [2,3,0,1,7,6,5,4],
    [3,2,1,0,6,7,4,5],
    [7,6,5,4,2,3,0,1],
    [5,4,7,6,0,1,2,3],
    [1,0,3,2,4,5,6,7]
]

array3 = [
    [0,1,2,3,4,5,6,7],
    [4,5,6,7,0,1,2,3],
    [2,3,0,1,6,7,4,5],
    [6,7,4,5,2,3,0,1],
    [1,0,3,2,5,4,7,6],
    [5,4,7,6,1,0,3,2],
    [3,2,1,0,7,6,5,4],
    [7,6,5,4,3,2,1,0]
]

Originals = [array1,array2,array3]

Normalized = [Normalize(array1),Normalize(array2),Normalize(array3)]

print( AreMutuallyOrthogonal( Originals ) )

print('')

for i in Normalized:
    for j in i:
        print(j)
    print('')

print( AreMutuallyOrthogonal( Normalized ) )