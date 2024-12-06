package POO_master_classes.Usuario;

public class Main {
    public static void main (String args[]){
        Usuario usuario1 = new Usuario("x",22, false);
        usuario1.nome = "Pedro";
        usuario1.adulto = true;
        Usuario usuario2 = new Usuario("Maria",2, false);
        usuario1.imprimirdados();
        usuario2.imprimirdados();
    }
}
