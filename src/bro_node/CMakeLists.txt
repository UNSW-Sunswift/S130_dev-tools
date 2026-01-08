set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin) 
add_executable(bro_node src/bro_node.cpp)

SET (LIBS 
    bro
)

target_include_directories(bro_node PRIVATE include)
target_link_libraries(bro_node PRIVATE ${LIBS})