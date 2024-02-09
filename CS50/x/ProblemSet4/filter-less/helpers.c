#include "helpers.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i <= height; i++)
    {
        for (int j = 0; j <= width; j++)
        {
            BYTE new_value = round((image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen) / 3.0);
            image[i][j].rgbtRed = new_value;
            image[i][j].rgbtBlue = new_value;
            image[i][j].rgbtGreen = new_value;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i <= height - 1; i++)
    {
        for (int j = 0; j <= width - 1; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            if (sepiaRed >= 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen >= 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue >= 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i <= height; i++)
    {
        for (int j = 0; (j <= round((width / 2) - 1) && (width % 2 == 1)) || (j <= round((width / 2) - 1) && (width % 2 == 0)); j++)
        {
            RGBTRIPLE temp;
            temp = image[i][j];
            image[i][j] = image[i][(width - 1) - (j)];
            image[i][(width - 1) - (j)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //Make copy of original, for modification purposes:
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];

        }
    }
    //Blur algorithm:
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Get the sum of the 3 x 3 area around the current pixel:
            float count = 0;
            int sum_red = 0;
            int sum_green = 0;
            int sum_blue = 0;
            for (int k = (i - 1); k <= (i + 1); k++)
            {
                if (k >= 0 && k < height)
                {
                    for (int l = (j - 1); l <= (j + 1); l++)
                    {
                        if (l >= 0 && l < width)
                        {
                            sum_red += copy[k][l].rgbtRed;
                            sum_green += copy[k][l].rgbtGreen;
                            sum_blue += copy[k][l].rgbtBlue;
                            count++;
                        }
                    }
                }
            }
            int av_red = round(sum_red / count);
            if (av_red > 255)
            {
                av_red = 255;
            }
            image[i][j].rgbtRed = av_red;
            int av_green = round(sum_green / count);
            if (av_green > 255)
            {
                av_green = 255;
            }
            image[i][j].rgbtGreen = av_green;
            int av_blue = round(sum_blue / count);
            if (av_blue > 255)
            {
                av_blue = 255;
            }
            image[i][j].rgbtBlue = av_blue;
        }
    }
    return;
}
