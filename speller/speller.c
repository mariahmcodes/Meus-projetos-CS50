#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdbool.h>

#include "dictionary.h"

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Usage: ./speller dictionary.txt text.txt\n");
        return 1;
    }

    // Carrega o dicionário
    if (!load(argv[1]))
    {
        printf("Could not load dictionary.\n");
        return 1;
    }

    // Lê o arquivo de texto
    FILE *text = fopen(argv[2], "r");
    if (!text)
    {
        printf("Could not open text file.\n");
        unload();
        return 1;
    }

    char word[LENGTH + 1];
    while (fscanf(text, "%45s", word) != EOF)
    {
        if (!check(word))
            printf("%s\n", word);
    }

    fclose(text);
    unload();
    return 0;
}
