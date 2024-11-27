package rpg_game.src.main;

import javax.swing.JFrame;

public class Main {
    public static void main(String[] args) {
        JFrame tela = new JFrame();
        tela.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        tela.setResizable(false);
        tela.setTitle("");
        tela.setLocationRelativeTo(null); //centralizar

        GamePanel gamePanel = new GamePanel();
        tela.add(gamePanel);
        tela.pack(); //força a tela para tamanho do gamePanel.
        
        tela.setVisible(true);
        gamePanel.comecarJogoThread();
    }
}