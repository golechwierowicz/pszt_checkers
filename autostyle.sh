#!/bin/bash
autopep8 main.py > main.py.changed
mv main.py.changed main.py
chmod +x main.py
