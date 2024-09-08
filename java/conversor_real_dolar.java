import java.util.Scanner;

public class conversor_real_dolar {
    public static void main(String[] args) {
        System.out.println("Ola!");
        double dolar = 5.65;
        double real = 0.177;

        Scanner teclado = new Scanner(System.in); 
        System.out.println("Selecione a conversão: 1- Dolar para real. 2- Real para dolar.");
        int modo = teclado.nextInt();
        if(modo == 1){
            System.out.println("Coloque abaixo a quantidade de Dolares que deseja converter para Real.");
            double conversor = teclado.nextDouble();
            double i = conversor * dolar;
            System.out.print("Deu aproximadamente: " +i);
            System.out.println(" Em Reais/BRLs");
            teclado.close();
        }
        else{
            System.out.println("Coloque abaixo a quantidade de Reais que deseja converter para Dolares.");
            double conversor = teclado.nextDouble();
            double i = conversor * real;
            System.out.print("Deu aproximadamente: " +i);
            System.out.println(" Em Dolares/USD");
            teclado.close();
        }
    }
}
