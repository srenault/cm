# cm tools

## Setup python on debian

### Requirements

```bash
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev
sudo apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm 
sudo apt-get install -y libncurses5-dev  libncursesw5-dev xz-utils tk-dev
```

### Setup

```shell
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.x.tgz
tar xvf Python-3.6.x.tgz
cd Python-3.x.3
./configure --enable-optimizations --with-ensurepip=install
make -j8
sudo make altinstall
python3.6
```
You can define different python with priority:

```shell
update-alternatives --install /usr/bin/python python /usr/local/bin/python3.7 50
update-alternatives --install /usr/bin/python python /usr/bin/python2.7 40
update-alternatives --install /usr/bin/python python /usr/bin/python3.5 30
```

You can set the default python using:

```shell
update-alternatives --config python
```

## Setup pipenv
```shell
pip install --user pipenv
```

## Setup cm tools

```shell
cd cm
python setup.py install

cd tools
pipenv install
pipenv install -e ../
```
