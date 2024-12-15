# Self equivale this em outras linguagens
class Animal:
    def __init__(self, name):
        self.name = name
        self.is_alive = True

    def eat(self):
        print(f"{self.name} is eating.")

    def sleep(self):
        print(f"{self.name} is sleeping.")

class Dog(Animal):
    def speak(self):
        print(f"{self.name} said 'WOOF!' ")

class Cat(Animal):
    pass

class Mice(Animal):
    pass

dog = Dog("Scooby")
cat = Cat("Garfield")
mice = Mice("Mickey")

print(dog.name)
print(dog.is_alive)
dog.speak()
mice.sleep()
mice.eat()