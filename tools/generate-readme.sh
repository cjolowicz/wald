#!/bin/bash

pandoc --from=markdown --to=plain --output=README.txt README.md
pandoc --from=markdown --to=rst   --output=README.rst README.md
