#include <stdio.h>
#include <cs50.h>

// protótipo da função
void print_row(int spaces, int bricks);

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1);

    for (int i = 0; i < n; i++)
    {
        int spaces = n - i - 1;
        int bricks = i + 1;
        print_row(spaces, bricks);
    }
}

// implementação da função (sem ponto e vírgula depois!)

void print_row(int spaces, int bricks)

{
    for (int i = 0; i < spaces; i++)
    {
        printf(" ");
    }
    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }

    printf("\n");
}
