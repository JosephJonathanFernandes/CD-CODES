#include <stdio.h>
#include <stdlib.h>

int main() {
    int a, b, sum;
    
    printf("Enter two numbers: ");
    scanf("%d %d", &a, &b);
    
    sum = a + b;
    
    if (sum > 100) {
        printf("Large sum: %d\n", sum);
    } else {
        printf("Sum: %d\n", sum);
    }
    
    for (int i = 0; i < 5; i++) {
        printf("Loop iteration: %d\n", i);
    }
    
    return 0;
}