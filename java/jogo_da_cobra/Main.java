package jogo_da_cobra;

import java.util.Scanner;


public class Main {
    public static void main(String[] args) {
        SnakeGame game = new SnakeGame();
        Scanner teclado = new Scanner(System.in);
        while (game.gameOver == false) {
            game.printBoard();
            if (teclado.hasNextLine()) {
                String input = teclado.nextLine().toUpperCase();

                //movimentacao da cobra
                switch (input) {
                    case "W": game.changeDirection('U'); break;
                    case "S": game.changeDirection('D'); break;
                    case "A": game.changeDirection('L'); break;
                    case "D": game.changeDirection('R'); break;
                    case "Q": game.changeDirection('Q'); break;
                    //Q para sair do jogo.
                }
            }
            game.update();
        }
        
        System.out.println("Game Over!");
        teclado.close();
    }
}