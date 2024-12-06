public class Animal {
    String tipo;
    String som;

    public void oAnimalFaz(){
        System.out.println( "O Animal: "+tipo+", faz: " +som);
    }
    public static void main(String[] args) {
        Animal animal1 = new Animal();
        animal1.tipo = "Cachorro";
        animal1.som = "Latido";
        animal1.oAnimalFaz();
        Animal animal2 = new Animal();
        animal2.tipo = "Gato";
        animal2.som = "Miado";
        animal2.oAnimalFaz();
    }
}