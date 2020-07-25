import parser
import sys
from kvhf.file import KVH_file
import lib.gfe as gfe


def str_commit(commit, number_message_letter):
    message=commit.message[0:number_message_letter]
    if len(commit.message) >number_message_letter:
       message+="..." 
    return " ".join([commit.hexsha,':',message])

def my_input(msg):
    if not_interactive:
        return input(msg+'.\n\nPlease enter a new label in the prompt:')
    else:
        sys.exit(msg)

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



args= parser.getArgs()

paths = args["files"]
out_path=args["out_path"]
sep_key = args["sep_key"] 
sep_val=args["sep_val"]
keys=args["keys"]
git_extract=args['git_extract']
commits_manual_selection=args['commits']
git_actualized_label=args['actualized']
merge=args["merge"]
extend_history=args["extend"]
forbiden_commits = args["commit_filter"]
branchs=args['branchs']
paths_restrict=args['path_restrict']
dirty=args['dirty']
not_interactive=args['not_interactive']




     


  


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
    if git_extract:
        
        repo= gfe.get_repo(paths[0])
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
        

        for path in paths:
            current_file = KVH_file(path, key_sep=sep_key, value_sep= sep_val)
            user_label=None
            if not current_file.labels:
                user_label=input("No label detected for "+ path)

            try:
                repo=gfe.get_repo(path)
                head=repo.head.commit
            except Exception:#There is no commit for this path so its new
                continue

            old_file= KVH_file(head.search_files(path), key_sep=sep_key, value_sep= sep_val)
            if current_file.labels[-1] == old_file.labels[-1]:
                user_label=input("The label of "+ path + " did not change since last commit")
            if user_label:
                current_file.labels.append(user_label)
                current_file.dump(path)





