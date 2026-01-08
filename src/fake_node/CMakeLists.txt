set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin) 
add_executable(fake_node src/main.cpp src/funny_node.cpp)

SET (LIBS 
    std_types
    custom_types
    dds_node
    bro
)

target_include_directories(fake_node PRIVATE include)
target_link_libraries(fake_node PRIVATE ${LIBS})