# pip install --platform manylinux2014_x86_64 --only-binary=:all: --target python python-can[mf4] colorama

import os
import subprocess
import shutil

CONTAINER_NAME = "python-container"
IMAGE = "python:3.9-slim"
PYTHON_DIR = "python"
ZIP_FILE = "python.zip"

# Run the container
subprocess.run([
    "docker", "run", "--rm", "-v", f"{os.getcwd()}:/app", 
    "-w", "/app", "--name", CONTAINER_NAME, IMAGE, 
    "bash", "-c", 
    "pip install --platform manylinux2014_x86_64 --only-binary=:all: --target python python-can[mf4] colorama"
], check=True)

# Zip the python folder
if os.path.exists(PYTHON_DIR):
    shutil.make_archive(PYTHON_DIR, 'zip', PYTHON_DIR)
    print(f"Zipped {PYTHON_DIR} to {ZIP_FILE}")
else:
    print(f"Error: {PYTHON_DIR} directory not found")
