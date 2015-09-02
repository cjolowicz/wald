#!/bin/bash

case $(uname) in Darwin)
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew install python
    brew install pyenv
    brew install pyenv-virtualenv
    brew install pandoc
    ;;
esac

pyenv install 3.3.6
pyenv virtualenv 3.3.6 wald
pyenv local wald
pip install --upgrade pip
pip install pip-tools
pip-compile requirements.in
pip-compile dev-requirements.in
pip-sync requirements.txt dev-requirements.txt
./convert-readme.sh
