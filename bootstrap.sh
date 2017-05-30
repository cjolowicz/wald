#!/bin/bash

srcdir=$(dirname $0)
tooldir=$srcdir/tools
scripts=(
    install-pyenv
    install-homebrew
    install-pandoc
    install-python
    create-virtualenv
    install-pip-tools
    install-requirements
    generate-readme
)

for script in ${scripts[@]}; do
    $tooldir/$script.sh
done
