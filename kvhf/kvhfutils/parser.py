import argparse
import shlex
from meta import version

parser = argparse.ArgumentParser("kvhfutils is done to manipulate kvf files to facilitate automatic integration with git to plot interesting metrics about your project across commits")

parser.add_argument('-V','--version', action='version', version=version)

parser.add_argument('files', metavar='FILES', help="The files to manipulate")
parser.add_argument('-o', '--out-path',
                    help='Path of potential output')

group = parser.add_mutually_exclusive_group()
group.add_argument('-m', '--merge', action='store_true', help= 'Merge FILES vertically and store result in output file')
group.add_argument('-e', '--extend_history', action='store_true', help= 'Merge FILES horizontally and store result in output file')
group.add_argument('-k', '--keys', action='append', nargs='*',
        help='If the option is alone, list of key=values you want to add to a file. If key allready exist, append values to it. If the option is not alone, specify subset of keys you want to work with.')
group.add_argument('-a', '--git-actualized-label', action='store_true',
                    help='Exit status set to 0 if FILES have a different label than in the previous commit. (ie ready to commit).')

group.add_argument('-g', '--git-extract', metavar="COMMITS" action= 'append',nargs='*', help="""Switch to git extraction mode. The FILES argument will be searched in every given git commits and will be merged into one kvhf file representing the whole commit history of the files, for further manipulation of your choice. If no value is given algromerate every commit of the current branch of the first file given in FILES in order of creation. See git rev list to see how to have better controle over what commits you will get, for exemple: 
        kvhutil -g $(git rev-list FILE --reverse)  
        to aglomerate only the commits touching FILE in the chronological order.
        """)
def getArgs(string=None):  # we allow string for testing purpose
    if string:
        args = parser.parse_args(shlex.split(string))
    else:
        args = parser.parse_args()
    args = vars(args)
    return args


