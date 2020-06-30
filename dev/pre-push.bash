#!/bin/bash
set -e
#Run test
cd ../build
rm -rf -- *
cmake ..
make all
make lazy-test
