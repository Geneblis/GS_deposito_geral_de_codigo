import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Random;

public class JogoDaCobraGUI extends JPanel implements ActionListener {
    private static final int LARGURA_TELA = 600;
    private static final int ALTURA_TELA = 600;
    private static final int TAMANHO_BLOCO = 25;
    private static final int NUM_BLOCOS = (LARGURA_TELA * ALTURA_TELA) / (TAMANHO_BLOCO * TAMANHO_BLOCO);
    private static final int VELOCIDADE = 150;

    private final int[] x = new int[NUM_BLOCOS];
    private final int[] y = new int[NUM_BLOCOS];
    private int tamanhoInicialCobra = 1;
    private int comidaX, comidaY;
    private char direcao = 'D'; // Direções: 'C' - cima, 'B' - baixo, 'E' - esquerda, 'D' - direita
    private boolean rodando = false;
    private Timer timer;
    private Random random;

    public JogoDaCobraGUI() {
        random = new Random();
        setPreferredSize(new Dimension(LARGURA_TELA, ALTURA_TELA));
        setBackground(Color.BLACK);
        setFocusable(true);
        addKeyListener(new ControleTeclado());
        iniciarJogo();
    }

    private void iniciarJogo() {
        rodando = true;
        gerarComida();
        timer = new Timer(VELOCIDADE, this);
        timer.start();
    }

    private void gerarComida() {
        comidaX = random.nextInt(LARGURA_TELA / TAMANHO_BLOCO) * TAMANHO_BLOCO;
        comidaY = random.nextInt(ALTURA_TELA / TAMANHO_BLOCO) * TAMANHO_BLOCO;
    }

    private void mover() {
        for (int i = tamanhoInicialCobra; i > 0; i--) {
            x[i] = x[i - 1];
            y[i] = y[i - 1];
        }

        switch (direcao) {
            case 'C': y[0] -= TAMANHO_BLOCO; break;
            case 'B': y[0] += TAMANHO_BLOCO; break;
            case 'E': x[0] -= TAMANHO_BLOCO; break;
            case 'D': x[0] += TAMANHO_BLOCO; break;
        }
    }

    private void verificarComida() {
        if (x[0] == comidaX && y[0] == comidaY) {
            tamanhoInicialCobra++;
            gerarComida();
        }
    }

    private void verificarColisao() {
        // Verificar colisão com o corpo
        for (int i = tamanhoInicialCobra; i > 0; i--) {
            if (x[0] == x[i] && y[0] == y[i]) {
                rodando = false;
                break;
            }
        }

        // Verificar colisão com bordas
        if (x[0] < 0 || x[0] >= LARGURA_TELA || y[0] < 0 || y[0] >= ALTURA_TELA) {
            rodando = false;
        }

        if (!rodando) {
            timer.stop();
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        if (rodando) {
            g.setColor(Color.RED);
            g.fillOval(comidaX, comidaY, TAMANHO_BLOCO, TAMANHO_BLOCO);

            for (int i = 0; i < tamanhoInicialCobra; i++) {
                if (i == 0) {
                    g.setColor(Color.GREEN);
                } else {
                    g.setColor(new Color(45, 180, 0));
                }
                g.fillRect(x[i], y[i], TAMANHO_BLOCO, TAMANHO_BLOCO);
            }

            g.setColor(Color.WHITE);
            g.drawString("Tamanho: " + tamanhoInicialCobra, 10, 10);
        } else {
            fimDeJogo(g);
        }
    }

    private void fimDeJogo(Graphics g) {
        g.setColor(Color.RED);
        g.setFont(new Font("Dialog", Font.BOLD, 50));
        FontMetrics metrics = getFontMetrics(g.getFont());
        g.drawString("FIM DE JOGO", (LARGURA_TELA - metrics.stringWidth("FIM DE JOGO")) / 2, ALTURA_TELA / 2);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (rodando) {
            mover();
            verificarComida();
            verificarColisao();
        }
        repaint();
    }

    private class ControleTeclado extends KeyAdapter {
        @Override
        public void keyPressed(KeyEvent e) {
            switch (e.getKeyCode()) {
                case KeyEvent.VK_W:
                    if (direcao != 'B') direcao = 'C';
                    break;
                case KeyEvent.VK_S:
                    if (direcao != 'C') direcao = 'B';
                    break;
                case KeyEvent.VK_A:
                    if (direcao != 'D') direcao = 'E';
                    break;
                case KeyEvent.VK_D:
                    if (direcao != 'E') direcao = 'D';
                    break;
            }
        }
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Jogo da Cobra 2.0");
        JogoDaCobraGUI jogo = new JogoDaCobraGUI();

        frame.add(jogo);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }
}
