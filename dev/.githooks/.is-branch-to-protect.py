#!/usr/bin/python3
import subprocess
import sys

#TODO remove comments from the file
with open(sys.argv[1]) as f:
        branchList=f.read().splitlines()

currentBranch= subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode('utf-8')

if currentBranch in branchList:
    print (1)
else:
    print (0)

