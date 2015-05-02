// Author: Dr. Jeff McGough
// Accessed: 29 April 2015
// Modifications:
// 	f, k values to create different Gray-Scott patterns

#include <stdio.h>
#include <stdlib.h>
#include <time.h>


#define N 200
#define N1 201
#define Nh 100

int main()
{
    int i,j, count =0;
    double  f, k, e, dx, dxx, dt, d1, d2;
    double  diff1, diff2, nl;
    double  u[N1][N1], ub[N1][N1], v[N1][N1], vb[N1][N1];
    FILE *fp1, *fp2;
    
    f = 0.02;
    k = 0.05;
 
    e = 0.00001;
    dx = 2.5/(N-1);
    dxx = dx*dx;
    dt = 1.0;
    d1 = 2.0*e/dxx;
    d2 = e/dxx;
    count = 0;
    
    srand((unsigned) time(NULL));
    
    for(i=0; i< N1; i++)
    {
        for(j=0;j<N1;j++)
        {
            u[i][j] = 1.0 - 0.01*rand()/(RAND_MAX);
            v[i][j] = 0.0 + 0.05*rand()/(RAND_MAX);
            ub[i][j] = 1.0;
            vb[i][j] = 0.0;
        }
    }
    
    for(i=Nh-10; i< Nh+10; i++)
    {
        for(j=Nh-10;j<Nh+10;j++)
        {
            u[i][j] = 0.5;
            v[i][j] = 0.25;
        }
    }
    
    while (count < 10000)
    {
        count = count +1;
        
        for(i=1; i< N; i++)
        {
            for(j=1;j<N;j++)
            {
                
                diff1 = u[i-1][j]+u[i+1][j] + u[i][j-1] + u[i][j+1] -4.0*u[i][j];
                diff2 = v[i-1][j]+v[i+1][j] + v[i][j-1] + v[i][j+1] -4.0*v[i][j];
                nl = u[i][j]*v[i][j]*v[i][j];
                ub[i][j] = u[i][j] + dt*(d1*diff1 + f*(1.0 - u[i][j]) - nl);
                vb[i][j] = v[i][j] + dt*(d2*diff2 - (f+k)*v[i][j] + nl);
 
            }
        }
        for(i=1; i< N; i++)
        {
            for(j=1;j<N;j++)
            {
                u[i][j] = ub[i][j];
                v[i][j] = vb[i][j];
            }
        }
        for(i=1 ; i<N; i++){
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
    
    fp1 = fopen("gsuData.txt","w");
    fp2 = fopen("gsvData.txt","w");
    
    for(i=1; i< N; i++)
    {
        for(j=1;j<N;j++)
        {
            fprintf(fp1, "%lf  ",u[i][j]);
            fprintf(fp2, "%lf  ",v[i][j]);

        }
        fprintf(fp1,"\n");
        fprintf(fp2,"\n");
    }
    fclose(fp1);
    fclose(fp2);
    puts("To plot Datafile using Gnuplot:");
    puts("set contour");
    puts("unset surface");
    puts("unset ztics");
    puts("unset zlabel");
    puts("set view map");
    puts("splot \"gsuData.txt\" matrix with lines\n");

    
    return 0;
    
}

