import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.util.ArrayList;
import java.util.Random;

public class SnakeGameGUI extends JPanel implements ActionListener {
    private static final int ALTURA = 10;
    private static final int LARGURA = 20;
    private static final int TAMANHO_CELULA = 30;
    
    private ArrayList<int[]> cobra;
    private int[] comida;
    private char direction;
    private boolean gameOver;
    private Timer timer;

    public SnakeGameGUI() {
        cobra = new ArrayList<>();
        cobra.add(new int[]{ALTURA / 2, LARGURA / 2}); // posição inicial da cobra
        direction = 'R'; // Direção inicial
        spawnComida();
        gameOver = false;

        timer = new Timer(250, this); // Atualização dos frames
        timer.start();

        setFocusable(true);
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                switch (e.getKeyCode()) {
                    case KeyEvent.VK_W: changeDirection('U'); break;
                    case KeyEvent.VK_S: changeDirection('D'); break;
                    case KeyEvent.VK_A: changeDirection('L'); break;
                    case KeyEvent.VK_D: changeDirection('R'); break;
                    case KeyEvent.VK_Q: System.exit(0); break; // Sair do jogo
                }
            }
        });
    }

    private void spawnComida() {
        Random rand = new Random();
        int x, y;
        do {
            x = rand.nextInt(ALTURA);
            y = rand.nextInt(LARGURA);
        } while (isCobraPosicao(x, y));
        comida = new int[]{x, y};
    }

    private boolean isCobraPosicao(int x, int y) {
        for (int[] segment : cobra) {
            if (segment[0] == x && segment[1] == y) {
                return true;
            }
        }
        return false;
    }

    public void changeDirection(char newDirection) {
        if ((direction == 'U' && newDirection != 'D') ||
            (direction == 'D' && newDirection != 'U') ||
            (direction == 'L' && newDirection != 'R') ||
            (direction == 'R' && newDirection != 'L')) {
            direction = newDirection;
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        
        if (gameOver) {
            // Muda a cor de fundo para vermelho
            g.setColor(Color.RED);
            g.fillRect(0, 0, getWidth(), getHeight());
            g.setColor(Color.WHITE); // Muda a cor do texto para branco
            g.drawString("Game Over!", LARGURA * TAMANHO_CELULA / 4, ALTURA * TAMANHO_CELULA / 2);
            return; // Não desenha mais nada
        }

        // Desenha a cobra
        g.setColor(Color.GREEN);
        for (int[] segment : cobra) {
            g.fillRect(segment[1] * TAMANHO_CELULA, segment[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA);
        }

        // Desenha a comida
        g.setColor(Color.RED);
        g.fillRect(comida[1] * TAMANHO_CELULA, comida[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA);
    }

    @Override
    public void actionPerformed(ActionEvent e) { // Método de atualização
        if (gameOver) return;

        int[] cabeca = cobra.get(0);
        int newX = cabeca[0];
        int newY = cabeca[1];

        switch (direction) {
            case 'U': newX--; break;
            case 'D': newX++; break;
            case 'L': newY--; break;
            case 'R': newY++; break;
        }

        if (newX < 0 || newX >= ALTURA || newY < 0 || newY >= LARGURA || isCobraPosicao(newX, newY)) {
            gameOver = true;
            timer.stop();
            return;
        }

        cobra.add(0, new int[]{newX, newY});

        if (newX == comida[0] && newY == comida[1]) {
            spawnComida();
        } else {
            cobra.remove(cobra.size() - 1);
        }

        repaint(); // Atualiza a tela
    }

    // main
    public static void main(String[] args) {
        JFrame frame = new JFrame("Jogo da Cobra 2.0");
        SnakeGameGUI game = new SnakeGameGUI();
        frame.add(game);
        frame.setSize(LARGURA * TAMANHO_CELULA, ALTURA * TAMANHO_CELULA);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
        frame.setResizable(false);
    }
}