/*** test #5
 * test:  
 *  printf, 
 *  swap function, 
 *  variable declartion, 
 *  variable initialization, 
 *  evaluate expression, 
 * */

#include <stdio.h>
#include <stdlib.h>


void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
    return; 
}



int main() 
{ 
    int a = 1; 
    int b = 2; 
    printf("a : %d, b : %d \n", a, b); 
    swap(&a, &b); 
    printf("a : %d, b : %d \n", a, b); 
    
    return 0; 
}