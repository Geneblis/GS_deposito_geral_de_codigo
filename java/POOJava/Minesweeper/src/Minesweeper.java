import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Random;
import javax.swing.*;

public class Minesweeper {
    private class MineTile extends JButton{
        int r;
        int c;

        public MineTile(int r, int c){
            this.r = r;
            this.c = c;
        }
    }

    int tamanhoTile = 70;
    int numLin = 8;
    int numCols = numLin;
    int bordaLargura = numCols * tamanhoTile;
    int bordaAltura = numLin * tamanhoTile;
    int tilesClicados = 0;
    int totalMinas = 12;
    Random aleatorizador = new Random();

    JFrame frame = new JFrame("Minesweeper");
    JLabel textoTitulo = new JLabel();
    JPanel textoPainel = new JPanel();
    JPanel Borda = new JPanel();

    MineTile[][] board = new MineTile[numLin][numCols];
    ArrayList<MineTile> mineList;
    boolean gameOver = false;

    void setMines(){
        mineList = new ArrayList<MineTile>();
        int mineLeft = totalMinas;
        while(mineLeft > 0){
            int r = aleatorizador.nextInt(numLin);
            int c = aleatorizador.nextInt(numCols);

            MineTile tile = board[r][c];    
            if (!mineList.contains(tile)){
                mineList.add(tile);
                mineLeft -= 1;
            }    
        }
    }
    void revealMines(){
        for(int i=0; i< mineList.size(); i++){
            MineTile tile = mineList.get(i);
            tile.setText("💣");
        }

        gameOver = true;
        textoTitulo.setText("Game Over!");
    }
    void checkMines(int r, int c) {
        if (r < 0 || r >= numLin || c < 0 || c >= numCols) {
            return;
        }

        MineTile tile = board[r][c];
        if (!tile.isEnabled()) {
            return; // Se o tile já foi revelado, não faça nada
        }

        tile.setEnabled(false);
        tilesClicados += 1;
        int minesFound = countAdjacentMines(r, c);

        if (minesFound > 0) {
        tile.setText(Integer.toString(minesFound));
        } 
        else {
            tile.setText("");
            checkMines(r - 1, c - 1);
            checkMines(r - 1, c);
            checkMines(r - 1, c + 1);
            checkMines(r, c - 1);
        checkMines(r, c + 1);
        checkMines(r + 1, c - 1);
            checkMines(r + 1, c);
            checkMines(r + 1, c + 1);
        }

        if(tilesClicados == numLin * numCols - mineList.size()) {
            gameOver = true;
            textoTitulo.setText("Minas Liberadas!");
        }
    }

    int countAdjacentMines(int r, int c) {
        int minesFound = 0;
        for (int i = -1; i <= 1; i++) {
            for (int j = -1; j <= 1; j++) {
                if (i == 0 && j == 0) continue; // Ignora o próprio tile
                if (countMine(r + i, c + j) == 1) {
                    minesFound++;
                }
            }
        }
        return minesFound;
    }
    int countMine(int r, int c){
        if(r < 0 || r >= numLin || c < 0 || c >= numCols ){
            return 0;
        }
        if(mineList.contains(board[r][c])){
            return 1;
        }
        return 0;
    }

    Minesweeper(){
        frame.setSize(bordaLargura, bordaAltura);
        frame.setLocationRelativeTo(null);
        frame.setResizable(false);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());

        textoTitulo.setFont(new Font("Arial", Font.BOLD, 25));
        textoTitulo.setHorizontalAlignment(JLabel.CENTER);
        textoTitulo.setText("Minesweeper: " +Integer.toString(totalMinas));
        textoTitulo.setOpaque(true);
        
        textoPainel.setLayout(new BorderLayout());
        textoPainel.add(textoTitulo);
        frame.add(textoPainel, BorderLayout.NORTH);

        Borda.setLayout(new GridLayout(numLin, numCols));
        frame.add(Borda);
    
        for (int r = 0; r < numLin; r++){
            for(int c = 0; c < numCols; c++){
                MineTile tile = new MineTile(r, c);
                board[r][c] = tile;
                
                tile.setFocusable(false);
                tile.setMargin(new Insets(0, 0, 0, 0));
                tile.setFont(new Font("Arial Unicode MS", Font.PLAIN, 45));
                tile.addMouseListener(new MouseAdapter() {
                    @Override
                    public void mousePressed(MouseEvent e) {
                        if(gameOver){
                            return;
                        }
                        MineTile tile = (MineTile) e.getSource();
                    
                        if (e.getButton() == MouseEvent.BUTTON1) {
                            if (tile.getText().equals("")) {
                                if (mineList.contains(tile)) {
                                    revealMines();
                                } else {
                                    checkMines(tile.r, tile.c);
                                }
                            }
                        }
                        else if(e.getButton() == MouseEvent.BUTTON3){
                            if(tile.getText() == "" && tile.isEnabled()){
                                tile.setText("🚩");
                            }
                            else if(tile.getText() == "🚩"){
                                tile.setText("");
                            }
                        }
                    }
                });
                Borda.add(tile);
            }
        }

        frame.setVisible(true);

        setMines();
    }

    public static void main (String[] args) throws Exception {
        Minesweeper minesweeper = new Minesweeper();
    }
}
