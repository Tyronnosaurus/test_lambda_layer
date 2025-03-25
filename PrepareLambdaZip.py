"""
Prepares zip files with the Lambda Function and the Lambda Layer.
DOES NOT WORK! Since pip compiles it in wichever OS it is run in (and I use Windows), the packages won't work in AWS Lambda (which uses Linux).
See PrepareLambdaZip_Docker.py instead.
"""

import os
import shutil
import subprocess
import tempfile
import zipfile
from colorama import Fore


def prepare_dependencies(temp_dir, requirements_file):
    """
    Installs dependencies in the temp directory.
    As per AWS, packages must be installed inside a directory named "python". See:
        https://stackoverflow.com/a/72454095/17029705
        https://repost.aws/knowledge-center/lambda-import-module-error-python
    """

    print(f"Downloading dependencies specified in {requirements_file}. This might take a few minutes.")
    dir = os.path.join(temp_dir, "python")

    print(Fore.LIGHTBLACK_EX) # Print all pip output in grey
    subprocess.run([
        "pip", "install",
        "--platform", "manylinux2014_x86_64",     # This is the Lambda runtime environment
        "--only-binary=:all:",
        "--target", dir,  # Install packages in '<tmpFolder>/python'
        "--requirement", requirements_file,
    ], check=True)
    print(Fore.RESET) # Reset color


def copy_files(temp_dir, files_to_copy):
    """Copies specific files and folders to the temporary directory."""
    print(f"Copying project files")
    for item in files_to_copy:
        dest_path = os.path.join(temp_dir, os.path.basename(item))
        if os.path.isdir(item):
            shutil.copytree(item, dest_path)
        else:
            shutil.copy(item, dest_path)

def zip_directory(source_dir, zip_name):
    """Creates a ZIP file from the contents of the directory."""
    print(f"Zipping files...")

    if os.path.exists(zip_name):
        print(f"Deleting existing {zip_name}")
        os.remove(zip_name)

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, source_dir))



def main():
    requirements_file = "requirements.txt" # File with the dependencies that should be installed in Lambda Layers
    lambda_files = ["lambda_function.py"]
    output_zip_lambda_layer = "lambda-layer.zip"
    output_zip_lambda_function = "lambda-function.zip"
    
    with tempfile.TemporaryDirectory(delete=True) as temp_dir:
        prepare_dependencies(temp_dir, requirements_file)
        zip_directory(temp_dir, output_zip_lambda_layer)
        print(Fore.GREEN + f"Lambda Layer package created: {output_zip_lambda_layer}" + Fore.RESET)

    with tempfile.TemporaryDirectory(delete=True) as temp_dir:
        copy_files(temp_dir, lambda_files)
        zip_directory(temp_dir, output_zip_lambda_function)
        print(Fore.GREEN + f"Lambda Function package created: {output_zip_lambda_function}" + Fore.RESET)

    print("Temporarily created folders have been cleaned.")



if __name__ == "__main__":
    main()
