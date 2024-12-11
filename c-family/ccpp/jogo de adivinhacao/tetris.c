#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

// Definição das constantes
#define TAMANHO_TELA 20
#define TAMANHO_PIECE 4

// Estrutura para representar uma peça
typedef struct {
    int forma[TAMANHO_PIECE][TAMANHO_PIECE];
    int x, y;
} Piece;

// Função para inicializar uma peça
void inicializarPiece(Piece *piece) {
    int forma = rand() % 7;
    switch (forma) {
        case 0: // I
            piece->forma[0][0] = 1;
            piece->forma[0][1] = 1;
            piece->forma[0][2] = 1;
            piece->forma[0][3] = 1;
            break;
        case 1: // J
            piece->forma[0][0] = 1;
            piece->forma[1][0] = 1;
            piece->forma[2][0] = 1;
            piece->forma[2][1] = 1;
            break;
        case 2: // L
            piece->forma[0][2] = 1;
            piece->forma[1][2] = 1;
            piece->forma[2][2] = 1;
            piece->forma[2][1] = 1;
            break;
        case 3: // O
            piece->forma[0][0] = 1;
            piece->forma[0][1] = 1;
            piece->forma[1][0] = 1;
            piece->forma[1][1] = 1;
            break;
        case 4: // S
            piece->forma[0][1] = 1;
            piece->forma[0][2] = 1;
            piece->forma[1][0] = 1;
            piece->forma[1][1] = 1;
            break;
        case 5: // T
            piece->forma[0][1] = 1;
            piece->forma[1][0] = 1;
            piece->forma[1][1] = 1;
            piece->forma[1][2] = 1;
            break;
        case 6: // Z
            piece->forma[0][0] = 1;
            piece->forma[0][1] = 1;
            piece->forma[1][1] = 1;
            piece->forma[1][2] = 1;
            break;
    }
    piece->x = TAMANHO_TELA / 2;
    piece->y = 0;
}

// Função para desenhar a tela
void desenharTela(int tela[TAMANHO_TELA][TAMANHO_TELA], Piece *piece) {
    int i, j;
    for (i = 0; i < TAMANHO_TELA; i++) {
        for (j = 0; j < TAMANHO_TELA; j++) {
            if (i == 0 || j == 0 || i == TAMANHO_TELA - 1 || j == TAMANHO_TELA - 1) {
                printf("#");
            } else if (tela[i][j] == 1) {
                printf("O");
            } else if (i >= piece->y && i < piece->y + TAMANHO_PIECE && j >= piece->x && j < piece->x + TAMANHO_PIECE) {
                if (piece->forma[i - piece->y][j - piece->x] == 1) {
                    printf("X");
                } else {
                    printf(" ");
                }
            } else {
                printf(" ");
            }
        }
        printf("\n");
    }
}

// Função para verificar colisão
int verificarColisao(int tela[TAMANHO_TELA][TAMANHO_TELA], Piece *piece) {
    int i, j;
    for (i = 0; i < TAMANHO_PIECE; i++) {
        for (j = 0; j < TAMANHO_PIECE; j++) {
            if (piece->forma[i][j] == 1) {
                if (piece->x + j < 1 || piece->x + j > TAMANHO_TELA - 2 || piece->y + i < 1 || piece->y + i > TAM ```c
> TAMANHO_TELA - 2) {
                    return 1;
                }
                if (tela[piece->y + i][piece->x + j] == 1) {
                    return 1;
                }
            }
        }
    }
    return 0;
}

// Função para mover a peça
void moverPiece(Piece *piece, int direcao) {
    switch (direcao) {
        case 1: // cima
            piece->y--;
            break;
        case 2: // baixo
            piece->y++;
            break;
        case 3: // esquerda
            piece->x--;
            break;
        case 4: // direita
            piece->x++;
            break;
    }
}

// Função para girar a peça
void girarPiece(Piece *piece) {
    int forma[TAMANHO_PIECE][TAMANHO_PIECE];
    int i, j;
    for (i = 0; i < TAMANHO_PIECE; i++) {
        for (j = 0; j < TAMANHO_PIECE; j++) {
            forma[j][TAMANHO_PIECE - 1 - i] = piece->forma[i][j];
        }
    }
    for (i = 0; i < TAMANHO_PIECE; i++) {
        for (j = 0; j < TAMANHO_PIECE; j++) {
            piece->forma[i][j] = forma[i][j];
        }
    }
}

int main() {
    int tela[TAMANHO_TELA][TAMANHO_TELA];
    int i, j;
    for (i = 0; i < TAMANHO_TELA; i++) {
        for (j = 0; j < TAMANHO_TELA; j++) {
            tela[i][j] = 0;
        }
    }
    Piece piece;
    inicializarPiece(&piece);
    int pontos = 0;

    while (1) {
        desenharTela(tela, &piece);
        printf("Pontos: %d\n", pontos);
        printf("Digite uma direção (1-cima, 2-baixo, 3-esquerda, 4-direita, 5-girar): ");
        int entrada;
        scanf("%d", &entrada);
        if (entrada >= 1 && entrada <= 4) {
            moverPiece(&piece, entrada);
            if (verificarColisao(tela, &piece)) {
                moverPiece(&piece, entrada == 1 ? 2 : entrada == 2 ? 1 : entrada == 3 ? 4 : 3);
            }
        } else if (entrada == 5) {
            girarPiece(&piece);
            if (verificarColisao(tela, &piece)) {
                girarPiece(&piece);
                girarPiece(&piece);
                girarPiece(&piece);
            }
        }
        if (piece.y + TAMANHO_PIECE > TAMANHO_TELA) {
            for (i = 0; i < TAMANHO_PIECE; i++) {
                for (j = 0; j < TAMANHO_PIECE; j++) {
                    if (piece.forma[i][j] == 1) {
                        tela[piece.y + i - TAMANHO_PIECE][piece.x + j] = 1;
                    }
                }
            }
            inicializarPiece(&piece);
            int linhas = 0;
            for (i = 0; i < TAMANHO_TELA; i++) {
                int linha = 1;
                for (j = 1; j < TAMANHO_TELA - 1; j++) {
                    if (tela[i][j] == 0) {
                        linha = 0;
                        break;
                    }
                }
                if (linha) {
                    linhas++;
                    for (j = i; j > 0; j--) {
                        for (int k = 1; k < TAMANHO_TELA - 1; k++) {
                            tela[j][k] = tela[j - 1][k];
                        }
                    }
                }
            }
            pontos += linhas * linhas;
        }
        usleep(100000); // pausa de 0.1 segundos
    }

    return 0;
}