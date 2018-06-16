#include <iostream>
#include <unistd.h>
using namespace std;

int grid[20][40];

int generation()
{
	int myGrid[20][40];

	for(int k = 0; k < 20; k++) // copies the current grid
	{
		for(int l = 0; l < 40; l++)
		{
			*(*(myGrid + k) + l) = *(*(grid + k) + l);  // grid[k][l];
		}
	}

	for(int i = 0; i < 20; i++)
	{
		for(int j = 0; j < 40; j++)
		{
			int neighbors = 0;

			if(i+1 < 20 && *(*(myGrid + (i+1)) + j)  == 0 )  // counts the amount of neighbors
			{
				neighbors++;
			}	
			if(i-1 >= 0 && *(*(myGrid + (i-1)) + j) == 0)
			{
				neighbors++;
			}
			if(j+1 < 40 && *(*(myGrid + i) + (j+1)) == 0)
			{
				neighbors++;
			}
			if(j-1 >= 0 && *(*(myGrid + i) + (j-1)) == 0)
			{
				neighbors++;
			}
			if(i-1 >= 0 && j-1 >=0 && *(*(myGrid + (i-1)) + (j-1)) == 0)
			{
				neighbors++;
			}
			if(i-1 >= 0 && j+1 < 40 && *(*(myGrid + (i-1)) + (j+1)) == 0)
			{
				neighbors++;
			}
			if(i+1 < 20 && j-1 >= 0 && *(*(myGrid + (i+1)) + (j-1)) == 0)
			{
				neighbors++;
			}
			if(i+1 < 20 && j+1 < 40 && *(*(myGrid + (i+1)) + (j+1)) == 0)
			{
				neighbors++;
			}	

			if(*(*(myGrid + i) + j) == 0) // checks for undercrowding and overcrowding
			{
				if(neighbors == 0 || neighbors == 1 || neighbors > 3)
				{
					*(*(grid + i) + j) = 1;
				}
			}
	
			if(*(*(myGrid + i) + j)  == 1) // checks for birth
			{
				if(neighbors == 3)
				{
					*(*(grid + i) + j) = 0;
				}
			}
		}
	}	
	
	return 0;
}

void display()
{
	for(int i = 0; i < 20; i++)
	{	
		for(int j = 0; j < 40; j++)
		{
			cout << *(*(grid + i) + j) << " ";
		}
	cout << endl;
	}
	cout << endl;
}


int main()
{
	for(int i = 0; i < 20; i++) // sets up initial grid
	{
		for(int j = 0; j < 40; j++)
		{
			*(*(grid + i) + j) = 1;
			*(*(grid + 10) + 15) = 0;
			*(*(grid + 11) + 15) = 0;
			*(*(grid + 10) + 16) = 0;
			*(*(grid + 11) + 16) = 0;

			*(*(grid + 12) + 17) = 0;
			*(*(grid + 13) + 17) = 0;
			*(*(grid + 12) + 18) = 0;
			*(*(grid + 13) + 18) = 0;
			cout << *(*(grid + i) + j) << " ";
		}
	cout << endl;
	}
	cout << endl;	

	for(int i = 0; i < 3; i++)  
	{
		generation();
		display();
		usleep(800000);
		cout << endl;
	}
	return 0;
}	
