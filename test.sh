#!/bin/bash

# this scripts launching from run.sh
echo python corstest.py -q -n $1 -parts $2 $3
python corstest.py -q -n $1 -parts $2 $3