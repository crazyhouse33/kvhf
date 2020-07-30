import argparse
import shlex
from kvhf.meta import version

parser = argparse.ArgumentParser("kvhfplot is an utility to generate graphs from kvhf files.")

parser.add_argument('-V','--version', action='version', version=version)

parser.add_argument('file', metavar='FILES',nargs='+',help="The files to plot, if more that one given operate on the concatenation of them")

parser.add_argument('-k', '--keys', action='append', default=[],
                    help='List of regexps. If a key match one of the regexp, it \'s plotted unless matched by a filter. If not provided every key is ploted')


parser.add_argument('-l', '--labels', action='append',default=[],
                    help='List of regexp. If a label match one of the regexps, it\'s plotted unless matched by a filter. If not provided every label is ploted')

parser.add_argument('-L', '--labels_filter', action='append',default=[],
                    help='List of regexp. If a label match one of the regexps, it wont be plotted ')

parser.add_argument('-K', '--keys-filter', action='append', default=[],
                    help='List of regexps. If a key match one of the regexp, it wont be plotted')
parser.add_argument('--sep-key', type=str,default=':',
                    help='Character separating the key and the values')
parser.add_argument('--sep-val', type=str,default=',',
                    help='Character separating the values')

parser.add_argument("--void-char", type=str, default='_', help= "Character signifying that a value is unknown")
parser.add_argument('-u', '--unity', action='append', nargs='*',default=[],
                    help='List of regexps. Keys that dont have an unity matching one of the regexps wont be ploted.')

parser.add_argument('-o', '--out-path',
                    help='Path of the created image. If none plot the image without saving it.')

parser.add_argument('-p', '--plot',
                    help='Plot image even if you precise an output file as well')

parser.add_argument('-f', '--out-format',
                    help='Format of the created image')

parser.add_argument('-y', '--y-label',
                    help='Legend ploted on graph to comment y axis')

parser.add_argument('-t', '--title',default='',
                    help='Title in the graph')










def getArgs(string=None):  # we allow string for testing purpose
    if string:
        args = parser.parse_args(shlex.split(string))
    else:
        args = parser.parse_args()
    args = vars(args)

    
    parsedUnity = parseMultiOptions(args['unity'])
    args['unity'] = parsedUnity
    return args


# Extend action wrapper (extend action is for recent version of python)
def parseMultiOptions(argparseproduct):
    if argparseproduct==None:
        return []
    res = []
    for liste in argparseproduct:
        res.extend(liste)
    return res
