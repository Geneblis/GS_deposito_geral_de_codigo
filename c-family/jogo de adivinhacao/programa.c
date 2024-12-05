#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    printf("**********************************************************\n");
    printf("**********************************************************\n");
    printf("             ,----------------,               ,---------, \n");
    printf("        ,-----------------------,           ,         , | \n");
    printf("      ,                       , |         ,         ,   | \n");
    printf("     +-----------------------+  |       ,         ,     | \n");
    printf("     |  .-----------------.  |  |      +---------+      | \n");
    printf("     |  |                 |  |  |      | -==----'|      | \n");
    printf("     |  | BEM-VINDO AO    |  |  |      |         |      | \n");
    printf("     |  |    JOGO DA      |  |  |//----|`---=    |      | \n");
    printf("     |  | ADIVINHAÇÃO!    |  |  |   ,//|==== ooo |      ; \n");
    printf("     |  |                 |  |  |  //  |(((( [33]|    ,   \n");
    printf("     |  `-----------------'  |,  .;'|  |((((     |  ,     \n");
    printf("     +-----------------------+  ;;  |  |         |,       \n");
    printf("        /_)______________(_//  //'   | +---------+        \n");
    printf("   ___________________________//___  `,                   \n");
    printf("  //  oooooooooooooooo  .o.  oooo //,   //,-----------    \n");
    printf(" // ==ooooooooooooooo==.o.  ooo= //   ,//--{)B     ,      \n");
    printf("//_==__==========__==_ooo__ooo=_//'   //___________,      \n");
    printf("**********************************************************\n");
    printf("**********************************************************\n\n");

    //Int = Inteiros, Double = Nao-inteiros
    //Numero randomico configurado pelo time.h
    int segundos = time(0);
    srand(segundos);
    int aleatorizador = rand();

    int secretnumb = aleatorizador % 100;
    int chute = 0;
    int tentativa = 1;
    int modo = 0;
    int acertou = 0;
    double pontos = 1000;

    printf("=================================\n");
    printf("Escolha seu modo de jogo:\n");
    printf("Pressione 1 para modo Dificil (5 tentativas):\n");
    printf("Pressione 2 para modo Casual (infinitas tentativas):\n");
    printf("=================================\n");
    printf("Escaneando...");
    scanf("%d", &modo);

    //Shouters, Greetings, sla cmo q chama isso.
if(modo == 1) {
    printf("=================================\n");
    printf("Modo de jogo Dificil inicializando... Bom jogo!\n");
    printf("=================================\n");
}
if(modo == 2) {
    printf("=================================\n");
    printf("Modo de jogo Casual inicializando... Bom jogo!\n");
    printf("=================================\n");
}
while(modo != 1 && modo !=2 ) {
    printf("Numero invalido! Escolha uma das opçoes!\n");
    scanf("%d", &modo);
}

    //Modo Casual
    while(modo == 2 && chute != secretnumb) {
        printf("Qual numero o programa gerou?\n");
        scanf("%d", &chute);
        printf("Seu chute foi: %d \n", chute);
        printf("Tentativa: %d\n", tentativa);
        if(chute < 0) {
            printf("\nNumeros negativos não são permitidos. Seu numero foi invalidado.\n");
           continue;
        } 

        int acertou = {chute == secretnumb};
        int chutemaior = {chute > secretnumb};
        int chutemenor = {chute < secretnumb};

        //printf("Seu chute foi: %d Porem o numero secreto eh: %d", chute, secretnumb);

        if(acertou) {
            printf("\n\nVocê Acertou!\nJogue novamente reniciando o programa.\n");
            printf("\nNumeros de tentativas: %d\n", tentativa-1);
            printf("Total de pontos %.1f\n", pontos);
            return 0;
        } 
        else {
            if(chutemaior) {
                printf("Seu Chute foi MAIOR que o Numero gerado.\n");
            }
            if(chutemenor) {
                printf("Seu Chute foi MENOR que o Numero gerado.\n");
            }
            tentativa++;

            double pontosremovidos = (chute - secretnumb) / (double)2; //Colocar 2.0 permite o valor ser compreendido como um double.
            if(pontosremovidos < 0 ) {
                pontosremovidos = pontosremovidos * -1;
            }
            pontos = pontos - pontosremovidos;
        }
    }

    //Modo Dificil
    while(modo == 1 && chute != secretnumb) {
        printf("Qual numero o programa gerou?\n");
        scanf("%d", &chute);
        printf("Seu chute foi: %d \n", chute);
        printf("Tentativa: %d\n", tentativa);
        if(chute < 0) {
            printf("\nNumeros negativos não são permitidos. Seu numero foi invalidado.\n");
           continue;
        } 
        int tentativas_dificil = 5;
        int acertou = {chute == secretnumb};
        int chutemaior = {chute > secretnumb};
        int chutemenor = {chute < secretnumb};
        int perdeu = {tentativa == tentativas_dificil};
        if(acertou) {
            printf("\n\nVocê Acertou!\nJogue novamente reniciando o programa.\n");
            printf("\nNumeros de tentativas: %d\n", tentativa-1);
            printf("Total de pontos %.1f\n", pontos);
            return 0;
        }
        if(perdeu) {
            printf("\n\nVocê perdeu, numero de tentativas excedida.\n\nJogue novamente reniciando o programa.");
            printf("Total de pontos %.1f\n", pontos);
            return 0;
        }
        else {
            if(chutemaior) {
                printf("Seu Chute foi MAIOR que o Numero gerado.\n");
            }
            if(chutemenor) {
                printf("Seu Chute foi MENOR que o Numero gerado.\n");
            }
            tentativa = tentativa + 1;

            double pontosremovidos = (chute - secretnumb) / (double)2;
            if(pontosremovidos < 0 ) {
                pontosremovidos = pontosremovidos * -1;
            }
            pontos = pontos - pontosremovidos;
            printf("%d", tentativas_dificil);
        }
    }
}