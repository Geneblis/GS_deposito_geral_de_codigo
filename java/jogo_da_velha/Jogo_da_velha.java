import java.awt.*;
import java.awt.event.*;
import java.util.*;
import javax.swing.*;



public class Jogo_da_velha implements ActionListener {
    
    Random random = new Random();
    JFrame frame = new JFrame();
    JPanel tituloPanel = new JPanel();
    JPanel buttonPanel = new JPanel();
    JLabel textfield = new JLabel();
    JButton[] buttons = new JButton[9];
    boolean jogador1_turno;

    Jogo_da_velha(){
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800,800);
        frame.getContentPane().setBackground(new Color(50,50,50));
        frame.setLayout(new BorderLayout());
        frame.setVisible(true);

        //texto
        textfield.setBackground(new Color(25,25,25));
        textfield.setForeground(new Color(25,255,0));
        textfield.setFont(new Font("DialogInput", Font.BOLD, 75));
        textfield.setHorizontalAlignment(JLabel.CENTER);
        textfield.setText("Jogo da Velha");
        textfield.setOpaque(true);

        //titulo
        tituloPanel.setLayout(new BorderLayout());
        tituloPanel.setBounds(0,0,800,100);

        //jogo
        buttonPanel.setLayout(new GridLayout(3,3));;
        buttonPanel.setBackground(new Color(150,150,150));

        for(int i=0;i<9;i++){
            buttons[i] = new JButton();
            buttonPanel.add(buttons[i]);
            buttons[i].setFont(new Font("MV Boli", Font.BOLD, 120));
            buttons[i].addActionListener(this);


        }

        //painel completo
        tituloPanel.add(textfield);
        frame.add(tituloPanel,BorderLayout.NORTH);
        frame.add(buttonPanel);

        //comeco do jogo
        primeiroTurno();
    }

    @Override
    public void actionPerformed(ActionEvent e){
        //Executor de partidas.
        for(int i=0;i<9;i++){
            if(e.getSource()==buttons[i]){
                if(jogador1_turno){ //turno do jogador X
                    if(buttons[i].getText()==""){
                        buttons[i].setForeground(new Color(255,0,0));
                        buttons[i].setText("X");
                        jogador1_turno=false;
                        textfield.setText("Turno O");
                        check();
                    }
                }
                else{
                    if(buttons[i].getText()==""){ //turno do jogador O
                        buttons[i].setForeground(new Color(0,0,255));
                        buttons[i].setText("O");
                        jogador1_turno=true;
                        textfield.setText("Turno X");
                        check();
                    }
                }
            }
        }
    }

    public void primeiroTurno(){
        try {
            Thread.sleep(2000);
        }catch(InterruptedException e){
            e.printStackTrace();
            System.err.println("Erro ao computar partida.");
        }
        if(random.nextInt(2)==0){ //Determina quem começa a partida.
            jogador1_turno=true;
            textfield.setText("Turno X");
        }
        else{
            jogador1_turno=false;
            textfield.setText("Turno O");
        }
    }

    public void xVence(int a, int b, int c){
        buttons[a].setBackground(Color.GREEN);
        buttons[b].setBackground(Color.GREEN);
        buttons[c].setBackground(Color.GREEN);

        for (int i=0;i<9;i++){
            buttons[i].setEnabled(false);
        }
        textfield.setText("Jogador X Venceu!");
    }

    public void OVence(int a, int b, int c){
        buttons[a].setBackground(Color.GREEN);
        buttons[b].setBackground(Color.GREEN);
        buttons[c].setBackground(Color.GREEN);

        for (int i=0;i<9;i++){
            buttons[i].setEnabled(false);
        }
        textfield.setText("Jogador O Venceu!");
    }

    public void check(){
        //Vitoria do jogador X
        //vai doer os olhos tentar ler este codigo.
        if(
            (buttons[0].getText()=="X") &&
            (buttons[1].getText()=="X") &&
            (buttons[2].getText()=="X")
        ){
            xVence(0, 1, 2);
        }

        if(
            (buttons[3].getText()=="X") &&
            (buttons[4].getText()=="X") &&
            (buttons[5].getText()=="X")
        ){
            xVence(3, 4, 5);
        }

        if(
            (buttons[6].getText()=="X") &&
            (buttons[7].getText()=="X") &&
            (buttons[8].getText()=="X")
        ){
            xVence(6, 7, 8);
        }

        if(
            (buttons[0].getText()=="X") &&
            (buttons[3].getText()=="X") &&
            (buttons[6].getText()=="X")
        ){
            xVence(0, 3, 6);
        }

        if(
            (buttons[1].getText()=="X") &&
            (buttons[4].getText()=="X") &&
            (buttons[7].getText()=="X")
        ){
            xVence(1, 4, 7);
        }

        if(
            (buttons[2].getText()=="X") &&
            (buttons[5].getText()=="X") &&
            (buttons[8].getText()=="X")
        ){
            xVence(2, 5, 8);
        }

        if(
            (buttons[0].getText()=="X") &&
            (buttons[4].getText()=="X") &&
            (buttons[8].getText()=="X")
        ){
            xVence(0, 4, 8);
        }

        if(
            (buttons[2].getText()=="X") &&
            (buttons[4].getText()=="X") &&
            (buttons[6].getText()=="X")
        ){
            xVence(2, 4, 6);
        }

        //Vitoria do jogador O
        if(
            (buttons[0].getText()=="O") &&
            (buttons[1].getText()=="O") &&
            (buttons[2].getText()=="O")
        ){
            OVence(0, 1, 2);
        }

        if(
            (buttons[3].getText()=="O") &&
            (buttons[4].getText()=="O") &&
            (buttons[5].getText()=="O")
        ){
            OVence(3, 4, 5);
        }

        if(
            (buttons[6].getText()=="O") &&
            (buttons[7].getText()=="O") &&
            (buttons[8].getText()=="O")
        ){
            OVence(6, 7, 8);
        }

        if(
            (buttons[0].getText()=="O") &&
            (buttons[3].getText()=="O") &&
            (buttons[6].getText()=="O")
        ){
            OVence(0, 3, 6);
        }

        if(
            (buttons[1].getText()=="O") &&
            (buttons[4].getText()=="O") &&
            (buttons[7].getText()=="O")
        ){
            OVence(1, 4, 7);
        }

        if(
            (buttons[2].getText()=="O") &&
            (buttons[5].getText()=="O") &&
            (buttons[8].getText()=="O")
        ){
            OVence(2, 5, 8);
        }

        if(
            (buttons[0].getText()=="O") &&
            (buttons[4].getText()=="O") &&
            (buttons[8].getText()=="O")
        ){
            OVence(0, 4, 8);
        }

        if(
            (buttons[2].getText()=="O") &&
            (buttons[4].getText()=="O") &&
            (buttons[6].getText()=="O")
        ){
            OVence(2, 4, 6);
        }

    }

}