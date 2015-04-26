// Author: Stephanie Athow
// Date: 24 April 2015
// Professor: Dr. Jeff McGough
// Problem Statement:
//	Reproduce patterns theta, lambda, mu, alpha in the Gray-Scott Model (CA).
//	You don't have to follow the color scheme.

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 200
#define N1 201
#define Nh 100

int main()
{
	int i , j, t = 0, count = 0;			// iteration/location counters
	double f , k, e, dx, dxx, dt, d1, d2;	// calculated values
	double diff1, diff2;					// calculated values
	double u[N1][N1], ub[N1][N1], v[N1][N1], vb[N1][N1];	// grids for u, du, v, dv
	
	FILE *fp1, *fp2;		// output files
	
	f = 0.04;
	k = 0.06;
	e = 0.00001;
	dx = 2.5 / ( N-1 );
	dxx = dx * dx;
	dt = 1.0;
	d1 = 2.0 * e / dxx;
	d2 = e / dxx;
	count = 0;
	
	srand( (unsigned) time(NULL) );
	
	// randomly perturb mesh
	for( i = 0; i < N1; i++ )
	{
		for( j = 0; j < N1; j++ )
		{
			u[i][j] = 1.0 - 0.01 * rand() / (RAND_MAX);
			v[i][j] = 0.0 + 0.05 * rand() / (RAND_MAX);
			ub[i][j] = 1.0;
			vb[i][j] = 0.0;
		}
	}
	
	for( i = Nh-10; i < Nh + 10; i++ )
	{
		for( j = Nh-10; j < Nh+10; j++ )
		{
			u[i][j] = 0.5;
			v[i][j] = 0.25;
		}
	}
	
	// run through time iterations
	while( count < 10000 )
	{
		count = count + 1;
		for( i = 1; i < N; i++ )
		{
			for( j = 1; j < N; j++ )
			{
				// diff1 = change in u
				// diff2 = change in v
				diff1 = u[i-1][j] + u[i+1][j] + u[i][j-1] + u[i][j+1] - 4.0*u[i][j];
				diff2 = v[i-1][j] + v[i+1][j] + v[i][j-1] + v[i][j+1] - 4.0*v[i][j];
				
				// (partial) du/dt = d1*deltaU - u*v^2 + F*( 1-u )
				// (partial) dv/dt = d2*deltaV + u*v^2 - (F + k)*v
				ub[i][j] = u[i][j] + dt*(d1*diff1 + f*(1.0-u[i][j] - u[i][j]*v[i][j]*v[i][j];
				vb[i][j] = v[i][j] + dt*(d2*diff2 - (f+k)*v[i][j] + u[i][j]*v[i][j]*v[i][j];
			}
		}
		
		// update grid
		for( i = 1; i < N; i++ )
		{
			for( j = 1; j < N; j++ )
			{
				u[i][j] = ub[i][j];
				v[i][j] = vb[i][j];
			}
		}
		
		// boundary conditions - wrapping
		for( i = 1; i < N; i++ )
		{
			u[i][0] = ub[i][N-1];
			u[i][N] = ub[i][1];
			v[i][0] = vb[i][N-1];
			v[i][N] = vb[i][1];
			u[0][i] = ub[N-1][i];
			u[N][i] = ub[1][i];
			v[0][i] = vb[N-1][i];
			v[N][i] = vb[1][i];
		}
	}
	
	
	// save data into text file to display with another program or gnu plot
	fp1 = fopen( "gsuData.txt", "w" );
	fp2 = fopen( "gsvData.txt", "w" );
	
	for( i = 1; i < N; i++ )
	{
		for( j = 1; j < N; j++ )
		{
			fprintf( fp1, "%lf ", u[i][j] );
			fprintf( fp2, "%lf ", v[i][j] );
		}
		
		fprintf( fp1, "\n" );
		fprintf( fp2, "\n" );
	}
	
	fclose( fp1 );
	fclose( fp2 );
		
	return 0;
}



/*
Gnuplot commands:
set contour
unset surface
unset ztics
unset label
unset key
set view map
splot "gsuData.txt" matrix with lines
set ouput "gsuData.eps"
set term postscript eps
replot
*/