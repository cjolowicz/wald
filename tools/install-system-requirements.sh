#!/bin/bash

case $(uname) in Darwin)
    url=https://raw.githubusercontent.com/Homebrew/install/master/install
    ruby -e "$(curl -fsSL $url)"

    brew install pyenv pyenv-virtualenv pyenv-which-ext
    brew install pandoc
esac
