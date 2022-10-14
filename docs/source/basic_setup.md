### [Go Back](./index.md#directory)

This page shows the basic setup for using OpenRAM.

# Basic Setup

## Dependencies

Please see the Dockerfile for the required versions of tools.

In general, the OpenRAM compiler has very few dependencies:
+ Docker
+ Make
+ Python 3.6 or higher
+ Various Python packages (pip install -r requirements.txt)
+ [Git]

## Docker

We have a [docker setup](./docker) to run OpenRAM. To use this, you should run:
```
cd OpenRAM/docker
make build
```
This must be run once and will take a while to build all the tools.


## Environment

You must set two environment variables:
+ OPENRAM\_HOME should point to the compiler source directory.
+ OPENERAM\_TECH should point to one or more root technology directories (colon separated).

You should also add OPENRAM\_HOME to your PYTHONPATH.

For example add this to your .bashrc:

```
  export OPENRAM_HOME="$HOME/OpenRAM/compiler"
  export OPENRAM_TECH="$HOME/OpenRAM/technology"
```

You should also add OPENRAM\_HOME to your PYTHONPATH:
```
  export PYTHONPATH=$OPENRAM_HOME
```

Note that if you want symbols to resolve in your editor, you may also want to add the specific technology
directory that you use and any custom technology modules as well. For example:
```
  export PYTHONPATH="$OPENRAM_HOME:$OPENRAM_TECH/sky130:$OPENRAM_TECH/sky130/custom"
```

We include the tech files necessary for [SCMOS] SCN4M_SUBM,
[FreePDK45]. The [SCMOS] spice models, however, are
generic and should be replaced with foundry models. You may get the
entire [FreePDK45 PDK here][FreePDK45].


### Sky130 Setup

To install [Sky130], you must have the open_pdks files installed in $PDK_ROOT. 
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
