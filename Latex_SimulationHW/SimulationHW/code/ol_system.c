#include <stdio.h>
#include <stdlib.h>
#include <string.h>



double  get_angle();
double  get_distance();

int     get_iterations();
int     define_symbols( char **symbols );

void    get_axiom( char **word );
void    define_productions( char *symbols, char ***productions, int n_symbols );
void    calculate_iteration( char *word, char *symbols, char **productions, int t_max, int n_symbols );

int     symbol( char *symbols, char *tmp);
void    create_iteration( char *old_iteration, char *new_iteration, char *symbols, char **productions );

void    write_iterations( char **all_iterations, int t_max );

int main( int argc, char **argv)
{
    int t_max;
    
    char *word;
    char *symbols; 
    char **productions;
    int i, j;
    int n_symbols;
    int plants;
    printf( "How many plant like structures to calculate? : ");
    scanf( "%d", &plants );

    for( j = 0; j < plants; j++ )
    {
        printf( "Tree %d info:\n\n", j+1 );
        t_max = get_iterations();
        n_symbols = define_symbols( &symbols );
        define_productions( symbols, &productions, n_symbols );
        get_axiom( &word );
        calculate_iteration( word, symbols, productions, t_max, n_symbols );


       // free(word);
       
        free(symbols);

        for( i = 0; i < n_symbols; i++ )
            free(productions[i]);
        free(productions);
    }
}

double get_angle()
{
    double tmp;
    printf( "Enter an angle delta that +/- symbols will turn: ");
    scanf( "%lf", &tmp );
    return tmp;
}

double get_distance()
{
    double tmp;
    printf( "Enter a distance the turtle will move with F/f/G/g symbols: ");
    scanf( "%lf", &tmp );
    return tmp;
}

int get_iterations()
{
    int tmp;
    printf( "Enter the maximun number of iterations that will be calculated: ");
    scanf( "%d", &tmp );
    return tmp;
}

int define_symbols( char **symbols )
{
    char buffer[256];
    int i;
    printf( "Enter symbols that will be used (example: FGfg+-[] ): " );
    scanf( "%s", buffer );
    i = strlen(buffer);
    *symbols = (char*) malloc( sizeof(char) * i );
    strcpy( *symbols, buffer );
    return strlen(*symbols);
}

void define_productions( char * symbols, char ***productions, int n_symbols )
{
    char buffer[256];
    int i;
    int j;
    *productions = malloc( sizeof( char* ) * n_symbols );
    int x = strlen(symbols);
    for( i = 0; i < x; i++ )
    {
        printf( "Enter the production rule for %c: ", symbols[i] );
        scanf("%s", buffer );
        j = strlen( buffer );
        (*productions)[i] = ( char* ) malloc( sizeof( char ) * j);
        strcpy( (*productions)[i], buffer );
    }
}

void get_axiom( char **word )
{
    char buffer[256];
    int i;
    printf( "Enter axiom that will be used: ");
    scanf("%s", buffer);
    i = strlen(buffer);
    *word = ( char* ) malloc( sizeof( char ) * i );
    strcpy( *word, buffer );
}

void calculate_iteration( char * word, char *symbols, char ** productions, int t_max, int n_symbols)
{
    char *cur_iteration = word;
    char *old_iteration = malloc( sizeof( char* ) * t_max);
    int  *production_sizes = ( int* ) malloc( sizeof(int) *n_symbols );
    char buffer[256];
    int i, j;
    int size;
    int len;
    old_iteration = word;
    for( j = 0; j < n_symbols; j++ )
        production_sizes[j] = strlen( productions[j] );

    FILE *fp;
    double distance = get_distance();
    double angle = get_angle();
    printf( "Enter file to export all iterations to: ");
    scanf( "%s", buffer );
    fp = fopen( buffer, "w" );
    if( !fp )
        return;
    
    fprintf( fp, "%f", distance );
    fputs(" ", fp);
    fprintf( fp, "%f", angle );
    fputs("\n",fp);
    fputs( word, fp);
    fputs("\n",fp);
    for( i = 1; i < t_max; i++)
    {
        size = 0;
        len = strlen( old_iteration );
        for( j = 0; j < len; j++)
            size += production_sizes[ symbol(symbols, &cur_iteration[j] ) ];
        printf("\n\n%d\n\n", (size+1) * sizeof(char));
        printf("BEFORE\n\n", old_iteration);
        cur_iteration = malloc( sizeof(char) * (size+1) );
        printf("AFTER\n\n", old_iteration);
        create_iteration( old_iteration, cur_iteration, symbols, productions );
        //cur iteration becomes old iteration
        free(old_iteration);
        old_iteration = cur_iteration;
        
        //store current iteration to file
        fputs( cur_iteration, fp);
        fputs("\n",fp);
    }
    free(production_sizes);
    free( old_iteration );
    
    fclose(fp);
}

int symbol( char *symbols, char *tmp )
{
    int i;
    for( i = 0; symbols[i] != *tmp; i++ );
    return i;
}

void create_iteration( char *old_iteration, char *new_iteration, char *symbols, char **productions )
{
    int j, k, t, len;
    len = strlen(old_iteration);
    k = 0;
    t = symbol( symbols, &old_iteration[k] );
    strcpy(new_iteration, productions[t]);
    for( k = 1; k < len; k++ )
    {
        t = symbol( symbols, &old_iteration[k]);
        strcat( new_iteration, productions[t] );
    }
}
