# Glob for all sources
file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS *.cpp)

# Create lib
add_library(custom_types STATIC ${SOURCES})

target_include_directories(
    custom_types
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)