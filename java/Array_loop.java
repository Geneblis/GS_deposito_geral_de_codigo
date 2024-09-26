import java.util.Arrays;
import java.util.Scanner;

public class Array_loop {
    public static void main(String[] args) {
        String nomes_array[] = {"Iago", "So", "Faz"};
        Scanner teclado = new Scanner(System.in);
        for(int i=1; i <= 3 ; i++){
            System.out.println("Coloque o nome correspondente ao numero: " +i);
            nomes_array[i-1] = teclado.next();
        }
        System.out.println(Arrays.toString(nomes_array));
        teclado.close();
    }
}
