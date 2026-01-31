#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>

// Máximo tamanho de uma palavra
#define LENGTH 45

// Funções que você deve implementar
bool check(const char *word);
bool load(const char *dictionary);
unsigned int hash(const char *word);
unsigned int size(void);
bool unload(void);

#endif
