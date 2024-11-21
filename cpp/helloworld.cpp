#include <array>
#include <iostream>
#include <string>


void sla(){
    std::string carruagem_string = "Carruagem";
    std::cout << carruagem_string << std::endl;
}

void array_basica(){
    std::array<int, 3> array_1{{1, 2,3}};
    for (const auto& elementos_para_string : array_1) {
       std::cout << elementos_para_string << " ";
    }
    std::cout << "" << std::endl;
}

int main() {
    array_basica();
    sla();
    std::cout << "Dale mundo." << std::endl; //

    return 0;

}