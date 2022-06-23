#include <iostream>
#include <set>
// #include <iterator>

using namespace std;

#define SIZE 3

typedef pair<int, int> pairs;

bool IsOrthogonal(int GridOne[SIZE][SIZE], int GridTwo[SIZE][SIZE]) {
    set<pairs> s;

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            pairs x = make_pair(GridOne[i][j], GridTwo[i][j]);

            s.insert(x);
        }
    }
  
    int Cardinality = 0;
    for (auto const &x : s) {
        Cardinality++;
    }
    
    if (Cardinality == SIZE*SIZE) {
        return true;
    }
    else {
        return false;
    }
}

int main(){
    // Starting Puzzle
    int PuzzleOne[SIZE][SIZE] = {   
        {1, 2, 3},
        {2, 3, 1},
        {3, 1, 2}
    };

    int PuzzleTwo[SIZE][SIZE] = {
        {1, 2, 3},
        {3, 1, 2},
        {2, 3, 1}
    };



    // int EmptyPuzzle[SIZE][SIZE] = { {0} };

    cout << IsOrthogonal(PuzzleOne, PuzzleTwo) << endl;

    // cout << "There are " << NumberOfSolutions </< " solutions" << endl;

    // cin.get(); // Pauses the outputs at each solution
    return 0;
}