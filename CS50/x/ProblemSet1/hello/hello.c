#include <stdio.h>
#include <cs50.h>

//Prints "hello, " and the name the user inputs:
int main(void)
{
    //gets the user's name
    string first_name = get_string("What is your name? ");
    //prints the user's name
    printf("hello, %s\n", first_name);
}