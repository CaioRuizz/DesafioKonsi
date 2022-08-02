#!/bin/bash

. ../../setup_env.sh

python3 -m unittest discover -s tests -p '*_test.py'