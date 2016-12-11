#!/bin/bash

function doLibrary {
    autopep8 $1 > $1.changed
    mv $1.changed $1
}

function doExecutable {
    doLibrary $1
    chmod +x $1
}

doExecutable main.py
doExecutable scenarioEvolution1.py
doExecutable compareEvolution1.py

doLibrary controller.py
doLibrary controllerSimpleEvolution1.py
doLibrary rules.py
doLibrary minimax.py
# currently display.py is excluded
