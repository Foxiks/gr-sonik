# gr-soniks
OOT GnuRadio blocks for working in the SONIKS network

### Install Dependencies
1. gr-Satellites: https://github.com/daniestevez/gr-satellites
2. FFMpeg: https://github.com/FFmpeg/FFmpeg
3. ```sudo apt-get install gcc build-essentia libffi-dev python3-dev python3-cffi python3-opencv python3-pip git cmake libusb-1.0-0-dev libboost-all-dev gnuradio-dev liblog4cpp5-dev swig```
4. ``` python3 -m pip install websocket crc ephem construct pydub wave```

### Installation
```
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
```
