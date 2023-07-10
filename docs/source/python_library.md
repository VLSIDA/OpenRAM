### [Go Back](./index.md#table-of-contents)

# Python Library
This page explains the Python library of OpenRAM.



## Table of Contents
1. [Installation](#installation)
1. [Environment Variables](#environment-variables)
1. [Usage](#usage)



## Installation
OpenRAM is available as a Python library. There are a few ways to install it:

+ Install the latest _stable_ version:
```
pip3 install openram
```

+ Install the latest _dev_ version:
```
pip3 install git+https://git@github.com/VLSIDA/OpenRAM.git@dev
```

+ Install using Makefile (you need to clone the repo):
```
git clone git@github.com:VLSIDA/OpenRAM.git
cd OpenRAM
make library
```



## Environment Variables
OpenRAM library doesn't need any environment variables by default. However, if
you have set the environment variables explained on
[basic usage](.basic_usage.md#go-back), the library will use the OpenRAM source
code located at `OPENRAM_HOME`.

If you want the convenience of being able to run OpenRAM from any Python script
and have a custom OpenRAM setup, you can set these environment variables to
point to that OpenRAM installation directory.

If you don't want to use this feature, you can simply unset these environment
variables.

> **Note**: If you are a developer working on the source code on local clone of
> the repository and want to use the Python library at the same time, you should
> set both `OPENRAM_HOME` and `OPENRAM_TECH` to point to the local clone (follow
> [Basic Setup](./basic_setup.md#go-back)). This way, the library will use the
> source code located at these paths and you won't have to rebuild the library
> after every change.



## Usage
With the OpenRAM library, you can use OpenRAM in any Python script. You can
import "openram" as follows:
```python
import openram
openram.init_openram("myconfig.py") # Config files are explained on "Basic Usage" page
# Now you can use modules from openram
from openram import tech
...
```

Note that you need to initialize OpenRAM so that the modules are imported
properly. You can also look at [sram\_compiler.py](../../sram_compiler.py) as an
example on how to use "openram."

If you want to pass custom configuration when generating an SRAM, you can use
the `sram_config` class.
```python
import openram
openram.init_openram("myconfig.py")

from openram import sram_config
c = sram_config(...)

from openram import sram
s = sram(sram_config=c,
         name="custom_name")

s.save()

openram.end_openram()
```

