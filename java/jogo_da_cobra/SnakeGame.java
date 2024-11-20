package jogo_da_cobra;

import java.util.ArrayList;
import java.util.Random;

public class SnakeGame {
    private static final int HEIGHT = 10;
    private static final int WIDTH = 20;
    private static final char SNAKE_BODY = 'O';
    private static final char COMIDA = '*';
    private static final char EMPTY = ' ';
    
    private ArrayList<int[]> snake;
    private int[] comida;
    private char direction;
    boolean gameOver;
    
    public SnakeGame() {
        snake = new ArrayList<>();
        snake.add(new int[]{HEIGHT / 2, WIDTH / 2}); // posicao inicial da cobra, em um array.
        direction = 'R'; // Direção inicial
        spawnComida();
        gameOver = false;
    }
    
    private void spawnComida() {
        Random rand = new Random();
        int x, y;
        do {
            x = rand.nextInt(HEIGHT);
            y = rand.nextInt(WIDTH);
        } while (isSnakePosition(x, y));
        comida = new int[]{x, y};
    }
    
    private boolean isSnakePosition(int x, int y) {
        for (int[] segment : snake) {
            if (segment[0] == x && segment[1] == y) {
                return true;
            }
        }
        return false;
    }
    
    public void changeDirection(char newDirection) {
        // Impede a cobra de se mover na direção oposta
        if ((direction == 'U' && newDirection != 'D') ||
            (direction == 'D' && newDirection != 'U') ||
            (direction == 'L' && newDirection != 'R') ||
            (direction == 'R' && newDirection != 'L')) {
            direction = newDirection;
        }
    }
    
    public void update() {
        if (gameOver) return;
        
        int[] head = snake.get(0);
        int newX = head[0];
        int newY = head[1];
        
        switch (direction) {
            case 'U': newX--; break;
            case 'D': newX++; break;
            case 'L': newY--; break;
            case 'R': newY++; break;
        }
        
        // Verifica se a cobra colidiu com as bordas ou com ela mesma
        if (newX < 0 || newX >= HEIGHT || newY < 0 || newY >= WIDTH || isSnakePosition(newX, newY)) {
            gameOver = true;
            return;
        }
        
        // Adiciona nova cabeça
        snake.add(0, new int[]{newX, newY});
        
        // Verifica se comeu a comida
        if (newX == comida[0] && newY == comida[1]) {
            spawnComida(); // Gera nova comida
        } else {
            snake.remove(snake.size() - 1); // Remove a cauda
        }
    }
    
    public void printBoard() {
        //Usa 2 arrays para criar o "mapa"
        //Array I eh usado para altura
        //Array J para largura.
        //Comida spawna dentro de ambos arrays .

        for (int i = 0; i < HEIGHT; i++) {
            for (int j = 0; j < WIDTH; j++) {
                if (i == comida[0] && j == comida[1]) {
                    System.out.print(COMIDA);
                } else if (isSnakePosition(i, j)) {
                    System.out.print(SNAKE_BODY);
                } else {
                    System.out.print(EMPTY);
                }
            }
            System.out.println();
        }
        System.out.println("==============================");
        System.out.println("CONTROLES:");
        System.out.println("Use W (cima), S (baixo), A (esquerda), D (direita) para mover. Pressione Q para sair.");
    }
}