import os
import re
import sys

def convert_to_conda_env():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the path to requirements.txt relative to the script's location
    requirements_path = os.path.join(script_dir, '../../requirements.txt')

    # Read the requirements.txt file
    with open(requirements_path, 'r') as req_file:
        lines = req_file.readlines()

    dependencies = []
    i = 0
    env_name = None
    while i < len(lines):
        line = lines[i].strip()
        # Check if the line is not a comment and contains a dependency
        if line and not line.startswith('#'):
            # Check subsequent lines for comments with "(pyproject.toml)"
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith('#'):
                if '(pyproject.toml)' in lines[j]:
                    # Add dependency to the list
                    dependencies.append(line)
                    if env_name is None:
                        # # Extract the environment name before "(pyproject.toml)"
                        match = re.search(r'(\w+)\s+\(pyproject\.toml\)', lines[j])
                        if match:
                            env_name = match.group(1)  
                j += 1
        i += 1

    # Write the environment.yml file
    output_file = os.path.join(script_dir, '../../environment.yml')
    with open(output_file, 'w') as env_file:
        env_file.write(f"name: {'my_env' if env_name is None else env_name}\n")
        env_file.write("dependencies:\n")
        env_file.write(f"  - python={sys.version_info.major}.{sys.version_info.minor}\n")  # Include Python as a dependency
        for dep in dependencies:
            env_file.write(f"  - {dep}\n")

# Convert requirements.txt to environment.yml
convert_to_conda_env()