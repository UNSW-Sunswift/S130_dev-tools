#include <iostream>
#include <thread>
#include <chrono>
#include "funny_node.hpp"
#include "bro.hpp"

int main() {
    FunnyNode funny_node(42);
    int32_t i = 0;
    while(true) {
        int32_t result = funny_node.compute_funny_value(i);
        std::cout << "Computed funny value: " << result << std::endl;
        std::cout << "bro: " << brochacho() << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
        i++;
    }
    return 0;
}