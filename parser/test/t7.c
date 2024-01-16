/*** test #7
 * test:  
 *  printf, 
 *  array variable declartion, 
 *  variable initialization, 
 *  evaluate expression, 
 *  array element print function
 * */

#include <stdio.h>
#include <stdlib.h>



void printArray(int* arr, int i) {
    printf("%d \n ", arr[i]);
    return;
}

int main() 
{ 
    int a[10];
    a[0] = 1;
    a[1] = 0; 
    a[2] = 3; 
    a[3] = 4;
    a[5] = 5; 
    a[6] = 7; 
    a[8] = 0; 
    printf("I am going to print some elements of array a "); 
    printArray(a, 0); 
    printArray(a, 1); 
    printArray(a, 2); 
    printArray(a, 3); 
    printArray(a, 5); 
    printArray(a, 6); 
    printArray(a, 8); 
    
    return 0; 
}