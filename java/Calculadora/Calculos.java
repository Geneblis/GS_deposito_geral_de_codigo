package Calculadora;

public class Calculos {

    public static void main (String[] args){
        // Soma adicao = new Soma();
        // int resultado = adicao.soma(a: 30, b: 30);
        // System.out.println(resultado);
        // 
        //// ADICAO FEITO COM METODOS A E B

        int resultado2 = Subtracao.subtracao(30, 30); //nao precisa declarar o objeto subtracao como pois foi definido como static.
        System.out.println(resultado2);


        Soma adicao = new Soma();
        adicao.parcela1 = 30;
        adicao.parcela2 = 60;
        adicao.soma();
    }
}