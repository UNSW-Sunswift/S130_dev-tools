#include "std_types.hpp"
#include <chrono>
#include <thread>
#include <iostream>
#include <cstdint>

int main() {
    int32_t starting = 100;
    Int32 my_int = Int32(starting);
    std::cout << "My initial integer is " << my_int.get_int() << std::endl;

    int i = 0;
    while(true) {
        i++;
        my_int.set_int(starting + i);
        std::cout << "my int is " << my_int.get_int() << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    return 0;
}