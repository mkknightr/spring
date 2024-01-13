#include <stdio.h>
#include <string.h>

int isPalindrome(char str[]) {
    int left = 0;
    int right = strlen(str) - 1;

    while (left < right) {
        if (str[left] != str[right]) {
            return 0; // not palindrom 
        }

        left++;
        right--;
    }

    return 1; // palindrom 
}

int main() {
    char str[100];

    printf("Please input a string: ");
    fgets(str, sizeof(str), stdin);

    // replace the last \n to \0 
    if (str[strlen(str) - 1] == '\n') {
        str[strlen(str) - 1] = '\0';
    }

    if (isPalindrome(str)) {
        printf("palindrom!\n");
    } else {
        printf("NOT palindrom!\n");
    }

    return 0;
}
