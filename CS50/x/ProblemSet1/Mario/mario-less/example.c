#include <stdio.h>
#include <cs50.h>

int main (void)
{
    //we declare the variable:
    int h;
    //the "do while" loop starts by saying do:
    do
    //we open curly braces to indicate what should wedo in our "do while loop"
    {
        //we say what we wanna do:
        h = get_int ("How high?: ");
    }
    //A while argument works in the following manner:
    //It checks whether the condition(s) are fulfilled, aka true or false (boolean)
    //if it/they is/are, then it executes the code.
    //We indicate what the conditions are for the do portion:
    while (h <= 0 || h >= 9);
}