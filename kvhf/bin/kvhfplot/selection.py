import re
#This fragmentation is a hav
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
