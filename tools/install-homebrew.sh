#!/bin/bash

case $(uname) in Darwin)
    url=https://raw.githubusercontent.com/Homebrew/install/master/install
    ruby -e "$(curl -fsSL $url)"
    ;;
esac
