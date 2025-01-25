package POOJava.Usuario;

public class Usuario {
    public String nome;
    public int idade;
    public boolean adulto;


    //Construtor. Em Java, um construtor é um método especial que tem o !!mesmo nome da classe!! e não tem um tipo de retorno.
    public Usuario(String nome, int idade , boolean adulto){
        this.nome = nome;
        this.idade = idade;
        this.adulto = adulto;
    }

    //Funcao ou Metodo, feito com Void.
    public void imprimirdados(){
        System.out.print("//Nome do Usuario: "+this.nome);
        System.out.print(" //Idade do Usuario: "+this.idade+ " Anos.");
        System.out.println(" //Usuario é adulto? "+this.adulto);
    }

}