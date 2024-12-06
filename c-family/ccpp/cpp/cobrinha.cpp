#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <string>
#include <conio.h> // Para _kbhit() e _getch()

using namespace std;

class SnakeGame {
private:
    static const int ALTURA = 10;
    static const int LARGURA = 20;
    static const char TAMANHO_COBRA = 'O';
    static const char COMIDA = '*';
    static const char EMPTY = ' ';
    
    vector<pair<int, int>> snake;
    pair<int, int> comida;
    char direction;
    bool gameOver;

    void spawnComida() {
        int x, y;
        do {
            x = rand() % ALTURA;
            y = rand() % LARGURA;
        } while (isSnakePosition(x, y));
        comida = {x, y};
    }

    bool isSnakePosition(int x, int y) {
        for (const auto& segment : snake) {
            if (segment.first == x && segment.second == y) {
                return true;
            }
        }
        return false;
    }

public:
    SnakeGame() {
        srand(static_cast<unsigned int>(time(0))); // Inicializa o gerador de números aleatórios
        snake.push_back({ALTURA / 2, LARGURA / 2}); // Posição inicial da cobra
        direction = 'R'; // Direção inicial
        spawnComida();
        gameOver = false;
    }

    void changeDirection(char newDirection) {
        // Impede a cobra de se mover na direção oposta
        if ((direction == 'U' && newDirection != 'D') ||
            (direction == 'D' && newDirection != 'U') ||
            (direction == 'L' && newDirection != 'R') ||
            (direction == 'R' && newDirection != 'L')) {
            direction = newDirection;
        }
    }

    void update() {
        if (gameOver) return;

        auto head = snake.front();
        int newX = head.first;
        int newY = head.second;

        switch (direction) {
            case 'U': newX--; break;
            case 'D': newX++; break;
            case 'L': newY--; break;
            case 'R': newY++; break;
        }

        // Verifica se a cobra colidiu com as bordas ou com ela mesma
        if (newX < 0 || newX >= ALTURA || newY < 0 || newY >= LARGURA || isSnakePosition(newX, newY)) {
            gameOver = true;
            return;
        }

        // Adiciona uma nova parte à cobra
        snake.insert(snake.begin(), {newX, newY});

        // Verifica se comeu a comida
        if (newX == comida.first && newY == comida.second) {
            spawnComida(); // Gera nova comida
        } else {
            snake.pop_back(); // Remove a cauda
        }
    }

    void printMapa() {
        cout << "====================" << endl; // Setando uma altura
        for (int i = 0; i < ALTURA; i++) {
            cout << "|"; // Criando paredes
            for (int j = 0; j < LARGURA; j++) {
                if (i == comida.first && j == comida.second) {
                    cout << COMIDA;
                } else if (isSnakePosition(i, j)) {
                    cout << TAMANHO_COBRA;
                } else {
                    cout << EMPTY;
                }
            }
            cout << endl;
        }
        cout << "====================" << endl; // Chão + controles
        cout << "CONTROLES:" << endl;
        cout << "Use W (cima), S (baixo), A (esquerda), D (direita) para mover. Pressione Q para sair." << endl;
    }

    void Jogar() {
        while (!gameOver) {
            printMapa();
            if (_kbhit()) { // Verifica se uma tecla foi pressionada
                char input = _getch(); // Lê a tecla pressionada
                input = toupper(input); // Converte para maiúscula

                // Movimentação da cobra
                if (input == 'W') changeDirection('U');
                else if (input == 'S') changeDirection('D');
                else if (input == ' A') changeDirection('L');
                else if (input == 'D') changeDirection('R');
                else if (input == 'Q') break; // Q para sair do jogo

                update(); // Atualiza o estado do jogo apenas quando uma tecla é pressionada
            }
        }

        cout << "Game Over!" << endl;
    }
};

int main() {
    SnakeGame game;
    game.Jogar();
    return 0;
}