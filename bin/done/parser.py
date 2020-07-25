import argparse
import shlex
import os
from meta import version

parser = argparse.ArgumentParser(description="done is an utility to ensure some action had been done at least / exactely once. It aims at integrating himself easely into buil systems.", epilog="""

STDOUT:
Nothing if CMD had not been lunch. 
Otherwise correspond to the stdout of CMD appended by: "CMD Exit status: $ret"


EXIT STATUS:
0 everything went fine or no-crash
1 if failed because of the check phase (ie command was not lunched)
2 if failed because CMD exit status was not NULL and no child permissive flag
        """)
parser.add_argument('-V','--version', action='version', version=version)

parser.add_argument('-f', '--done-dir-path', help='Use given done directory path. By default look for a .done directory in current working directory and then going up the directory parents.')


subparsers = parser.add_subparsers(help='sub-command help', dest='mode')

parser_exec = subparsers.add_parser('exec', help='Run CMD if required actions are marked, produced and not locked. Then mark produced action and lock given actions if CMD exit normally.')

parser_exec.add_argument('command', metavar='CMD',nargs='?',default="",help="The command to execute")
parser_exec.add_argument('-r', '--required-action', metavar='ACTION_NAME',action='append',default=[], help='Will fail before execution if the given actions are not marked as done.')
parser_exec.add_argument('-p', '--produced-action', metavar='ACTION_NAME',action='append', default=[],help='Will mark theses actions as marked after sucessfull execution.')

parser_exec.add_argument('-l', '--lock-action', action='append',default=[], help='Given actions will be locked after a success, meaning next execution will fail. If no actions is given, this will feed the option with the given produced action.')
parser_exec.add_argument('-a', '--lock-products', action='store_true',default=[], help='Append produced actions to the action to be locked')

parser_exec.add_argument('--child-permissive',action='store_true', help='If the flag is activated, a non zero exit status for the child is not considered as a fail')

parser_exec.add_argument('--required-permissive',action='store_true', help='If the flag is activated, an action not passing checks because some actions are not marked is not considered as a fail')
parser_exec.add_argument('--lock-no-fail', action='store_true', help='If the flag is activated, an action not passing checks because allready marked is considered as a fail')


parser_exec = subparsers.add_parser('init', help='Create an empty done directory at given path (f option)')



def getArgs(string=None):  # we allow string for testing purpose
    if string:
        args = parser.parse_args(shlex.split(string))
    else:
        args = parser.parse_args()
    args = vars(args)
    return args
