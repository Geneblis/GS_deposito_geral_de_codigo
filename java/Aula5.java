import java.util.Scanner;

public class Aula5 {
    public static void main(String[] args) {
        int resposta = 2;
        while(resposta!=1){
            System.out.println("Insira um valor:");
            Scanner teclado = new Scanner(System.in);
            double valor = teclado.nextDouble();
            if(valor <= 99.99 ){
                System.out.println("Sem desconto.");
                System.out.println("Total a pagar:");
                System.out.println(valor);
            }
            if(valor >= 100 && valor<1000){
                System.out.println("Voce recebeu 10% de desconto!");
                double desconto = valor * 0.1;
                valor = valor - desconto;
                System.out.println("Total a pagar:");
                System.out.println(valor);
            }
            else if(valor>=100 && valor>=1000){
                System.out.println("Voce recebeu um desconto de 95%!");
                double desconto = valor * 0.9;
                valor = valor - desconto;
                System.out.println("Total a pagar:");
                System.out.println(valor);
            }
            else{
                System.out.println("Total a pagar:");
                System.out.println(valor);
            }
            System.out.print("Desja continuar? 1-parar, 2-continuar");
            resposta = teclado.nextInt();
            //teclado.close();
        }
    }
}
