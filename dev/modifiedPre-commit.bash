#!/bin/bash
#This script is gonna be lanched on all modifed file by git, file path as command argument. If this script return a non zero status code, commit dont pass


listDeco='  *'

if [[ $1 == *.c ]] 
then
	echo "$listDeco" linting $1 
	clang-format $1 -style="{BasedOnStyle: llvm, ColumnLimit: 200}" -i
fi

