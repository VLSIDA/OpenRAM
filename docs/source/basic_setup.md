### [Go Back](./index.md#table-of-contents)

# Basic Setup
This page shows the basic setup for using OpenRAM to generate an SRAM.



## Table of Contents
1. [Dependencies](#dependencies)
1. [Nix](#nix)
1. [Docker](#docker-deprecated-use-nix-instead)
1. [Environment](#environment)
1. [Sky130 Setup](#sky130-setup)



## Dependencies
In general, the OpenRAM compiler has very few dependencies:
+ Git
+ Make
+ Python 3.5 or higher
+ Various Python packages (pip install -r requirements.txt)
+ Nix



## Nix
OpenRAM uses Nix to provide the external toolchain (layout tools, simulators,
etc.) needed for SRAM generation.

Enter the Nix development environment with:
```
nix develop
```

Within the devShell, required executables are available on `PATH`

OpenRAM uses the `use_nix` option (enabled by default) to initialize Nix-based
tool dependencies via `nix develop`.

## Docker (deprecated, use Nix instead)
We have a [docker setup](../../docker) to run OpenRAM. To use this, you should
run:
```
cd OpenRAM/docker
make build
```
This must be run once and will take a while to build all the tools. If you have
the OpenRAM library installed, you can also run the docker setup from the
package installation directory.



## Environment

If you haven't installed the OpenRAM library or you want to use a different
OpenRAM installation, you can set two environment variables:
+ `OPENRAM_HOME` should point to the compiler source directory.
+ `OPENRAM_TECH` should point to one or more root technology directories (colon
  separated).

If you have the library installed and `OPENRAM_HOME` set, the library will use
the installation on the `OPENRAM_HOME` path.

> See [Python library](./python_library.md#go-back) for details.

If you don't have the library, you should also add `OPENRAM_HOME` to your
`PYTHONPATH`. This is not needed if you have the library.

You can add these environment variables to your `.bashrc`:
```
export OPENRAM_HOME="$HOME/OpenRAM/compiler"
export OPENRAM_TECH="$HOME/OpenRAM/technology"
export PYTHONPATH=$OPENRAM_HOME
```

Note that if you want symbols to resolve in your editor, you may also want to
add the specific technology directory that you use and any custom technology
modules as well. For example:
```
export PYTHONPATH="$OPENRAM_HOME:$OPENRAM_TECH/sky130:$OPENRAM_TECH/sky130/custom"
```

We include the tech files necessary for [SCMOS] SCN4M\_SUBM, [FreePDK45]. The
[SCMOS] spice models, however, are generic and should be replaced with foundry
models. You may get the entire [FreePDK45 PDK here][FreePDK45].



## Sky130 Setup

To install [Sky130], you can run:

```
cd $HOME/OpenRAM
make sky130-pdk
```

This will use ciel to get the PDK.

> **Note**: If you don't have Magic installed, enter the OpenRAM Nix devShell
> first (it provides Magic and other tools via `PATH`):
>
> ```
> nix develop
> ```

Then you must also install the [Sky130] SRAM build space with the appropriate
cell views into the OpenRAM technology directory by running:

```
cd $HOME/OpenRAM
make sky130-install
```

You can also run these from the package installation directory if you have the
OpenRAM library.

## GF180 Setup

OpenRAM currently **does not** support gf180mcu for SRAM generation. However ROM generation for gf180mcu is supported as an experimental feature.

To install gf180mcuD, you can run:

```
cd $HOME/OpenRAM
make gf180mcu-pdk
```

[SCMOS]:    https://www.mosis.com/files/scmos/scmos.pdf
[FreePDK45]: https://www.eda.ncsu.edu/wiki/FreePDK45:Contents
[Sky130]:   https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram.git
