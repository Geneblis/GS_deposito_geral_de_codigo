import java.util.Scanner;

public class Main{
    public static void main(String[] arg) {
        Scanner teclado = new Scanner(System.in);
        System.out.println("Teu peso");
        double peso = teclado.nextDouble();      
        System.out.println("Tua altura");
        double alt = teclado.nextDouble();
        double imc = peso / (alt * alt);
        System.out.println("Seu IMC eh de: ");
        System.out.print(imc);
        teclado.close();
        
    }
}