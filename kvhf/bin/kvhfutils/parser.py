import argparse
import shlex
from kvhf.meta import version

parser = argparse.ArgumentParser(description="kvhfutils is an utility to manipulate kvf files to facilitate automatic integration.")

parser.add_argument('-V','--version', action='version', version=version)

parser.add_argument('files', metavar='FILES',nargs='*',help="The files to manipulate")
parser.add_argument('-o', '--out-path',
                    help='Path of potential output')


parser.add_argument('-s', "--not-interactive", action='store_true',help= "Just fail unstead of letting user input a new label.")


group = parser.add_mutually_exclusive_group()
group.add_argument('-m', '--merge', action='store_true', help= 'Merge FILES vertically and store result in output file')
group.add_argument('-e', '--extend', action='store_true', help= 'Merge FILES horizontally and store result in output file')
group.add_argument('-k', '--keys', action='append',nargs='*',
        help='If the option is alone, list of key=values you want to add to a file. If key allready exist, append values to it. If the option is not alone, specify subset of keys you want to work with.')
group.add_argument('-a', '--actualized', action='store_true',help='Exit status set to 0 if FILES have a different label than in the previous commit. (ie ready to commit) and regeneration of FILES had been done.')

group.add_argument('-g', '--git-extract',  action='store_true',help="""Switch to git extraction mode. 

The FILES argument will be searched in every given git commits and will be merged into one kvhf file representing the whole commit history of the files. If no value is given algromerate every commit of the current branch of the first file given in FILES in order of creation and use other following options to select commits you want to have. If the others options dont fits your need precisely enought, manually precise the wanted commits with commits option. Check documentation about git rev list to to have better controle over what commits you will get, for exemple: 
        kvhutil -g -c $(git rev-list FILE --reverse)  
        To aglomerate only the commits touching FILE in the chronological order. 
        """)


parser.add_argument('-b', "--branchs", help= "Branchs where to get the commits if COMMITS unspecified, can be many branch if space separated")
parser.add_argument('-C', "--commit-filter",nargs='*',action='append', help= "Removes commits that starts by one of the given hash begins")
parser.add_argument('-c', "--commits",action= 'append', metavar='COMMITS', nargs='*', help= "Manually select commits. Doing so desactivate some other filter options.")
parser.add_argument('-p', "--path-restrict",nargs='*', action='append',help= "If COMMITS unspecified, select only commit containing modification on given paths.")
parser.add_argument('--sep-key', type=str,default=':',
                    help='Character separating the key and the values')
parser.add_argument('--sep-val', type=str,default=',',
                    help='Character separating the values')
parser.add_argument('-d', '--dirty', action='store_true', help= 'The current dirty tree will analyzed for extraction if modified')



# Extend action wrapper (extend action is for recent version of python)
def parseMultiOptions(argparseproduct):
    if argparseproduct==None:
        return None
    res = []
    for liste in argparseproduct:
        res.extend(liste)
    return res

def extend_arg(arg, string):
    arg[string]= parseMultiOptions(arg[string])

def getArgs(string=None):  # we allow string for testing purpose
    if string:
        args = parser.parse_args(shlex.split(string))
    else:
        args = parser.parse_args()
    args = vars(args)

    extend_arg(args, 'keys')
    extend_arg(args,'commits')
    extend_arg(args,'commit_filter')
    extend_arg(args,'path_restrict')
    return args


