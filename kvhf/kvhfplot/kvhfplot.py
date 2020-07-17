#!usr/bin/python3
import parser
from kvhf.file import KVH_file
import re

def select_keys(kvh_file, keys, keys_filter, unity):
    """Given a list of regexp string of wanted keys, unwanted key, an wanted unity, retrieve list of matching keys in a kvhf file"""

    keys_reg= list(map(re.compile,keys))
    keys_filter_reg= list(map(re.compile, keys_filter))
    unity_reg= list(map(re.compile,unity))
    return [key for key in kvh_file.dico.keys() if 
        (any(regex.match(key) for regex in keys_reg) or not keys) and 
        not any(regex.match(key) for regex in keys_filter_reg) and 
        (any(regex.match(kvh_file.dico[key].unity) for regex in unity_reg) or not unity)
        ]

def select_pos(kvh_file, labels, labels_filter):
    """Given a list of wanted label regexp string , and a list of unwanted one, return necessary indexs to match requirement"""
    labels_reg= map(re.compile,labels)
    labels_filter_reg= map(re.compile,labels_filter)
    return [i for i in range(len(kvh_file.labels)) if (any(regex.match(kvh_file.labels[i]) for regex in labels_reg) or not labels) and
        not any(regex.match(kvh_file.labels[i]) for regex in labels_filter_reg)
        ]
#We need to import the module for testing the two upper functions
if __name__ == "__main__":
#import bcolors
#def get_git_file(path,commit):
#    print("Recolting commit ", bcolors.BOLD,commit.hexsha,":", commit.message, bcolors.ENDC)
#    f = commit.tree / path 
#    return f.data_stream

    args= parser.getArgs()

    paths= args["file"]
    sep_key = args["sep_key"] 
    sep_val=args["sep_val"]
    keys=args["keys"]
    keys_filter= args["keys_filter"]
    labels = args["labels"]
    labels_filter=args["labels_filter"]
    ylabel = args["y_label"]
    unity=args["unity"]
    out_path=args['out_path']
    out_format= args['out_format']

    the_file= KVH_file(paths[0], key_sep=sep_key, value_sep=sep_val)
    for path in paths[1::]:
        f= KVH_file(path, key_sep=sep_key, value_sep=sep_val)
        the_file.merge_vertical(f)
     
    matched_keys = select_keys(the_file, keys, keys_filter, unity)

    pos = select_pos(the_file, labels, labels_filter)

    if len(pos) == 1:
        the_file.pie_plot(matched_keys,out_path, out_format, it=pos[0])
    else:
        the_file.plot(matched_keys, out_path, out_format, ylabel, pos)




        
        
