import java.util.Scanner;

public class While_loop {
    public static void main(String[] args) {
        int contador = 8;
        int numeroaleatorio1 = 3;
        int numeroaleatorio2 = 7;   

        while (contador != 0) {
            numeroaleatorio1 = numeroaleatorio1 * numeroaleatorio2;
            numeroaleatorio2 = numeroaleatorio2 * numeroaleatorio1;
            System.out.println(numeroaleatorio1);
            System.out.println(numeroaleatorio2);
            System.out.println("Coloque 0 para finalizar o programa.");
            Scanner teclado = new Scanner(System.in);
            contador = teclado.nextInt();
            if(contador == 0) {
                teclado.close();
            }
        }
    }
}
