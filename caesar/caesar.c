#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main (int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n\n");
        return 1;
    }

    for (int i = 0; argv[1][i] != '\0'; i++)
    {
        if (!isdigit(argv[1][i])) // or ascii 0  < i > 9
        {
            printf("Usage: ./caesar key\n\n");
            return 1;
        }
    }

    int k = atoi(argv[1]);
    string text = get_string("plaintext:  ");
    int n = strlen(text);
    char ciphertext[n + 1];

    for (int i=0; i<n ; i++)
    {
        if (isupper(text[i]))
        {
            ciphertext[i] = ((text[i] - 'A' + k) % 26) + 'A';
        }

        else if (islower(text[i]))
        {
            ciphertext[i] = ((text[i] - 'a' + k) % 26) + 'a';
        }

        else
        {
            ciphertext[i] = text[i]; // leave non-letters unchanged
        }
    }
        ciphertext[n]= '\0';
        printf("ciphertext: %s\n", ciphertext);
        return 0;
}
