#/usr/bin/env bash

# AIEvolution3 cannot be run under pypy3, because it uses theano and numpy
python3 ./src/compareEvolution1.py $@
