package POO_master_classes.Usuario;

public class Administrador {
    private Usuario usuario;

    public void definir_nome(String nome) {
        if (usuario == null) {
            usuario = new Usuario(nome, 0, false);
        } else {
            usuario.nome = nome;
        }
    }

    public Usuario getUsuario() {
        return usuario;
    }
}