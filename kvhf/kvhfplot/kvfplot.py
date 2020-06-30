import parser
import bcolors

def get_git_file(path,commit):
    print("Recolting commit ", bcolors.BOLD,commit.hexsha,":", commit.message, bcolors.ENDC)
    f = commit.tree / path 
    return f.data_stream

args= parser.getArgs()

path = args["file"]
sep_key = args["sep_key"] 
sep_val=args["sep_val"
keys=args["keys"]
branch= args["branch"]
start_commit=args["start_commit"]
commits=args["commits"]
forbiden_commits = args["commits_filter"]

if not args['git']:

    sdf= Serie_dict_file(path, sep_key, sep_val])
    sdf.plot_pie(keys)
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













