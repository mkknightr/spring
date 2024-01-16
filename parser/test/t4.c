/*** test #4
 * test:  
 *  printf, 
 *  variable comparison,
 *  variable declaration,   
 *  evaluate expression, 
 * */

#include <stdio.h>
#include <stdlib.h>

int main() 
{ 
    int a = 1; 
    int b = 2; 
    int c = 3; 
    int d; 
    d = a + b; 
    printf("1 > 2   :  %d\n", 1 > 2); 
    printf("1 < 2   :  %d\n", 1 < 2);
    printf("1 <= 2  :  %d\n", 1 <= 2);
    printf("1 >= 2  :  %d\n", 1 >= 2);
    printf("1 == 2  :  %d\n", 1 == 2); 
    printf("1 != 2  :  %d\n", 1 != 2); 

    
    return 0; 
}