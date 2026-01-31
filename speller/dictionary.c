#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Estrutura de um node na hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Número de baldes na hash table (número primo grande)
const unsigned int N = 14311;

node *table[N];       // hash table
unsigned int word_count = 0; // contador de palavras carregadas

// Retorna true se a palavra estiver no dicionário
bool check(const char *word)
{
    int index = hash(word);
    node *cursor = table[index];

    while (cursor != NULL)
    {
        // Compara ignorando maiúsculas/minúsculas
        if (strcasecmp(cursor->word, word) == 0)
            return true;
        cursor = cursor->next;
    }

    return false;
}

// Função de hash simples
unsigned int hash(const char *word)
{
    unsigned long hash = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash = hash * 31 + tolower(word[i]);
    }
    return hash % N;
}

// Carrega dicionário na memória
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
        return false;

    char buffer[LENGTH + 1];
    while (fscanf(file, "%45s", buffer) != EOF)
    {
        node *new_node = malloc(sizeof(node));
        if (!new_node)
            return false;

        strcpy(new_node->word, buffer);

        unsigned int index = hash(buffer);
        new_node->next = table[index];
        table[index] = new_node;

        word_count++;
    }

    fclose(file);
    return true;
}

// Retorna número de palavras no dicionário
unsigned int size(void)
{
    return word_count;
}

// Libera memória alocada
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
