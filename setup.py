# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from setuptools import setup, find_namespace_packages


# Include these folder from the root of repo as submodules
include = ["compiler", "docker", "technology", "macros"]
# Exclude files/folders with these words
exclude = ["docs", "images", "miniconda"]


# Find all modules inside the 'compiler' folder
dirs = []
for dir in find_namespace_packages():
    if any(x in dir for x in exclude):
        continue
    dirs.append(dir)

# Replace 'compiler' with 'openram' for package names
packages = []
for dir in dirs:
    packages.append(dir)

# Make the included folders submodules of openram package
for i in range(len(packages)):
    if any(x in packages[i] for x in include):
        packages[i] = "openram." + packages[i]

# Fix directory paths
for i in range(len(dirs)):
    dirs[i] = dirs[i].replace(".", "/")

# Insert the root as the openram module
packages.insert(0, "openram")
dirs.insert(0, "")

# Zip package names and their paths
package_dir = {k: v for k, v in zip(packages, dirs)}


# Create a list of required packages
with open("requirements.txt") as f:
    reqs = f.read().splitlines()


# Read version from file
version = open("VERSION", "r").read().rstrip()


with open("README.md") as f:
    long_description = f.read()


# Call the setup to create the package
setup(
    name="openram",
    version=version,
    description="An open-source static random access memory (SRAM) compiler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://openram.org/",
    download_url="https://github.com/VLSIDA/OpenRAM/releases",
    project_urls={
        "Bug Tracker": "https://github.com/VLSIDA/OpenRAM/issues",
        "Documentation": "https://github.com/VLSIDA/OpenRAM/blob/stable/docs/source/index.md",
        "Source Code": "https://github.com/VLSIDA/OpenRAM",
    },
    author="Matthew Guthaus",
    author_email="mrg+vlsida@ucsc.edu",
    keywords=[ "sram", "magic", "gds", "netgen", "ngspice", "netlist" ],
    license="BSD 3-Clause",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: System :: Hardware",
    ],
    packages=packages,
    package_dir=package_dir,
    include_package_data=True,
    install_requires=reqs,
)
