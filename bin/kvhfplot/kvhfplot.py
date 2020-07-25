#!usr/bin/python3
import parser
from kvhf.file import KVH_file
import re

def select_keys(kvh_file, keys, keys_filter, unity):
    """Given a list of regexp string of wanted keys, unwanted key, an wanted unity, retrieve list of matching keys in a kvhf file"""

    keys_reg=[re.compile(key) for key in keys]
    keys_filter_reg= [re.compile(key) for key in keys_filter]
    unity_reg= [re.compile(unit) for unit in unity]
    return [key for key in kvh_file.dico.keys() if 
        (any(regex.match(key) for regex in keys_reg) or not keys_reg) and 
        not any(regex.match(key) for regex in keys_filter_reg) and 
        (any(regex.match(kvh_file.dico[key].unity) for regex in unity_reg) or not unity_reg)
        ]

def select_pos(kvh_file, labels, labels_filter):
    """Given a list of wanted label regexp string , and a list of unwanted one, return necessary indexs to match requirement"""
    labels_reg= [re.compile(label) for label in labels]
    labels_filter_reg= [re.compile(label) for label in labels_filter]
    matching_labels=[label for label in kvh_file.labels if (any(regex.match(label) for regex in labels_reg) or not labels) and
        not any(regex.match(label) for regex in labels_filter_reg)
        ]
    return kvh_file.labels_to_pos(matching_labels)
#We need to import the module for testing the two upper functions
if __name__ == "__main__":

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
    plot= args['plot']

    the_file= KVH_file(paths[0], key_sep=sep_key, value_sep=sep_val)
    for path in paths[1::]:
        f= KVH_file(path, key_sep=sep_key, value_sep=sep_val)
        the_file.merge_vertical(f)
     
    matched_keys = select_keys(the_file, keys, keys_filter, unity)

    pos = select_pos(the_file, labels, labels_filter)

    if len(pos) == 1:
        the_file.draw_pie(matched_keys, it=pos[0])
    else:
        the_file.draw_history(matched_keys, ylabel, pos)

    if out_path:        
        the_file.save_img(out_path, out_format)
    
    if not out_path or plot:
        the_file.plot()

    






        
        
