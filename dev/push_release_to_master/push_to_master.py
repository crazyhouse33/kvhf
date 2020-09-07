#!/usr/bin/python3

import os
import sys
import argparse
from subprocess import check_output
sys.path= ['../..']+sys.path
from kvhf import __version__ as version
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
            sys.exit("Aborting release, a problem occured")

def did_you(string):
        inp=input("Did you "+string+"?[y/n]")
        if inp !='y':
            exit("Well do it")

if not args.dry:
    did_you("update the help page")
    did_you("update the templates files if they exist.")
    did_you("change the version number? ")

current_dir=os.getcwd()
#This script assume your test command build everything that need to be rebuilded

root_dir= check_output(['git', 'rev-parse' ,'--show-toplevel']).decode()[:-1]
test_script="run_tests.bash"
test_script_dir=root_dir+"/tests/"

# run test
change_dir(test_script_dir)
threatCommand("./"+test_script)#configuring file and running memory tests

#Commit
change_dir(root_dir)
threatCommand('git commit -a --no-verify -m"Pushing release version {} to master"'.format(version))#commiting the readme and co change
breakpoint()

current_branch = check_output(["git","rev-parse","--abbrev-ref" ,"HEAD"]).decode()[:-1]
header= "{}:\n\n".format(version)
changeLogMessage= header+ args.message

#distribute
change_dir(root_dir+'/dev')
threatCommand("./distribute.bash")

#Commit in master
threatCommand("git checkout master")

threatCommand("git checkout {} -- kvhf tests setup.py .gitignore LICENSE README.md".format(current_branch))

threatCommand('git commit -a -m "'+ changeLogMessage+ '"')



#push and come back to initial branch/dir
if not args.no_push:#Push and back to current
    threatCommand('git push')
    threatCommand('git checkout '+current_branch)
    change_dir(current_dir)


