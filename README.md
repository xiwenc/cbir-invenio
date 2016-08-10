
Installation
==

download opencv-2.4.8
```bash
cmake -D CMAKE_INSTALL_PREFIX=/home/xcheng/apps/opencv ../

export PYTHONPATH=~/apps/opencv/lib/python2.7/dist-packages
export DYLD_LIBRARY_PATH=~/apps/opencv/lib
```

Third parties
===
```bash
apt-get liblapack-dev gfortran

apt-get build-dep python-gtk2
wget http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.24/pygtk-2.24.0.tar.bz2
tar xf pygtk-2.24.0.tar.bz2
cd pygtk-2.24.0
./configure --prefix=/home/xcheng/.virtualenvs/invenio/lib/python2.7
make
make install

apt-get build-dep python-gobject-2
cd ../
wget http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.10/pygobject-3.10.2.tar.xz
tar xf pygobject-3.10.2.tar.xz
cd pygobject-3.10.2
```
