#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int string_index(int character);
int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    // TODO: Compute and return score for string
    int word_value = 0;
    int i;
    int n = 0;
    int length = strlen(word);
    for (i = 0; i <= length; i++)//Iterate on every char of the string:
    {
        //Set n to the int value of the char we are iterating over at the moment,
        n = word[i];
        //check value of n in POINTS array,
        n = string_index(n);
        //Add said value to the word value,
        word_value += POINTS[n];
    }
    return word_value;
}

//Checks for the index number of the character in question:
int string_index(int character)
{

    int i;
    for (i = 0; i <= 0; i++)
    {
        if (character > 64 && character < 91)
        {
            character -= 65;
        }
        else if (character > 96 && character < 123)
        {
            character -= 97;
        }
    }
    return character;
}


