import os


def generate_cmake(folder_path, file_names):
    # folder check
    os.makedirs(folder_path, exist_ok=True)

    # Path to the CMakeLists.txt file
    cmake_file_path = os.path.join(folder_path, "CMakeLists.txt")

    # CMake content
    cmake_content = f"""cmake_minimum_required(VERSION 3.17)
project(project1 C)

set(CMAKE_C_STANDARD 11)

add_compile_options(
      "-ggdb3"
      "-Werror"
      "-Wall"
      "-xc"
      "-Wno-error=parentheses"
      "-pedantic"
      "-fdiagnostics-color"
      "-fmax-errors=5"
      "-Werror=vla"
      "-Wno-error=implicit-fallthrough"
      "-Wno-parentheses"
      "-Wextra"
      "-Wno-error=unused-parameter"
      "-std=c11"
)

add_link_options(
        "-Wl,-wrap,main"
        "-Wl,-Map=main.map"
        "-ggdb3"
        "-Wl,-cref"
)

add_executable(project1
"""
    # files added
    for file_name in file_names:
        cmake_content += f'        "{file_name}"\n'

    cmake_content += """)

# Dołącz niezbędne biblioteki
target_link_libraries(project1
        "m"
)
"""

    with open(cmake_file_path, "w") as cmake_file:
        cmake_file.write(cmake_content)
