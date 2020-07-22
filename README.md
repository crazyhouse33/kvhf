# KVHF
Key Values History File.

This python package come from a suit of software that aim to automate into the build system a solution to plot intersting metrics (usually performance related) across commits.

You can also use this as an easy way to plot graphs. 

# Install
```bash
pip install kvhf
``` 

# File format

A KVHF file is composed from 3 kinds of entity, separated by lines

 1. Labels: Placed at the begining of the file prepended by # and separated by specified key\_sep.
 2. Keys: Anything not starting by -, followed by key\_sep, and somes values separated by precised val\_sep
 3. Attributes : You can give the plotter more information about the last key which will change the way the plotter draw it. See the exemple in next section. 


# Plotter Exemple
You can use this package as an easy way to plot data. Imagine you have following file:

```
#t1:t2:t3

building time: 5,  6,7
-maxs:         6, 10, 11
-mins:         4,  5, 6
-stdevs:       1,  2, 3
-unity: sec

run time: 9,7,6
-mins: 4,5,4
```

Then the command 
```bash

``` 
will output this image.

If your selection match only one label, it switch to pie chart mode, such as in this exemple:

Run kvhfplot.py -h to get more details about how to control what is being plotted

# Continious Integration and KVHF

The plotter come with an utility to facilitate integration of KVHF to your continious integration in order to plot metrics at wanted commits.

The recommended way to use kvhf in this purpose will be illustrated in following section. But you can proceed differently to reach same result.

The recommended way is to create a one label kvhf file per commit, and to merge with an accumulator at each commit. This way, in each commit, you have:

1. A clean per commit resume file
2. The accumulator to print the past  

Without the accumulator, you are gonna need to extract a kvhf from the git history trought kvhfutils --git-extract (see later). But extracting is gonna be slower and slower for every commits.

## File Creation
First, you need a way to automate a per commit kvhf file creation. For this you can use:
 1. kvhfutils -k to add keys or attribute to allready existing kvhf file.
 2. kvhfutils -m to combine keys of two allready existing kvhf files.
 3. A third party software that produce kvhf files (eprof)

According to your build system, create a script or a target that create that commit resume thanks to those tools.

ex:
```bash
kvhfutils per_commit_resume.kvf -k exe_size: $(du bin/myexe) -k exe_size:unity:Mo
kvhfutils per_commit_resume.kvf -k exe_size: $(du bin/myexe) -k exe_size:unity:Mo
``` 

## Commits hooks

In general you have to understand that changing labels coming from previous commits is going to be super annoying and dangerous (git rebase). And thus you must really be carefull with the choices of your labels. 

This step is not mandatory to use kvhf but you are guaranted (if you are human) to make the following mistakes one day:

1. Forgeting to rerun your first step script to overide the per\_commit\_resume file
2. Forgeting to put a label on the new per\_commit\_resume file

That's why you should integrate to your commits hooks the following actions:
1. (pre-commit) kvhfutils --git-actualized-label per\_commit\_resume 

This will check that the label of the file is existing and not the same as the previous commit one. Forcing you to edit (and to think seriously about it) the label before commiting the change. 

2. (pre-commit) kvhfutils -o accumulator.kvhf  --extend accumulator.kvhf per\_commit\_resume

This save the need to extract the whole history each time you want to plot it.

3.(post-commit) rm per\_commit\_resume

This will make the next commit fail if you forgot to rerun the resume creation script.


# Tricks
The process of choosing wich labels to plot can be tedious even with the regexp selection/filter. You can use instead kvhfutils -g to extract a kvhf file from given commits only. Here you have this commit view that allow you to select commits that modified a particular set of file such as in the following exemple:
```bash
kvhfutils.py --git-extract --path-restrict src/executor.c -p io.c -o important_changes.kvhf
``` 

You can also specify a list of commits. The labels will be extracted in given order. You can achieve the same results as previous command with:

```bash
kvhutil -g -c $(git rev-list src/executor.c io.c --reverse)
```


# Libs
The package expose python modules that you may use:
1. Obviously a module to manipulate kvhf file ( kvhf.file and kvhf.stat )
2. Wrapper simplifying gitpython interface to facilitate repository exploration.

# Warning
I did kvhf because I felt the need for it for another project. I built it quicquely and put it on github. I tried to do something powerfull but all the edges features are not tested. I am sure if you try to mess around with features you can read in the help option and not presented here you can encounter some bugs. Pull request accepted :)

# TODO
1. (BASIC) Good gestion of disapparing appearing key during commits.
2. (label selection) Label in two part, on that is not plotted (the other one is still use for searching labels) 
4. (plotting) Smarter way to choose the stale according to keys values
3. (plotting) New attributes to plot?

