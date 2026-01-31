#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    string text = get_string("Text: ");

    int letters = 0;
    int words = 1;       // start at 1 because last word isn't followed by space
    int sentences = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char c = text[i];      // optional: store current char for readability

        if (isalpha(c))
            letters++;

        else if (c == ' ')
            words++;

        else if (c == '.' || c == '!' || c == '?')
            sentences++;
    }

    printf("Letters: %i\n", letters);
    printf("Words: %i\n", words);
    printf("Sentences: %i\n", sentences);
}
