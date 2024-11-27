package rpg_game.src.main;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.text.ListFormat.Style;

import javax.swing.JPanel;

public class GamePanel extends JPanel implements Runnable {

    //Configuracoes de Tela
    final int originalTamanhoTile = 16;
    final int escala = 3;

    final int tileTamanho = originalTamanhoTile * escala; //escala apliada, 64 tile
    final int maxScreenColuna = 16;
    final int maxScreenLinha = 12;
    final int screenWidth = tileTamanho * maxScreenColuna; //1024
    final int screenHeight = tileTamanho * maxScreenLinha; //768

    //fps cap
    final int fps = 60;
    
    Thread gameThread;
    KeyHandler keyH = new KeyHandler();

    //posicao do jogador
    int playerX = 100;
    int playerY = 100;
    int playerV = 4; //velocidade, 4 pixeis.

    public GamePanel(){

        this.setPreferredSize(new Dimension(screenWidth, screenHeight));
        this.setBackground(Color.black);
        this.setDoubleBuffered(true);
        this.addKeyListener(keyH);
        this.setFocusable(true);
        
    }

    public void comecarJogoThread(){
        gameThread = new Thread(this);
        gameThread.start();
    }


    public void run() {
        System.out.println("Jogo iniciou!");
        double drawIntervalo = 1000000000.0 / fps; // Intervalo em nanosegundos
        double delta = 0;
        long sistemaTempo = System.nanoTime();
        long atualTempo;
        long timer = 0;
        int contadorDraw = 0;


        //renderizador usando Delta, melhor performance.
        while (gameThread != null) {
            try {
                atualTempo = System.nanoTime();
                delta += (atualTempo - sistemaTempo) / drawIntervalo;
                timer += (atualTempo - sistemaTempo);
                sistemaTempo = atualTempo;
            
                if (delta >= 1) {
                    update();
                    repaint();
                    delta--;
                    contadorDraw++;
                }
                if (timer >= 1000000000) {
                    System.out.println("FPS:" + contadorDraw);
                    contadorDraw = 0;
                    timer = 0;
                }
                // Pequeno atraso para evitar que o loop consuma muito CPU
                Thread.sleep(1); 
            }catch (Exception e) {
                System.err.println("Algo deu errado na execução do run().");
                e.printStackTrace(); // Imprime qualquer exceção que ocorra
            }
        }
    }

    public void update(){

        //X+ direita, Y+ cima.
        if(keyH.upPressed == true){
            playerY = playerY - playerV;
        }else if(keyH.downPressed == true) {
            playerY = playerY + playerV;
        }else if(keyH.leftPressed == true) {
            playerX = playerX - playerV;
        }else if(keyH.rightPressed == true) {
            playerX = playerX + playerV;
        }
    }
    public void paintComponent(Graphics g){
        super.paintComponent(g);

        Graphics2D g2 = (Graphics2D)g;
        g2.setColor(Color.white);
        g2.fillRect(playerX, playerY, tileTamanho, tileTamanho);
        g2.dispose();
    }

}
