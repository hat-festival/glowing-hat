## Set a hostname

```bash
sudo raspi-config nonint do_hostname hatlights
sudo raspi-config nonint do_serial 1
```

## Install `git`

```bash
sudo apt -y update && sudo apt install -y git
```

## Get this repo

```bash
git clone https://github.com/hat-festival/hatlights
cd hatlights
```

## Configure everything

```bash
./configure
make
```
