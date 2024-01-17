/** test #10 
 *  scanf function  
 *  print int value 
 *   
*/
#include <stdio.h>

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
    return;
}

void bubbleSort(int arr[], int n) {

    for(int i = 0; i < n; i++){
        for(int j = 0; j < n-1; j++){
            if(arr[j] > arr[j+1]){
                swap(&arr[j], &arr[j+1]);
            }
        }
    }



    printf("\n\nArray after sorted  : ");
    for(int i = 0; i < n; i++){
        printf("%d ", arr[i]);
    }


    return;
}


int main() {
    int arr[1000]; 
    int n; 
    printf("Please input the length of the array : \n"); 
    scanf("%d", &n); 
    printf("array length is : %d", n); 
    printf("\n\ninput the array to be sorted (one number one line)\n"); 
    int i = 0; 
    while (i < n)
    {
        scanf("%d", &arr[i]); 
        i = i + 1; 
    }
    printf("\n\nArray before sorted  : ");
    i = 0; 
    while (i < n)
    {
        printf("%d ", arr[i]); 
        i = i + 1; 
    }

    // bubbleSort(arr, n);


    return 0;
}
