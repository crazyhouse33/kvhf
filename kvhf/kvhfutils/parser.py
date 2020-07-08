import argparse
import shlex
from setup import version

parser = argparse.ArgumentParser("kvhfutils is done to manipulate kvf files to facilitate automatic integration to plot interesting metrics about your project across commits")

parser.add_argument('-V','--version', action='version', version=version)

parser.add_argument('file', metavar='FILE', help="The file to manipulate")

parser.add_argument('-k', '--add-key', action='append', nargs='*',
                    help='List of key=values you want to add to a file. If key allready exist, append values to it. ')

parser.add_argument('-d', '--git-diff', action='store_true',
                    help='Exit status set to 0 if the file have a different label than the previous one. (ie probably it\'s actualized and ready to commit).')
parser.add_argument('--sep-values', type=str,
                    help='Character separating the the values (default ",")')

def getArgs(string=None):  # we allow string for testing purpose
    if string:
        args = parser.parse_args(shlex.split(string))
    else:
        args = parser.parse_args()
    args = vars(args)
    return args


