# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from setuptools import setup, find_namespace_packages


# Include these folder from the root of repo as submodules
include = ["docker", "technology"]
# Exclude files/folders with these words
exclude = ["docs", "images", "macros"]


# Find all modules inside the 'compiler' folder
dirs = []
for dir in find_namespace_packages():
    if any(x in dir for x in exclude):
        continue
    dirs.append(dir)

# Replace 'compiler' with 'openram' for package names
packages = []
for dir in dirs:
    packages += [dir.replace("compiler", "openram")]

# Make the included folders submodules of openram package
for i in range(len(packages)):
    if any(x in packages[i] for x in include):
        packages[i] = "openram." + packages[i]

# Fix directory paths
for i in range(len(dirs)):
    dirs[i] = dirs[i].replace(".", "/")

# Zip package names and their paths
package_dir = {k: v for k, v in zip(packages, dirs)}


# Create a list of required packages
with open("requirements.txt") as f:
    reqs = f.read().splitlines()


# Call the setup to create the package
setup(
    packages=packages,
    package_dir=package_dir,
    include_package_data=True,
    install_requires=reqs,
)