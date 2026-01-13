# Glob for all sources
set(SOURCES bro.cpp)

# Create lib
add_library(bro STATIC ${SOURCES})

target_include_directories(
    bro
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(
    bro
    PUBLIC
    std_types
)