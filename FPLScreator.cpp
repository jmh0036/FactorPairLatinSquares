// To compile:
// g++ -c FPLScreator.cpp -g
// g++ FPLScreator.cpp -o FPLScreator.o
// ./FPLScreator.o

#include <iostream>
#include <stdio.h>
#include <math.h>
#include <cstdlib>
#include <stdlib.h>
#include "dlx.h"
using namespace std;

#define block(r,c,i) (FParray[i][0]*((r)/FParray[i][0])+((c)/FParray[i][1]))

// Define the order of the FPLS(n)
#define N 23
const int intCount = 2; //Number of Factors (Factor Pairs)
const int Columns = 1587; //N*N*(intCount+1)
const int Rows = 12167; //N*N*N

int matrix[Rows][Columns]; //DLX Matrix

int grid[N][N]; //End Product

// Number of Factor Pairs = Number of factors 
int FactorCount(int n)
{
	int factorCount;
	factorCount = 0;

	for (int i = 1; i < n+1; i++)
	{
		if (n % i == 0)
			factorCount++;
	}

	return factorCount;
}

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
		for (r=0; r<N; r++,putchar('\n'))
			for (c=0; c<N; c++)
				{
					cout << grid[r][c];
					if (c != N-1)
						cout << " & ";
					if (c == N-1)
						cout << " \\nl";
				}
		printf("\n");
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

	for (int i = 2; i < (floor(sqrt(N))+1); i++)
	{
		if (N % i == 0)
		{
			whichPair++;
			FParray[whichPair][0] = i;
			FParray[whichPair][1] = N/i;
			if (i != (N/i))
			{
				whichPair++;
				FParray[whichPair][0] = N/i;
				FParray[whichPair][1] = i;
			}
		}
	}
	
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