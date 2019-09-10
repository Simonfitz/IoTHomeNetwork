sudo apt-get update
sudo apt install libffi-dev libbz2-dev liblzma-dev libsqlite3-dev libncurses5-dev libgdbm-dev zlib1g-dev libreadline-dev libssl-dev tk-dev build-essential libncursesw5-dev libc6-dev openssl git
wget https://github.com/python/cpython/archive/v3.7.2.zip
unzip v3.7.2.zip
cd cpython-3.7*
./configure --prefix=$HOME/.local --enable-optimizations
make -j -l 4
make install
export PATH=$HOME/.local/bin/:$PATH