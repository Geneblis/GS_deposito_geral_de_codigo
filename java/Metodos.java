import java.util.Scanner;

public class Methodos {
    //declaracao de metodo||function, vazio -> void
    static void imprime(){ 
        //comandos do metodo
        System.out.println("Ola!");
    }
    //Metodo com entrada
    static void soma(double a, double b){
        System.out.print("Soma de n1+n2 = ");
        System.out.println((a+b));
    }
    //Tentando fzr uma visiao, tive q informar valores com double.
    static void divisao(double a, double b){
        System.out.print("Divisao de n1+n2 = ");
        if(b == 0){
            System.out.println("Deu ruim.");
        } 
        else{
            System.out.println((a/b));
        }
    }
    public static void main(String[] args){
        Scanner teclado = new Scanner(System.in); 
        System.out.println("Insira o primeiro valor:");
        double n3 = teclado.nextDouble();
        System.out.println("Insira o segundo valor:");
        double n4 = teclado.nextDouble();
        double n1 = 348;
        double n2 = 2;
        imprime();
        soma(n1, n2);
        divisao(n3, n4);
        teclado.close();
    }
}