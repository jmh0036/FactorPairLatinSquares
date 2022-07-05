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
    # if arrayOfarrays == []:
    #     return True
    for i in range(len(arrayOfarrays)-1):
        for j in range(i+1,len(arrayOfarrays))
        if IsOrthogonal(i,j) == False:
            return False
    return True


MutOrthSet = [
    [
        [1, 2, 4, 3, 6, 7, 5, 4],
        [4, 5, 7, 6, 2, 3, 1, 0]
    ]
]


print(AreMutuallyOrthogonal(MutOrthSet))