set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/deploy/bin) 
add_executable(funny_node src/main.cpp src/funny_node.cpp)

SET (LIBS 
    dds_node
    std_types
    custom_types
)

target_include_directories(funny_node PRIVATE include)
target_link_libraries(funny_node PRIVATE ${LIBS})