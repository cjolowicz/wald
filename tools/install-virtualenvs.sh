#!/bin/bash

versions=(
    3.4.3
    3.3.6
    2.7.10
)

for version in ${versions[@]} ; do
    virtualenv=wald-py${version%.*}

    pyenv install $version
    pyenv virtualenv $version $virtualenv
done
