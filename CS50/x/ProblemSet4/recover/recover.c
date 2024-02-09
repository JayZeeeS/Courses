#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

void recover(FILE *file);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    else
    {
        FILE *image = fopen(argv[1], "r");
        if (image == NULL)
        {
            printf("File could not be opened");
            return 1;
        }
        recover(image);
        return 0;
    }
}


void recover(FILE *file)
{
    BYTE buffer[512];
    int jpeg_count = 0;
    char filename[8];
    FILE *recovered = NULL;
    while (fread(buffer, sizeof(BYTE), 512, file) == 512)
    {

        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpeg_count == 0)
            {
                sprintf(filename, "%03i.jpg", jpeg_count);
                recovered = fopen(filename, "w");
                fwrite(buffer, sizeof(BYTE), 512, recovered);
                jpeg_count++;
            }
            else if (jpeg_count > 0)
            {
                fclose(recovered);
                sprintf(filename, "%03i.jpg", jpeg_count);
                recovered = fopen(filename, "w");
                fwrite(buffer, sizeof(BYTE), 512, recovered);
                jpeg_count++;
            }

        }
        else if (jpeg_count > 0)
        {
            fwrite(buffer, sizeof(BYTE), 512, recovered);
        }
    }
    fclose(recovered);
    fclose(file);
}

