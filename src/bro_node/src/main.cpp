#include <iostream>
#include <thread>
#include <chrono>
#include "bro.hpp"

int main() {
    std::cout << brochacho() << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(1));

}