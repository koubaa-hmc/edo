cmake_minimum_required(VERSION 3.16)

project(EdoClient VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Find Qt packages
find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick QuickControls2)

# Main application executable
add_executable(edoclient_bin
    src/main.cpp
)

target_link_libraries(edoclient_bin PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
    Qt6::QuickControls2
)

# Set QML import path
target_compile_definitions(edoclient_bin PRIVATE
    QML_IMPORT_PATH="${CMAKE_SOURCE_DIR}/qml"
)

# Copy QML files to build directory
file(COPY ${CMAKE_SOURCE_DIR}/qml DESTINATION ${CMAKE_BINARY_DIR})

# Install targets
install(TARGETS edoclient_bin
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# Deploy QML files
install(DIRECTORY qml/ DESTINATION share/edoclient/qml)

# Print configuration
message(STATUS "Qt Version: ${Qt6_VERSION}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "Install Prefix: ${CMAKE_INSTALL_PREFIX}")
