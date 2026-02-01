# swiftruntimes (ERUN)
The goal of an ERUN is to shrink and rapidly expand its memory usage corresponding to the specific events.
In FaaS, we use it to reduce memory usage when idle and to rapidly reload required libraries when resuming function execution. 

Please check out the paper if interested in the entire design: [https://inria.hal.science/hal-05465369v1](details) accepted at the 24th International Conference on Pervasive Computing and Communications (PerCom 2026). 
## Commands for building eRUN

*dependecies from [https://devguide.python.org/getting-started/setup-building/#build-dependencies](link)*

### Ubuntu/Debian

`sudo apt install build-dep pkg-config build-essential gdb lcov pkg-config libbz2-dev libffi-dev libgdm-dev libgdbm-compat-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev `

### Fedora

`sudo yum install yum-utils`
`sudo yum-builddep python3`

### Build the gc expand/script of the custom cpython

`./configure --prefix=/tmp/python --with-pydebug --with-ensurepip=install`
`make` 

Test the extensible runtime 

`./python -m ensurepip --default-pip`

Check the progression of the memory usage of this program: `watch -n 0.5 pmap -x <pid>` 
```
import boto3
import time
import sys 
gc.mark(sys.modules['boto3'])
time.sleep(0.5)
gc.collect()
```

## Contact 

Djob Mvondo (djobiii2078@gmail / bmvondod@irisa.fr)
