#include <stdio.h>

char getChar()
{
    return "a";
}

int main()
{
    // This is a comment
    // Data types
    int count = 0;
    float floatType;
    char charType = "a";

    // Print and scan
    printf("This is a Text");
    scanf("%d", &floatType);

    // If else
    if (1 <= 1)
    {
        printf("This should be printed");
    }
    else
    {
        printf("This should never be printed");
    }

    // While
    while (count < 5)
    {
        printf("Count: %d\n", count);
        count = 5;
    }

    // Operators
    // Arithmetic
    int sum = 1 + 2;
    int subtraction = 3 - 1;
    int multiply = 2 * 2;
    int divide = 4 / 2;

    // Logic
    // AND
    if (1 < 2 && 3 > 2)
    {
        printf("AND Test");
    }

    // OR
    if (1 < 2 || 3 > 2)
    {
        printf("OR Test");
    }

    // NOT
    if (1 != 2)
    {
        printf("NOT Test");
    }
    return 0;
}