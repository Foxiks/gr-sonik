# gr-sonik
OOT GnuRadio blocks for working in the SONIK network

### Install Dependencies
1. gr-Satellites: https://github.com/daniestevez/gr-satellites
and
```
python3 -m pip install websocket crc ephem construct, pydub, wave
```

### Installation
```
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
```
