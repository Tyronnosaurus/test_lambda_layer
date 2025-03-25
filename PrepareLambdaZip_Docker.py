"""
Prepares zip files with the Lambda Function and the Lambda Layer.
Uses a Docker Linux container to compile the python dependencies, so that they're compatible with the AWS Lambda Linux environment.
Make sure Docker is installed and running before executing this script.
"""

import os
import subprocess
import shutil
import zipfile

#####################
## LAMBDA FUNCTION ##
#####################
ZIP_FILE = "lambda-function.zip"

# Delete zip if already exists
if os.path.exists(ZIP_FILE):
    print(f"Deleting existing {ZIP_FILE}")
    os.remove(ZIP_FILE)

# Zip necessary file(s)
zipfile.ZipFile(ZIP_FILE, "w", zipfile.ZIP_DEFLATED).write("lambda_function.py")


##################
## LAMBDA LAYER ##
##################
CONTAINER_NAME = "python-container"
IMAGE = "public.ecr.aws/sam/build-python3.11:1.135.0-20250310201004" # Image that closely resembles the Lambda environment. https://gallery.ecr.aws/sam/build-python3.11
ZIP_FILE = "lambda-layer.zip"
PYTHON_DIR = "python"    # In Lambda Layers, packages must go in a folder called 'python'

# Create 'python' folder
if os.path.exists(PYTHON_DIR):
    shutil.rmtree(PYTHON_DIR)
os.mkdir(PYTHON_DIR)

# Run the temporary container.
# Mounts current folder as a volume, and installs packages in 'python' folder so that we can zip them afterwards
subprocess.run([
    "docker", "run", "--rm", "-v", f"{os.getcwd()}:/app", 
    "-w", "/app", "--name", CONTAINER_NAME, IMAGE, 
    "bash", "-c", 
    f"pip install --platform manylinux2014_x86_64 --only-binary=:all: --target {PYTHON_DIR} -r requirements.txt"
], check=True)


# Delete zip if already exists
if os.path.exists(ZIP_FILE):
    print(f"Deleting existing {ZIP_FILE}")
    os.remove(ZIP_FILE)

# Zip the python folder
if os.path.exists("python"):
    shutil.make_archive(os.path.splitext(ZIP_FILE)[0], 'zip', root_dir=".", base_dir="python")
    print(f"Zipped {PYTHON_DIR} to {ZIP_FILE}")
else:
    print(f"Error: {PYTHON_DIR} directory not found")


# Clean up
shutil.rmtree("python")




