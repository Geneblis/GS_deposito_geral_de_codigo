import java.util.Scanner;

public class Teste_scanner_string {
    public static void main(String[] args) {
        System.out.println("teste");
        Scanner teclado = new Scanner(System.in);
        System.out.println("Qual seu nome?");
        String nome = teclado.next();
        System.out.println("Ola, " +nome);
        teclado.close();
    }
}