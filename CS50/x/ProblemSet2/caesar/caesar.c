#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool key_check(string s);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    if (key_check(argv[argc - 1]) == false || argc != 2)
    {
        printf("Usage: ./caesar key \n");
        return 1;
    }
    else
    {
        string p = get_string("plaintext:  ");
        printf("ciphertext: ");
        for (int i = 0; i <= strlen(p) - 1; i++)
        {
            char c = rotate(p[i], atoi(argv[argc - 1]));
            printf("%c", c);
        }
        printf("\n");
    }
}

// Iterates over the command line argument to check if the key is a digit and returns a boolean value:
bool key_check(string s)
{
    for (int i = 0; i <= strlen(s) - 1; i++)
    {
        if (isdigit(s[i]) == false)
        {
            return false;
        }
    }
    return true;
}

//Shifts a char by the amount of letters of the key, wrapping around of the alphabet, while ignoring non-alphabetic chars:
char rotate(char c, int n)
{
    char chipher;
    if (isupper(c))
    {
        chipher = (((c - 65) + n) % 26) + 65;
    }
    else if (islower(c))
    {
        chipher = (((c - 97) + n) % 26) + 97;
    }
    else
    {
        chipher = c;
    }
    return chipher;
}