#!/bin/bash

srcdir=$(dirname $(dirname $0))

env PYTHON_CONFIGURE_OPTS="--enable-framework" \
    xargs -n1 pyenv install < $srcdir/.python-version
