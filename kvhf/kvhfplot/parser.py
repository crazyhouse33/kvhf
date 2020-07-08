import argparse
from template.handler.handler import Handler
import shlex
from setup import version

parser = argparse.ArgumentParser("kvhfplot is done to plot kvhf files. It's support git agregation")

parser.add_argument('-V','--version', action='version', version=version)

parser.add_argument('file', metavar='FILE', help="The file to plot")


parser.add_argument('-C', '--commits', action='append', nargs='*',
                    help='List of commits hash you want to plot. This desactivate any kind of commit filtering')

parser.add_argument('-c', '--commits-filter', action='append', nargs='*',
                    help='List of commits hash that wont be ploted. If not provided every commit is checked')

parser.add_argument('-K', '--keys', action='append', nargs='*',
                    help='list of keys you want to plot. If not provided every key is ploted')

parser.add_argument('-k', '--keys-filter', action='append', nargs='*',
                    help='list of keys that wont be ploted.')

parser.add_argument('--sep-key', type=str,
                    help='Character separating the key and the values')

parser.add_argument(
    "-g", "--git", action='store_true', help="Plot the history of the given kvf file")
parser.add_argument("-d", "--debug", action='store_true',


def getArgs(string=None):  # we allow string for testing purpose
    if string:
        args = parser.parse_args(shlex.split(string))
    else:
        args = parser.parse_args()
    args = vars(args)

    parsedCommits = parseMultiOptions(args['commits'])
    args['commits'] = parsedCons
    parsedKeys = parseMultiOptions(args['commits'])
    args['keys'] = parsedKeys
    return args


# Correcting argparse stuff
def parseMultiOptions(argparseproduct):
    res = []
    for liste in argparseproduct:
        res.extend(liste)
    return res
