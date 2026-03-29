%{
#include <stdio.h>
#include <stdlib.h>

int token_count = 0;
%}

%%

[0-9]+          { token_count++; printf("NUMERO:%s\n", yytext); }
[0-9]+\.[0-9]+  { token_count++; printf("DECIMAL:%s\n", yytext); }
"print"         { token_count++; printf("PRINT:%s\n", yytext); }

[a-zA-Z_][a-zA-Z0-9_]*  { token_count++; printf("IDENTIFICADOR:%s\n", yytext); }
"="             { token_count++; printf("ASIGNACION:%s\n", yytext); }

"+"             { token_count++; printf("SUMA:%s\n", yytext); }
"-"             { token_count++; printf("RESTA:%s\n", yytext); }
"*"             { token_count++; printf("MULTIPLICACION:%s\n", yytext); }
"/"             { token_count++; printf("DIVISION:%s\n", yytext); }
"("             { token_count++; printf("PARENTESIS_IZQ:%s\n", yytext); }
")"             { token_count++; printf("PARENTESIS_DER:%s\n", yytext); }
[ \t\n]         { }
.               { printf("ERROR:Caracter no reconocido '%s'\n", yytext); }

%%

int yywrap() {
    return 1;
}

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            printf("ERROR: No se pudo abrir el archivo\n");
            return 1;
        }
        yyin = file;
    }
    
    yylex();
    printf("\n---TOTAL:%d\n", token_count);
    
    return 0;
}