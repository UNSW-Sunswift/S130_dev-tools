# Per-node info
set(TARGET_NAME bro_node)
set(SOURCES 
    src/main.cpp
)
set(INCLUDE_DIRS
    include
)
set (LIBS 
    dds_node
    std_types
    custom_types
    bro
)

# Compile and link
add_executable(${TARGET_NAME} ${SOURCES})
target_include_directories(${TARGET_NAME} PRIVATE ${INCLUDE_DIRS})
target_link_libraries(${TARGET_NAME} PRIVATE ${LIBS})

# Install time
install(
    TARGETS ${TARGET_NAME}
    RUNTIME DESTINATION bin
    COMPONENT ${TARGET_NAME}
)
install(
    FILES param/${TARGET_NAME}_param.json
    DESTINATION param
    COMPONENT ${TARGET_NAME}
)