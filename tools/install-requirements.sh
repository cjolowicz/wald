#!/bin/bash

pip-compile requirements.in
pip-compile dev-requirements.in
pip-sync *requirements.txt
