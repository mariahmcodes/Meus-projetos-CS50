#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // 1️⃣ Checar argumento
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // 2️⃣ Abrir arquivo de cartão
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("File not found.\n");
        return 1;
    }

    // 3️⃣ Buffer de 512 bytes e variáveis auxiliares
    uint8_t buffer[512];
    char filename[8];
    FILE *img = NULL;           // ponteiro para JPEG atual
    int jpeg_count = 0;         // contador de JPEGs encontrados

    // 4️⃣ Loop principal lendo 512 bytes
    while (fread(buffer, 1, 512, card) == 512)
    {
        // 5️⃣ Checar se bloco é início de JPEG
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // Se um JPEG já está aberto, fechar
            if (img != NULL)
                fclose(img);

            // Gerar nome do novo JPEG e abrir arquivo
            sprintf(filename, "%03i.jpg", jpeg_count);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                printf("Could not create output file.\n");
                fclose(card);
                return 1;
            }

            jpeg_count++;
        }

        // 6️⃣ Se JPEG está aberto, escrever o bloco
        if (img != NULL)
            fwrite(buffer, 512, 1, img);
    }

    // 7️⃣ Fechar arquivos abertos no final
    if (img != NULL)
        fclose(img);
    fclose(card);

    return 0;
}

