#!/bin/bash

case $(uname) in Darwin)
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew install pyenv
    brew install pyenv-virtualenv
    brew install pyenv-which-ext
    brew install pandoc
esac
