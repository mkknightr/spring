// test eval_expr : a + b, a - b, a * b, a / b 
#include <stdio.h>
#include <stdlib.h>



int main() 
{ 
    int a = 10; 
    int b = 9; 
    int c = 0 - 1; 
    // a = b * c; 
   //  c = b * b; 
   //  b = 8 / b; 
    a = a - c; 

    return 0; 
}