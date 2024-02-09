// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 17576;

// Hash table
node *table[N];

//Word Count
int word_count;

void freeLL(node *start);

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    //Hash word to obtain value
    unsigned int index = hash(word);
    //Access linked list
    node *cursor = table[index];
    //Traverse linked list
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }


    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int h = 1;
    //Looping through the first 3 letters of the word
    for (int i = 0; i < 3 || i < strlen(word); i++)
    {
        if (islower(word[i]) || isupper(word[i]))
        {
            //Normalizing the input
            char temp = word[i];
            temp = toupper(temp);
            h *= temp - 'A';
        }
    }

    return (h % N);
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    char buffer[LENGTH + 1] = " ";
    //Open the Dictionary file
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }
    //Read strings from file, one at a time
    while ((fscanf(dict, "%s", buffer)) != EOF)
    {
        //Create new node for each word
        node *new_word = malloc(sizeof(node));

        strcpy(new_word ->word, buffer);

        //Hash word to obtain hash value
        int index = hash(buffer);

        //Insert new node into hash value location
        if (table[index] == NULL)
        {
            new_word->next = NULL;
            table[index] = new_word;
        }
        else
        {
            new_word->next = table[index];
            table[index] = new_word;
        }
        word_count++;
    }
    fclose(dict);
    return true;
}


// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    word_count += 0;
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            freeLL(table[i]);
        }
    }
    return true;
}

void freeLL(node *start)
{
    if (start != NULL)
    {
        if (start->next != NULL)
        {
            freeLL(start->next);
        }
        free(start);
    }
}