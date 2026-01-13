# I hope globbing is safe
file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS *.cpp)

# Create lib
add_library(std_types STATIC ${SOURCES})

target_include_directories(
    std_types
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)