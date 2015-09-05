#!/bin/bash

case $(uname) in Darwin)
    url=https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer
    curl -L $url | bash

    url=https://raw.githubusercontent.com/Homebrew/install/master/install
    ruby -e "$(curl -fsSL $url)"

    brew install pandoc
esac
