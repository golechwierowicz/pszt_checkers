#!/bin/bash
name="main.py"
autopep8 $name > $name.changed
mv $name.changed $name
chmod +x $name

name="controller.py"
autopep8 $name > $name.changed
mv $name.changed $name

name="rules.py"
autopep8 $name > $name.changed
mv $name.changed $name
