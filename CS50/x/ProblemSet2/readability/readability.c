#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int letter_counter(string text_to_be_counted);
int word_counter(string text_to_be_counted);
int sentence_counter(string text_to_be_counted);
float average_per_100_words(int count, int words);
int round_of_grade_level(float average_letters, float average_sentences);
void grade_determinator(int index);

int main(void)
{
    string text = get_string("What text would you like to evaluate? ");
    int letter_count = letter_counter(text);
    int word_count = word_counter(text);
    int sentence_count = sentence_counter(text);
    float average_letters = average_per_100_words(letter_count, word_count);
    float average_sentences = average_per_100_words(sentence_count, word_count);
    int grade_index = round_of_grade_level(average_letters, average_sentences);
    grade_determinator(grade_index);
    return 0;
}
/*
What I will need:
A function that gets text input from the user.
    we will use `get_string` and set the output to a variable called "text".
*/

/*
A function that "reads" that text and count how many letters, words, and sentences there are in the user's input.
    We initiate the "letters", "words" and "sentences" variables.
    Using a for loop that iterates on a number while it is lower than the number of chars in the "text" string, treated as an array, we will do the following:
        Get the char from "text" and if it is a letter we add 1 to a "letters" variable
        If it is a " "(Space) we add 1 to the "words" variable
        If it is a punctuation mark like "." "!" or "?" we add 1 to the "sentences" variable
*/
int letter_counter(string text_to_be_counted)
{
    int letters = 0;
    int i;
    int length = strlen(text_to_be_counted);
    for (i = 0; i <= length;  i++)
    {
        if (((text_to_be_counted[i] >= 65) && (text_to_be_counted[i] <= 90)) || ((text_to_be_counted[i] >= 97)
                && (text_to_be_counted[i] <= 122)))
        {
            letters++;
        }

    }
    return letters;
}
int word_counter(string text_to_be_counted)
{
    int words = 0;
    int i;
    int length = strlen(text_to_be_counted);
    for (i = 0; i <= length; i++)
    {
        if (text_to_be_counted[i] == 32)
        {
            words++;
        }
    }
    words++;
    return words;
}

int sentence_counter(string text_to_be_counted)
{
    int sentences = 0;
    int i;
    int length = strlen(text_to_be_counted);
    for (i = 0; i <= length; i++)
    {
        if (text_to_be_counted[i] == 33 || text_to_be_counted[i] == 46 || text_to_be_counted[i] == 63)
        {
            sentences++;
        }
    }
    return sentences;
}

/*
A function that averages the variables for "letters" "words" and "sentences".
    We initiate variables called "average_letters" "average_sentences"
    We caclualte the average of letters per 100 words with the following formula:
        "letters" / "words" * 100 and store the resulting value in the "average letters" variable
    We calculate the average of sentences per 100 words with the following formula:
        "sentences" / "words" * 100 and store it in the "average_sentences" variable.
*/
float average_per_100_words(int count, int words)
{
    float average = ((float)count / (float)words * 100.0);
    return average;
}
/*
A function that uses the values returned from the third function and calculates the grade level index.
    We initialize the variable "index"
    We calculate the index and assign it to the variable:
        0.0588 * "average_letters" - 0.296 * "average_sentences" - 15.8
*/
int round_of_grade_level(float average_letters, float average_sentences)
{
    int index = (int)round(0.0588 * average_letters - 0.296 * average_sentences - 15.8);
    return index;
}
/*
A function that determines what grade level to output, where less than 1 should be "Lower than Grade 1" and more than 16 should be "Grade 16+".
        We determine if the index value is not < 1 and > than 16, if it is not then:
            We print the index value rounded out to the nearest int
        If it is a value that is < 1 then:
            We print "Before Grade 1"
        If it is a value that is > 16 then:
            We print "Grade 16+"
*/
void grade_determinator(int index)
{
    if ((index >= 1) && (index <= 16))
    {
        printf("Grade %i\n", index);
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Before Grade 1\n");
    }
    return;
}