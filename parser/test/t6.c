/*** test #6
 * test:  
 *  printf, 
 *  array variable declartion, 
 *  variable initialization, 
 *  evaluate expression, 
 * */

#include <stdio.h>
#include <stdlib.h>


int main() 
{ 
    int a[10];
    a[0] = 1;
    a[1] = 0; 
    printf("a[0] : %d, a[1] : %d \n", a[0], a[1]); 
    
    return 0; 
}