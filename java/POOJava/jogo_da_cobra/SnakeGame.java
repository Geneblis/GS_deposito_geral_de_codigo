import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class SnakeGame {
    private static final int ALTURA = 10;
    private static final int LARGURA = 20;
    private static final char TAMANHO_COBRA = 'O';
    private static final char COMIDA = '*';
    private static final char EMPTY = ' ';
    
    private ArrayList<int[]> snake;
    private int[] comida;
    private char direction;
    boolean gameOver;
    
    public SnakeGame() {
        snake = new ArrayList();
        snake.add(new int[]{ALTURA / 2, LARGURA / 2}); // posicao inicial da cobra, em um array.
        direction = 'R'; // Direção inicial
        spawnComida();
        gameOver = false;
    }
    
    private void spawnComida() {
        Random rand = new Random();
        int x, y;
        do {
            x = rand.nextInt(ALTURA);
            y = rand.nextInt(LARGURA);
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
        //U - Upwards - Cima
        //D - Downwards - Baixo
        //L - Leftwards - Esquerda
        //R - Rightwards - Direita
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
        if (newX < 0 || newX >= ALTURA || newY < 0 || newY >= LARGURA || isSnakePosition(newX, newY)) {
            gameOver = true;
            return;
        }
        
        // Adiciona uma nova parte a cobra.
        snake.add(0, new int[]{newX, newY});
        
        // Verifica se comeu a comida
        if (newX == comida[0] && newY == comida[1]) {
            spawnComida(); // Gera nova comida
        } else {
            snake.remove(snake.size() - 1); // Remove a cauda
        }
    }
    
    public void printMapa() {
        //Usa 2 arrays para criar o "mapa"
        //Array I eh usado para altura
        //Array J para largura.
        //Comida spawna dentro de ambos arrays .

        System.out.println("===================="); //Setando uma altura
        for (int i = 0; i < ALTURA; i++) {
            System.out.print("|"); //Criando paredes
            for (int j = 0; j < LARGURA; j++) {
                if (i == comida[0] && j == comida[1]) {
                    System.out.print(COMIDA);
                } else if (isSnakePosition(i, j)) {
                    System.out.print(TAMANHO_COBRA);
                } else {
                    System.out.print(EMPTY);
                }
            }
            System.out.println();
        }
        System.out.println("===================="); //Chao + controles
        System.out.println("CONTROLES:");
        System.out.println("Use W (cima), S (baixo), A (esquerda), D (direita) para mover. Pressione Q para sair.");
    }

    public void Jogar(){
        Scanner teclado = new Scanner(System.in);
        while (gameOver == false) {
            printMapa();
            if (teclado.hasNextLine()) {
                String input = teclado.nextLine().toUpperCase();

                //movimentacao da cobra
                switch (input) {
                    case "W": changeDirection('U'); break;
                    case "S": changeDirection('D'); break;
                    case "A": changeDirection('L'); break;
                    case "D": changeDirection('R'); break;
                    case "Q": changeDirection('Q'); break;
                    //Q para sair do jogo.
                }
            }
            update();
        }
        
        System.out.println("Game Over!");
        teclado.close();
    }

    public static void main(String[] args) {
        SnakeGame jogo = new SnakeGame();
        jogo.Jogar();
    }
}