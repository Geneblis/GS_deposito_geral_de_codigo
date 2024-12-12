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
    
    JFrame frame = new JFrame("Minesweeper");
    JLabel textoTitulo = new JLabel();
    JPanel textoPainel = new JPanel();
    JPanel Borda = new JPanel();

    MineTile[][] board = new MineTile[numLin][numCols];
    ArrayList<MineTile> mineList;

    void setMines(){
        mineList = new ArrayList<MineTile>();

        mineList.add(board[2][2]);
        mineList.add(board[2][3]);
        mineList.add(board[3][4]);
        mineList.add(board[1][1]);
    }
    void revealMines(){
        for(int i=0; i< mineList.size(); i++){
            MineTile tile = mineList.get(i);
            tile.setText("💣");
        }
    }
    void checkMines(int r, int c){
        if(r < 0 || r >= numLin || c < 0 || c >= numCols ){
            return;
        }

        MineTile tile = board[r][c];
        tile.setEnabled(false);
        if(!tile.isEnabled()){
            return;
        }
        int minesFound = 0;
        minesFound += countMine(r-1, c-1);
        minesFound += countMine(r-1, c);
        minesFound += countMine(r-1, c+1);

        minesFound += countMine(r, c-1);
        minesFound += countMine(r, c+1);
    
        minesFound += countMine(r+1, c-1);
        minesFound += countMine(r+1, c);
        minesFound += countMine(r+1, c+1);

        if(minesFound > 0){
            tile.setText(Integer.toString(minesFound));
        }
        else{
            tile.setText("");

            checkMines(r-1, c-1);
            checkMines(r-1, c);
            checkMines(r, c-1);
            checkMines(r, c+1);
            checkMines(r+1, c-1);
            checkMines(r+1, c);
            checkMines(r+1, c+1);
        }
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
        textoTitulo.setText("Minesweeper");
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
                        MineTile tile = (MineTile) e.getSource();

                        if(e.getButton() == MouseEvent.BUTTON1){
                            if(tile.getText()==""){
                                if(mineList.contains(tile)){
                                    revealMines();
                                }
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
