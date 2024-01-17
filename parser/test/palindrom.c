#include <stdio.h>
#include <string.h>

int isPalindrome(char str[]) {
    int a = 1;
    int b = 5;
    a++;
    b--;
    ++a;
    --b;
    int c = b++;
    int d = ++a;
    //4, 4, 3, 4
    printf("%d, %d, %d, %d\n", a, b, c, d);
    // int left = 0;
    // int right = strlen(str) - 1;

    // while (left < right) {
    //     if (str[left] != str[right]) {
    //         return 0; // not palindrom 
    //     }

    //     left++;
    //     right--;
    // }

    return 1; // palindrom 
}

int main() {
    
    char str[1000];
    isPalindrome(str);
    // printf("Please input a string: (string.length <= 1000)");
    // gets(str);
    // int len; 
    // int i; 
    // len = strlen(str);

    // // replace the last \n to \0 
    // if (str[strlen(str) - 1] == '\n') {
    //     str[strlen(str) - 1] = '\0';
    // }

    // int IsPLD = -1;
	// for (i = 0; i + i < len && IsPLD != 1; i = i + 1) 
	// {
	// 	if (str[len - 1 - i] != str[i]) 
	// 	{
    //         printf("NOT palindrom! \n");
    //         IsPLD = 1;
    //     }
	// }
    // if (IsPLD != 1) {
    //     printf("palindrom! \n");
    // }
    return 0;
}
