#include <stdio.h>
#include <string.h>

int isPalindrome(char str[]) {
    int left = 0;
    int right = strlen(str) - 1;
    int isPalindrom = 1;
    while (left < right) {
        if (str[left] != str[right]) {
            isPalindrom = 0; // not palindrom
        }

        left++;
        right--;
    }

    return 1; // palindrom 
}

int main() {
    char str[1005];

    printf("Please input a string: (string.length <= 1000): \n\n");
    gets(str);
    int len; 
    int i; 
    len = strlen(str);

    int left = 0; 
    int right = len - 1; 
    int flag = 1; 

    while (left < right)
    {
        if (str[left] != str[right]) 
        {
            flag = 0; 
        }
        left = left + 1; 
        right = right - 1; 
    }
    if (flag == 1) { 
        printf("\n\n ok palindrom!\n\n"); 
    }
    else{
        printf("\n\n no NOT palindrom! \n\n"); 
    }

    return 0;
}
