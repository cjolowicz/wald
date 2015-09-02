#!/bin/bash

tooldir=$(dirname $0)
srcdir=$(dirname $tooldir)

xargs -n1 pyenv install < $srcdir/.python-version
