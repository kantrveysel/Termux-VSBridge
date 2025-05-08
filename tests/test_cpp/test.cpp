#include <iostream>
#include <chrono>
#include <thread>

int main() {
    std::cout << "Starting C++ test" << std::endl;
    for (int i = -3; i < 0; ++i) {
        std::cout << i << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    std::cout << "Finished" << std::endl;
    return 0;
}