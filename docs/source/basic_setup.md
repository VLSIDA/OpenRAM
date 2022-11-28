### [Go Back](./index.md#table-of-contents)

# Basic Setup
This page shows the basic setup for using OpenRAM.



## Table of Contents
1. [Dependencies](#dependencies)
1. [OpenRAM Library](#openram-library)
1. [Docker](#docker)
1. [Environment](#environment)
1. [Sky130 Setup](#sky130-setup)



## Dependencies
Please see the Dockerfile for the required versions of tools.

In general, the OpenRAM compiler has very few dependencies:
+ Docker
+ Make
+ Python 3.6 or higher
+ Various Python packages (pip install -r requirements.txt)
+ Git



## OpenRAM Library
OpenRAM is available as a Python library. There are a few ways to install it:

+ Install using Makefile (you need to clone the repo):
```
git clone git@github.com:VLSIDA/OpenRAM.git
cd OpenRAM
make library
```

+ Install the latest _dev_ version:
```
pip3 install git+ssh://git@github.com/VLSIDA/OpenRAM.git@dev
```


## Docker
We have a [docker setup](../../docker) to run OpenRAM. To use this, you should run:
```
cd OpenRAM/docker
make build
```
This must be run once and will take a while to build all the tools. If you have the
OpenRAM library installed, you can also run the docker setup from the package
installation directory.



## Environment

If you haven't installed the OpenRAM library or you want to use a different OpenRAM installation,
you can set two environment variables:
+ OPENRAM\_HOME should point to the compiler source directory.
+ OPENRAM\_TECH should point to one or more root technology directories (colon separated).

If you have the library installed and OPENRAM\_HOME set, the library will use the installation on
the OPENRAM\_HOME path.

If you don't have the library, you should also add OPENRAM\_HOME to your PYTHONPATH. This is not
needed if you have the library.

You can add these environment variables to your `.bashrc`:
```
  export OPENRAM_HOME="$HOME/OpenRAM/compiler"
  export OPENRAM_TECH="$HOME/OpenRAM/technology"
  export PYTHONPATH=$OPENRAM_HOME
```

Note that if you want symbols to resolve in your editor, you may also want to add the specific technology
directory that you use and any custom technology modules as well. For example:
```
  export PYTHONPATH="$OPENRAM_HOME:$OPENRAM_TECH/sky130:$OPENRAM_TECH/sky130/custom"
```

We include the tech files necessary for [SCMOS] SCN4M\_SUBM,
[FreePDK45]. The [SCMOS] spice models, however, are
generic and should be replaced with foundry models. You may get the
entire [FreePDK45 PDK here][FreePDK45].



### Sky130 Setup

To install [Sky130], you must have the open\_pdks files installed in $PDK\_ROOT. 
To install this automatically, you can run:
```
cd $HOME/OpenRAM
make pdk
```

Then you must also install the [Sky130] SRAM build space and the appropriate cell views
by running:
```
cd $HOME/OpenRAM
make install
```

You can also run these from the package installation directory if you have the OpenRAM library.



[SCMOS]:    https://www.mosis.com/files/scmos/scmos.pdf
[FreePDK45]: https://www.eda.ncsu.edu/wiki/FreePDK45:Contents
[Sky130]:   https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram.git
