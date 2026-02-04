cmake_minimum_required(VERSION 3.15)
project(DecisionEngine VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -O3")

# Find Python (for pybind11)
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Add pybind11
add_subdirectory(pybind11)

# Source files
set(SOURCES
    decision_tree.cpp
    information_gain.cpp
    probability_engine.cpp
)

# Header files
set(HEADERS
    decision_tree.h
    information_gain.h
    probability_engine.h
)

# Create shared library
add_library(decision_engine SHARED ${SOURCES} ${HEADERS})

# Set library properties
set_target_properties(decision_engine PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
    PREFIX ""
    OUTPUT_NAME "decision_engine"
)

# Include directories
target_include_directories(decision_engine PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${Python3_INCLUDE_DIRS}
)

# Link libraries
target_link_libraries(decision_engine PRIVATE
    ${Python3_LIBRARIES}
)

# Python bindings (if using pybind11)
# Uncomment when pybind11 is set up
# pybind11_add_module(decision_engine_py bindings.cpp ${SOURCES})
# target_link_libraries(decision_engine_py PRIVATE decision_engine)

# Install targets
install(TARGETS decision_engine
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

# Testing
enable_testing()
add_subdirectory(tests)

# Print configuration
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "Python Version: ${Python3_VERSION}")