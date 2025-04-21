import os
import subprocess
from c_project_management.c_make_lists_GENERATOR import generate_cmake

# PRINTS TO DELETE

def build_and_execute_project(folder_path, file_names):
    # Generate CMakeLists.txt
    cmake_file_path = generate_cmake(os.path.join(folder_path, "CMakeLists.txt"), file_names)
    print(f"CMakeLists.txt generated at: {cmake_file_path}")

    # Build project
    try:
        # Run cmake
        subprocess.run(["cmake", "."], cwd=folder_path, check=True)
        # Run make
        subprocess.run(["make"], cwd=folder_path, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during build process: {e}")
        return

    # Execute the project
    executable_path = os.path.join(folder_path, "project1")
    if os.path.isfile(executable_path):
        try:
            result = subprocess.run([executable_path], capture_output=True, text=True)
            print("Execution Output:")
            print(result.stdout)
            print("Execution Errors:")
            print(result.stderr)
        except Exception as e:
            print(f"Error during execution: {e}")
    else:
        print("Executable not found. Build might have failed.")
