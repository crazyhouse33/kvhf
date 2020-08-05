#!/bin/bash


if [ -z "$1" ];then
	to_test=".."
else
	to_test="$*"
fi
bash -c "cd test_work_dir; PYTHONPATH=../.. python3 -m pytest -x ../$to_test"
