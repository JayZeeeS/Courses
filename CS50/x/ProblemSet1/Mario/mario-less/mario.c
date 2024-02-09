#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
//Welcomes the user and gets the desired height of the triangle.
    do
    {
        printf("This is your automated right angle triangle builder.\n\n");
        height = get_int("How high would you like your triangle to be? (max 8): ");
    }
    while (height <= 0 || height >= 101);

//Iterates over Columns(i) and Rows(j) while justifying to the right:
//Columns:
    for (int i = 1; i <= height; i++)
    {
//Justificator:
        int n = (height - (height - i));
        while (n <= height - 1)
        {
            n++;
            printf(" ");
        }
//Rows:
        for (int j = 1; j <= (i); j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
