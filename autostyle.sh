#!/bin/bash

function doLibrary {
    autopep8 $1 > $1.changed
    mv $1.changed $1
}

function doExecutable {
    doLibrary $1
    chmod +x $1
}

doExecutable ./src/main.py
doExecutable ./src/scenarioEvolution1.py
doExecutable ./src/compareEvolution1.py
doExecutable ./src/tests.py
doExecutable ./src/convertAIData.py
doExecutable ./src/nNetworkTest1.py
doExecutable ./src/nNetworkTest2.py

doLibrary ./src/controller.py
doLibrary ./src/controllerSimpleEvolution1.py
doLibrary ./src/rules.py
doLibrary ./src/minimax.py
doLibrary ./src/controllerEvolution2.py
doLibrary ./src/StateGenerator.py
doLibrary ./src/nNetwork.py
# currently display.py is excluded
