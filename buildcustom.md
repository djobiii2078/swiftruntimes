# Commands for building eRUN

# dependecies from https://devguide.python.org/getting-started/setup-building/#build-dependencies

# Ubuntu/Debian

`sudo apt install build-dep pkg-config build-essential gdb lcov pkg-config libbz2-dev libffi-dev libgdm-dev libgdbm-compat-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev `

# Fedora

sudo yum install yum-utils
sudo yum-builddep python3

./configure --prefix=/tmp/python --with-pydebug --with-ensurepip=install 
make 
./python -m ensurepip --default-pip 
