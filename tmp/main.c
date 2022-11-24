#include <stdio.h>
#include <stdlib.h>
#include <string.h>

union YYSTYPE
{
    char char_val;
    int int_val;
    float float_val;
    double double_val;
    char *str_val;
} yylval; // global variable for lexical analysis

int lex(FILE *file);
int parse(FILE *file);

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        printf("Input invalid!\n");
        return 0;
    }

    const char *filename = argv[2];
    FILE *fp = fopen(filename, "r");
    if (fp == NULL)
    {
        printf("Failed to open file: %s\n", filename);
        return 0;
    }

    if (!strcmp(argv[1], "lexer"))
    {
        while (lex(fp) != 0)
            ;
    }
    else if (!strcmp(argv[1], "parser"))
    {
        while (parse(fp) != 0)
            ;
    }

    // char *line = NULL;
    // size_t len = 0;
    // ssize_t read = 0;

    // while ((read = getline(&line, &len, fp)) != -1)
    // {
    //     printf("[%lu] \t", read);
    //     printf("%s", line);
    //     printf("tokens: ");

    //     int index = 0;
    //     while (index != read)
    //     {
    //         printf("%c", line[index]);
    //         index++;
    //     }

    //     printf("\n");
    // }

    fclose(fp);
    // if (line)
    // {
    //     free(line);
    // }

    return 0;
}
