#/usr/bin/env bash

# AINNetwork cannot be run under pypy3, because it uses theano and numpy
python3 ./src/compareEvolution1.py $@
