#!/bin/bash

srcdir=$(dirname $(dirname $0))

xargs -n1 pyenv install < $srcdir/.python-version
