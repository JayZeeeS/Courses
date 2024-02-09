#include <stdio.h>
#include<cs50.h>


bool valid_triangle(int side1, int side2, int side3);

int get_side(int length);

int main (void)
{
    int a = 0, b = 0, c = 0;
    a = get_side(a);
    b = get_side(b);
    c = get_side(c);
    if(valid_triangle(a, b, c) == true)
    {
        printf("Your triangle is possible\n");
    }
    else
    {
        printf("Try again\n");
    }
    return 0;
}

int get_side(int length)
{
    length = get_int("How long is this side:  ");
    return length;
}

bool valid_triangle(int side1, int side2, int side3)
{
    if(((side1 >= 0) && (side2 >= 0) && (side3 >= 00)) && (((side1 + side2) > side3) && ((side1 + side3) > side2) && ((side2 + side3) > side1)))
    {
        return true;
    }
    else
    {
        return false;
    }
}

