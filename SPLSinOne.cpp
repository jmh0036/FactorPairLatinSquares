// To run in linux: g++ SPLSinOne.cpp then run ./a.out
// To run in Windows: g++ -static-libgcc -static-libstdc++ SPLSinOne.cpp then run a.exe



//The following code is based on the paper "Dancing Links" by D. E. Knuth.
//See http://www-cs-faculty.stanford.edu/~uno/papers/dancing-color.ps.gz
// #ifndef DLX_H
// #define DLX_H
#include <cstring>
#include <climits>
#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <math.h>
#include <cstdlib>
#include <stdlib.h>
// #include "dlx.h"
using namespace std;
struct data_object //A module in the sparse matrix data structure.
{
    data_object* L;                //Link to next object left.
    data_object* R;                //         "          right.
    data_object* U;                //         "          up.
    data_object* D;                //         "          down.
    data_object* C;                //Link to column header.
    int x;                         //In a column header: number of ones 
                                       //in the column. Otherwise: row index.
    void cover()                   //Covers a column.
    {
        data_object* i=D;
        data_object* j;
        R->L=L;
        L->R=R;
        while (i!=this)
        {
            j=i->R;
            while (j!=i)
            {
                j->D->U=j->U;
                j->U->D=j->D;
                j->C->x--;
                j=j->R;
            }
            i=i->D;
        }
    }
    void uncover()                 //Uncovers a column.
    {
        data_object* i=U;
        data_object* j;
        while (i!=this)
        {
            j=i->L;
            while (j!=i)
            {
                j->C->x++;
                j->D->U=j;
                j->U->D=j;
                j=j->L;
            }
            i=i->U;
        }
        R->L=this;
        L->R=this;
    }
};
//Standard S-heuristic suggested in Knuth's paper: pick the column with the
//fewest ones. Takes the root of the sparse matrix structure as an argument; 
//returns a pointer to the column header with the fewest ones.
data_object* DLX_Knuth_S_heuristic(data_object* root)
{
    data_object* P=root->R;
    data_object* res;
    int best=INT_MAX/2;
    while (P!=root)
    {
        if (P->x<best)
        {
            best=P->x;
            res=P;
        }
        P=P->R;
    }
    return res;
}
template <typename Func1,typename Func2>
/*
Actual recursive function implementing Knuth's Dancing Links method.
h is the root of the sparse matrix structure. 
O is the stack that will contain a list of rows used.
*/
void DLX_search(data_object* h,int k,int* O,Func1 send_row,
        Func2 choose_column)
{
    int i;
    data_object *r,*c,*j;
    if (h->R==h) //done - solution found
    {
        //send rows used in solution back...
        for (i=0; i<k; i++)
            send_row(O[i]);
        //-1 signifies end of solution
        send_row(-1);
        return;
    }
    //otherwise
    c=choose_column(h); //choose a column to cover
    c->cover();         //cover it
    r=c->D;
    while (r!=c)
    {
        O[k]=r->x;
        j=r->R;
        while (j!=r)
        {
            j->C->cover();
            j=j->R;
        }
        DLX_search(h,k+1,O,send_row,choose_column);
        //set r <- O[k], and c<- C[r], this is unnecessary
        j=r->L;
        while (j!=r)
        {
            j->C->uncover();
            j=j->L;
        }
        r=r->D;
    }
    c->uncover();
}
template <typename random_access_iterator,typename Func1,typename Func2>
/*
Meta-implementation of Knuth's Dancing Links method for finding solutions to
the exact cover problem.

PARAMETERS:
int rows: Number of rows in the matrix.
int cols: Number of columns in the matrix.
random_access_iterator buf: A random access iterator to ints (either 0 or
1), the entries of the matrix, in row major order.
Func1 send_row: A function object with return type void which takes as a
parameter the index of a row in a solution to the problem. (e.g. store it in 
a buffer or print it out) -1 signifies the end of a solution.
Func2 choose_column: A deterministic function object taking as a parameter a
data_object* (the root) and returning a data_object* (the header of the
column to choose.)
*/
void DLX_dancing_links(int rows,int cols,random_access_iterator buf,
            Func1 send_row,Func2 choose_column)
{
    //step 1: construct the linked-list structure.
    //We can do this by iterating through the rows and columns. Time is
    //linear in the number of entries (optimal).
    //Space used is linear in the number of columns + the number of rows
    // + the number of ones.
    int i,j;
    data_object* root=new data_object; //root
    data_object* P=root;               //left-right walker
    data_object* Q;                    //top-down walker
    //array of pointers to column headers
    data_object** walkers=new data_object*[cols];
    //auxiliary stack for recursion
    int* st=new int[rows];
    for (i=0; i<cols; i++)
    {
        //create a column header and L/R links
        (P->R=new data_object)->L=P;
        //store a pointer to the column header
        walkers[i]=Q=P=P->R;
        P->x=0; //reset popcount
        for (j=0; j<rows; j++)
            if (buf[i+cols*j]) //a 1 in the current location?
            {
                //create a data object and U/D links
                (Q->D=new data_object)->U=Q;
                Q=Q->D;  //advance pointer
                Q->C=P;  //link to the column header
                P->x++;  //increment popcount for this column
                Q->x=j;  //note the row number of this entry
            }
        Q->D=P; //complete the column
        P->U=Q;
    }
    P->R=root; //complete the column list
    root->L=P;
    //eliminate empty columns
    P=root;
    for (i=0; i<cols; i++)
    {
        P=P->R;
        if (!P->x)
        {
            P->L->R=P->R;
            P->R->L=P->L;
        }
    }
    //now construct the L/R links for the data objects.
    P=new data_object;
    for (i=0; i<rows; i++)
    {
        Q=P;
        for (j=0; j<cols; j++)
            if (buf[j+cols*i]) //a one
            {
                //in _this_ row...
                walkers[j]=walkers[j]->D;
                //create L/R links
                (Q->R=walkers[j])->L=Q;
                //advance pointer
                Q=Q->R;
            }
        if (Q==P) continue;
        Q->R=P->R;       //link it to the first one in this row.
        P->R->L=Q;       //link the first one to the last one.
    }
    delete P;                //P is no longer needed
    delete walkers;          //walkers are no longer needed
    //step 2: recursive algorithm
    DLX_search(root,0,st,send_row,choose_column);
    delete st;
    P=root->R;
    while (P!=root)          //deallocate sparse matrix structure
    {
        Q=P->D;
        while (Q!=P)
        {
            Q=Q->D;
            delete Q->U;
        }
        P=P->R;
        delete P->L;
    }
    delete root;
}

//If no heuristic is specified, Knuth's S heuristic is used - select the
//column with the fewest ones to minimize the breadth of the search tree.
template <typename random_access_iterator,typename Func1>
void DLX_dancing_links(int rows,int cols,random_access_iterator buf,Func1 send_row)
{
    DLX_dancing_links(rows,cols,buf,send_row,DLX_Knuth_S_heuristic);
}

// #endif


// To compile:
// g++ -c DirtyDriver.cpp -g
// g++ DirtyDriver.cpp -o Dirty.o
// ./Dirty.o



#define block(r,c,i) (FParray[i][0]*((r)/FParray[i][0])+((c)/FParray[i][1]))

// Define the order of the FPLS(n)
#define N 6
#define a 2
#define b 3
const int intCount = 4; //Number of Factors (Factor Pairs)
const int Columns = N*N*(intCount+1); //N*N*(intCount+1)
const int Rows = N*N*N; //N*N*N

int matrix[Rows][Columns]; //DLX Matrix

int grid[N][N]; //End Product

// Number of Factor Pairs = Number of factors 
// int FactorCount(int n)
// {
//  int factorCount;
//  factorCount = 0;

//  for (int i = 1; i < n+1; i++)
//  {
//      if (n % i == 0)
//          factorCount++;
//  }

//  return factorCount;
// }

void f(int x)
{
    int i;
    int c;
    int r;
    if (x+1) 
    {
        i=x%N; x/=N;
        c=x%N; r=x/N;
        grid[r][c]=i+1;
    }
    else
    {
        ofstream myfile;
        myfile.open("3by8SPLS.txt");
        for (r=0; r<N; r++,putchar('\n'))
            for (c=0; c<N; c++)
                {
                    cout << grid[r][c];
                    std::string str = std::to_string(grid[r][c]);
                    myfile << str;
                    if (c != N-1)
                    {
                        cout << " & ";
                        myfile << " & ";}
                    if (c == N-1){
                        cout << " \\nl";
                        myfile << endl;}
                }
        printf("\n");
        myfile << endl;
        myfile.close();
        // cout << sizeof(myfile);
        // The below code stops after finding one.
        exit(0);
    }
}

void cover_col(int col)
{
    for (int row=0; row<(N*N)*N; row++)
        if (matrix[row][col])
        {
            matrix[row][col]=0;
            memset(matrix[row],0,sizeof(matrix[row]));
        }
}

void cover_row(int row)
{
    for (int col=0; col<(N*N)*(intCount+1); col++)
        if (matrix[row][col])
        {
            matrix[row][col]=0;
            cover_col(col);
        }
}
int main()
{
    // Calculates the factor Pairs.  
    int FParray[intCount][2];
    int whichPair;
    whichPair = 1;

    FParray[0][0] = 1;
    FParray[0][1] = N;
    FParray[1][0] = N;
    FParray[1][1] = 1;

    FParray[2][0] = a;
    FParray[2][1] = b;
    FParray[3][0] = b;
    FParray[3][1] = a;

    // for (int i = 2; i < (floor(sqrt(N))+1); i++)
    // {
    //  if (N % i == 0)
    //  {
    //      whichPair++;
    //      FParray[whichPair][0] = i;
    //      FParray[whichPair][1] = N/i;
    //      if (i != (N/i))
    //      {
    //          whichPair++;
    //          FParray[whichPair][0] = N/i;
    //          FParray[whichPair][1] = i;
    //      }
    //  }
    // }

    // Not sure why this doesn't work...
    // grid[2][0]=1;
    // grid[2][1]=2;
    // grid[2][2]=3;
    // grid[3][0]=4;
    // grid[3][1]=5;
    // grid[3][2]=6;

    for (int row=0,r=0; r<N; r++)
        for (int c=0; c<N; c++)
            for (int i=0; i<N; i++,row++)
            {
                //uniqueness constraint
                matrix[row][r+N*c]=1;
                //Factor Pair constraint (including Row & column)
                for (int pair = 0; pair < intCount; pair++)
                {
                    matrix[row][(pair+1)*(N*N)+i+N*(block(r,c,pair))] = 1;
                }
            }
    putchar('\n');
    DLX_dancing_links((N*N)*N,(N*N)*(intCount+1),(int*)&matrix,f);

    return 0;
}