import parser
import bcolors

def get_git_file(path,commit):
    print("Recolting commit ", bcolors.BOLD,commit.hexsha,":", commit.message, bcolors.ENDC)
    f = commit.tree / path 
    return f.data_stream

args= parser.getArgs()

paths = args["files"]
out_path=args["out_path"]
sep_key = args["sep_key"] 
sep_val=args["sep_val"]
keys=args["add_key"]
git_extract=args['git_extract']
git_actualized_label=args['git_actualized_label']
merge=args["merge"]
extend_history=args["extend_history"]
forbiden_commits = args["commits_filter"]
branchs=args['branchs']
paths_restrict=args['paths_restrict']

def merge_handle(paths, output, vertical=True):
    res=KVH_file(key_sep=sep_key, value_sep= sep_val)
    if vertical:
        the_function=res.merge_vertical
    else:
        the_function=res.merge_horizontal
    
    for path in paths:
            the_function(path)
    res.dump(out_path)

if merge:
    merge_handle(paths, out_path, vertical=True, keys=keys)
    
elif extend_history:
    merge_handle(paths, out_path, vertical=False, keys=keys)

elif keys:
    for f in paths:
        kvh_File= KVH_file(f, key_sep=sep_key, value_sep= sep_val)
        for key in keys:
            split= key.split(self.sep_key)
            if len(split)==2:
                key_name, values= split
                where_to_extend= kvh_File[key_name].means
            elif len(split)==3:
                key_name, attr, values = split
                where_to_extend = getattr(kvh_File[key_name], attr)
            else:
                sys.exit("Error, In key add mode, the keys should be in the form KEYNAME KEYSEP VALUE1 VALUESEP VALUE2 to add values to keys or KEYNAME KEYSEP ATTRIBUTE KEYSEP VALUE1 VALUESEP VALUE2... to add drawing attribute to an existant key ")
            where_to_extend.extend(kvh_File.parse_values(values))
        kvh_File.dump(path)

elif git_extract !=None:# Can be empty list
    if not git_extract:
        git_extract=None# We reput it to none in that case to triger default of explore
    res= KVH_file(key_sep=sep_key, value_sep= sep_val)
    for commit in git_commits_explore(paths[0], commits=git_extract, filter=forbiden_commits, branchs=branchs, paths_restrict=paths_restrict):
        files = commit.search_files(paths)
        commit_kvh_file= KVH_file(key_sep=sep_key, value_sep= sep_val)
        for file in files:
            commit_kvh_file.merge_vertical(KVH_file(file, key_sep=sep_key, value_sep= sep_val)) 
        res.merge_horizontal(commit_kvh_file)
    res.dump(out_path)

elif git_actualized_label:
    previous_commit= git_get_head(paths[0]).parents[0]
    for path in paths:
        current_file = KVH_file(path, key_sep=sep_key, value_sep= sep_val)
        old_file= KVH_file(previous_commit.search_files(path), key_sep=sep_key, value_sep= sep_val)
        if current_file.labels[-1] == old_file[labels-1]:
            sys.exit("Error: "+ path + " have the same label than in the previous commit")
        else:
            print(",".join(paths) +" all have new labels", file=sys.stderr)
