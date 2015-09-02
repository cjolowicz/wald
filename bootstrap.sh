#!/bin/bash

srcdir=$(dirname $0)
tooldir=$srcdir/tools

$tooldir/install-system-requirements.sh
$tooldir/install-python.sh
$tooldir/create-virtualenv.sh
$tooldir/install-pip-tools.sh
$tooldir/install-requirements.sh
$tooldir/generate-readme.sh
