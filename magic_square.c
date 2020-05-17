#include <stdio.h>
#include <stdlib.h> 

// Prints square
void print_square(int **arr, int square_size) {
    for (int i = 0; i <  square_size; i++) {
        for (int j = 0; j < square_size; j++) 
            printf("[%d] ", arr[i][j]); 
        printf("\n");
    } 
    printf("\n");
}

// Gets row index and fixes it if its going out of range
void fix_row_index(int *index, int square_size) {
    if (*index < 0)
            *index = square_size - 1;
}

// Gets column index and fixes it if its going out of range
void fix_column_index(int *index, int square_size) {
    if (*index >= square_size)
            *index = 0;
}

// Fill array according to magic square algorithm
void fill_square(int **arr, int square_size) {
    int row, column;
    row = 0;
    column = square_size / 2;
    for (int i = 1; i <= square_size * square_size; i++)
    {
        fix_row_index(&row, square_size);
        fix_column_index(&column, square_size);
        while (arr[row][column] != 0) {
            row--;
            fix_row_index(&row, square_size);
        }

        arr[row][column] = i;
        row--;
        column++;

    }
}

// Free square memory 
void free_square(int **arr, int square_size) {
    for (int i = 0; i < square_size; i++)
        free(arr[i]);
}

// Creates a square of size square_size X square_size and returns it.
int ** create_square(int square_size) {
    int ** arr = (int **)malloc(square_size * sizeof(int *));
    for (int i = 0; i < square_size; i++) 
         arr[i] = (int *)calloc(square_size, sizeof(int)); 
    return arr;
}

int main() {
    int square_size;
    int **arr;

    printf("Enter square size: ");
    scanf("%d", &square_size);

    arr = create_square(square_size);

    fill_square(arr, square_size);
    print_square(arr, square_size);
    free_square(arr, square_size);
}


