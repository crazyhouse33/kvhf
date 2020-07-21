import parser
import sys
from kvhf.file import KVH_file
import gfe.gfe as gfe


def str_commit(commit, number_message_letter):
    message=commit.message[0:number_message_letter]
    if len(commit.message) >number_message_letter:
       message+="..." 
    return " ".join([commit.hexsha,':',message])


args= parser.getArgs()

paths = args["files"]
out_path=args["out_path"]
sep_key = args["sep_key"] 
sep_val=args["sep_val"]
keys=args["keys"]
git_extract=args['git_extract']
commits_manual_selection=args['commits']
git_actualized_label=args['git_actualized_label']
merge=args["merge"]
extend_history=args["extend_history"]
forbiden_commits = args["commit_filter"]
branchs=args['branchs']
paths_restrict=args['path_restrict']
dirty=args['dirty']




def merge_handle(paths, output, vertical=True, keys=None):
    res=KVH_file(key_sep=sep_key, value_sep= sep_val)
    if vertical:
        the_function=res.merge_vertical
    else:
        the_function=res.merge_horizontal
    
    for path in paths:
        file_to_merge=KVH_file(path,key_sep=sep_key, value_sep= sep_val)
        the_function(file_to_merge,keys)
    res.dump(out_path)

if merge:
    merge_handle(paths, out_path, vertical=True, keys=keys)
    
elif extend_history:
    merge_handle(paths, out_path, vertical=False, keys=keys)
elif keys:

    for path in paths:
        try:
            kvh_File= KVH_file(path, key_sep=sep_key, value_sep= sep_val)
        except FileNotFoundError:
            kvh_File=KVH_file(key_sep=sep_key, value_sep= sep_val)
        for key in keys:
            split= key.split(sep_key)

            if len(split)==2:
                key_name, values= split
                where_to_extend= kvh_File.dico[key_name].means
            elif len(split)==3:
                key_name, attr, values = split
                where_to_extend = getattr(kvh_File.dico[key_name], attr)
            else:
                sys.exit("Error, In key add mode, the keys should be in the form KEYNAME KEYSEP VALUE1 VALUESEP VALUE2 to add values to keys or KEYNAME KEYSEP ATTRIBUTE KEYSEP VALUE1 VALUESEP VALUE2... to add drawing attribute to an existant key ")
            where_to_extend.extend(kvh_File.parse_values(values))
        kvh_File.dump(path)

else:
    if not paths:
        sys.exit("At least one file to extract must be given in order to localize git repo")
    repo= gfe.get_repo(paths[0])

    if git_extract:
        res= KVH_file(key_sep=sep_key, value_sep= sep_val)
        for commit in gfe.explore_commits(repo, commits=commits_manual_selection, filter=forbiden_commits, branchs=branchs, paths_restrict=paths_restrict,reverse=True):
            files = commit.search_files(paths)
            commit_kvh_file= KVH_file(key_sep=sep_key, value_sep= sep_val)
            for file in files:
                new_file=KVH_file(file, key_sep=sep_key, value_sep= sep_val)
                commit_kvh_file.merge_vertical(new_file) 
            print ("Recolting commit", str_commit(commit,20), file=sys.stderr) 
            res.merge_horizontal(commit_kvh_file)

        #We got the commits, now we need to add current files if they is one dirty ones
        if dirty and gfe.diffs(paths, repo):
            current_kvh_file= KVH_file(key_sep=sep_key, value_sep= sep_val)
            for path in paths:
                    to_merge=KVH_file(path, key_sep=sep_key, value_sep= sep_val)
                    current_kvh_file.merge_vertical(to_merge)
            res.merge_horizontal(current_kvh_file)
        res.dump(out_path)

    elif git_actualized_label:
        head= repo.head.commit
        for path in paths:
            current_file = KVH_file(path, key_sep=sep_key, value_sep= sep_val)
            old_file= KVH_file(head.search_files(path), key_sep=sep_key, value_sep= sep_val)
            if current_file.labels[-1] == old_file.labels[-1]:
                sys.exit("Error: "+ path + " have the same label than in the previous commit")
            else:
                print("All given files have new labels", file=sys.stderr)
