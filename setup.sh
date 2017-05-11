#!/usr/bin/env bash

apt-get install -y psmisc python python-pip python-dev libboost-all-dev

pip install subprocess32 gradescope-utils

(cd /autograder/source/reference-implementation; make)

(git clone https://github.com/cawka/gradescope-utils /root/utils; cd /root/utils; python setup.py install)
