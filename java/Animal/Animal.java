public class Animal {
    String tipo;
    String som;

    public void oAnimalFaz(){
        System.out.println("O animal faz: " +tipo);
    }
    public static void main(String[] args) {
        Animal animal1 = new Animal();
        animal1.tipo = "Cachorro";
        animal1.som = "Latido";
        animal1.oAnimalFaz();
    }
}