#include <stdio.h>

void init() {
    printf("Jogo inicializado...\n");
}

void gameLoop() {
    int choice;
    int game = 1;
    while (game == 1) {
        printf("Voce ve uma porta, o que voce faz?\n");
        printf("1- Entrar\n");
        printf("2- Voltar\n");
        printf("3- Outras Opcoes...\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &choice); // Lê a escolha do usuário
        getchar(); // Consome o caractere de nova linha

        switch (choice) {
            case 1:
                printf("Voce entrou na porta!\n");
                game = 0;
                break;
            case 2:
                printf("Voce voltou.\n");
                game = 0;
                break;
            case 3:
                printf("Outras opcoes...\n");
                game = 0;
                break;
            default:
                printf("Opcao invalida! Tente novamente.\n");
                game = 0;
                break;
        }
        printf("Pressione Enter para continuar...");
        getchar(); // Espera o usuário pressionar Enter
    }
}

void cleanup() {
    printf("Jogo finalizado!\n");
}

int main() {
    init(); // Inicializa o jogo
    gameLoop(); // Inicia o loop do jogo
    cleanup(); // Limpa e finaliza
    return 0;
}