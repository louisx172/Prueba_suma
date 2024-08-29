#include <iostream>

int main() {
    float a, b;
    std::cout << "Ingrese el valor de a: ";
    std::cin >> a;
    std::cout << "Ingrese el valor de b: ";
    std::cin >> b;
    float resultado = a + b;
    std::cout << "El resultado de la suma es: " << resultado << std::endl;
    return 0;
}