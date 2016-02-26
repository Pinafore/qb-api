#!/usr/bin/env bash

python run.py &
sleep 1
nosetests test
