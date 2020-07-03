#!/usr/bin/python3

import os
import sys
import argparse
from subprocess import check_output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser(description='Put a new realease on master, copying the current state of dev')
parser.add_argument("message", metavar='CHANGELOG_BODY',type=str, help='Body of the changelog message. Dont put any kind of header.')

parser.add_argument('--dry','-d',action='store_true', help='Show everything that will be executed unstead of executing')
parser.add_argument('--no-test','-f',action='store_true', help='Dont run test')

parser.add_argument('--no-push','-n',action='store_true', help='Dont push to remote')
args = parser.parse_args()

def change_dir(directory):
    print (bcolors.BOLD,"going to", directory,bcolors.ENDC)
    os.chdir(directory)


def threatCommand(command):
    print(bcolors.BOLD,command,bcolors.ENDC)
    if not args.dry:
        if os.system(command) !=0:
            sys.exit("Aborting release, a problem occured with git")

def did_you(string):
        inp=input("Did you "+string+"?[y/n]")
        if inp !='y':
            exit("Well do it")

if not args.dry:
    did_you("update authbreak help page (interface/cliparser.c)")
    did_you("update authbreak TEMPLATE readme (dev/push_release_to_master/push_to_master.py.cmake_template)")
    did_you("change the version number (CMakeLists.txt")

current_dir=os.getcwd()
build_dir= "/opt/handCraftedUtilityShit/authbreak/build"
root_dir="/opt/handCraftedUtilityShit/authbreak"

change_dir(build_dir)
threatCommand("cmake --build . --target full-test")#configuring file and running memory tests
change_dir(root_dir)
threatCommand('git commit -a -m"Pushing release version 0.6 to master"')#commiting the readme and co change

current_branch = check_output(["git","rev-parse","--abbrev-ref" ,"HEAD"]).decode("utf8")[:-1]
header= "Authbreak 0.6 :\n\n"
changeLogMessage= header+ args.message

threatCommand("git checkout master")

threatCommand("git checkout dev -- src tests build build-helpers CMakeLists.txt extern .gitignore LICENSE README.md")

change_dir(root_dir)
threatCommand('git commit -a -m "'+ changeLogMessage+ '"')

if not args.no_push:#Push and back to current
    threatCommand('git push')
    threatCommand('git checkout '+current_branch)
    change_dir(current_dir)

