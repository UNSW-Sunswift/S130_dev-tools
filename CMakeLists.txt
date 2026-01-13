cmake_minimum_required(VERSION 3.20)
project(SR_DRIVE)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# global tools always needed during install
install(
    FILES sunswift-dev-tools/target/srlaunch launch/launch_config.json
    DESTINATION tools
    COMPONENT tools
)
add_subdirectory(src)
add_subdirectory(core)