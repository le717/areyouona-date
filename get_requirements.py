import json
import sys


def get_packages(package_root):
    for package in package_root.keys():
        yield f"{package}{package_root[package]['version']}"


# Does the user want to include the dev-pacakegs?
try:
    dev_packages = sys.argv[1].upper() == "DEV"
except IndexError:
    dev_packages = False

# Parse the pipenv lock file
with open("Pipfile.lock", "rt") as f:
    lock_file = json.load(f)

# Go ahead and open the requirements file for writing
with open("requirements.txt", "wt") as f:
    # Get the standard packages
    for package in get_packages(lock_file["default"]):
        f.write(f"{package}\n")

    # Write the dev packages if requested
    if dev_packages:
        for package in get_packages(lock_file["develop"]):
            f.write(f"{package}\n")
