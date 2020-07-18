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
                kvh_File[key_name].means.extend(kvh_File.parse_values(values))
            elif len(split)==3:
                key_name, attr, values = split
                getattr(kvh_File[key_name], attr).extend(kvh_File.parse_values(values))
            else:
                sys.exit("Error, In key add mode, the keys should be in the form KEYNAME KEYSEP VALUE1 VALUESEP VALUE2 to add values to keys or KEYNAME KEYSEP ATTRIBUTE KEYSEP VALUE1 VALUESEP VALUE2... to add drawing attribute to an existant key ")
        kvh_File.dump(path)

elif git_extract:



    

def merge_handle(paths, output, vertical=True):
    res=KVH_file(key_sep=sep_key, value_sep= sep_val)
    if vertical:
        the_function=res.merge_vertical
    else:
        the_function=res.merge_horizontal
    
    for path in paths:
            the_function(path)
    res.dump(out_path)




if extend_history:
    res=KVH_file()
    for path in paths:
        res.merge_horizontal(path)

else:

    import git

    breakpoint()
    repo = git.Repo(path, search_parent_directories=True)
    root= repo.working_dir
    path= os.path.relpath(path, start = root)
    if branch==None:
        branch = repo.active_branch 
    
    #commit construction:
    if commits == None:
        good_commits=[]
        for commit in repo.iter_commits(branch, paths=path, since_hash = start_commit):
            if (commit.hexsha not in forbiden_commits):
                good_commits.append(commit)
    else:
        good_commits=[repo.rev_parse(commit) for commit in commits]

    for commit in good_commits:
        f = get_git_file(path,commit)













