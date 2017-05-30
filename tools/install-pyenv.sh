#!/bin/bash

case $(uname) in Darwin)
    url=https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer
    curl -L $url | bash
esac
