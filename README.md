# KVHF
Key Values History File.

This python package come from a suit of software that aim to make your continious integration system able to compare intersting performance related metrics across commits.

You can also use this as an easy way to plot graphs.

## Content

### Executables
1. kvhfplot
2. kvhfutils

### Libs

The package expose python modules that you may find usefull:

1. Modules to manipulate kvhf file ( kvhf.file and kvhf.stat )
2. Wrapper simplifying gitpython interface to facilitate repository exploration(lib.gfe)
3. Some convenients functions to open files even if parents directory does not exist (lib.ppath)

## Install
```bash
pip install --index-url https://test.pypi.org/simple/ kvhf
```

## kvhplot
### File format

A KVHF file is composed from 3 kinds of entity, separated by lines

 1. Labels: Placed at the begining of the file prepended by # and separated by specified key\_sep.
 2. Keys: Anything not starting by -, followed by key\_sep, and somes values separated by precised val\_sep
 3. Attributes : You can give the plotter more information about the last key which will change the way the plotter draw it. See the exemple in next section.


### Exemple
Imagine you have following file:

```
#t1,onlyforsearch:t2,t3

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
kvhfplot file
```

will output the plot this image:

![Iteration mode](https://github.com/crazyhouse33/kvhf/blob/dev/dev/data/images/hist.png?raw=true)

If your selection match only one label, it switch to bar chart mode:
```bash
kvhfplot file -l t1
```
![Key mode](https://github.com/crazyhouse33/kvhf/blob/dev/dev/data/images/hist_bars.png?raw=true)

If you activate the comparison switch, it print to pie chart mode:
```bash
kvhfplot file -l t1 -c
```
![Pie mode](https://github.com/crazyhouse33/kvhf/blob/dev/dev/data/images/hist_pie.png?raw=true)


Run kvhfplot -h to get more details about how to control what is being plotted (add title, choose keys...)

Any value can be "\_", which denote the fact that for an iteration the value was unknown.

## Continious Integration and KVHF

The plotter come with utilities to facilitate integration of KVHF continious integration systems, in order to plot metrics at wanted commits.

The recommended way to use kvhf in this purpose will be illustrated in following section. This will also serve as doc to use the package as a whole and wont expose every functionnalities of every tool. You are invited to read the help option of every executable.

The recommended way is to automatate of a kvhf file per commit, and to merge it with an accumulator. This way, in each commit, you have:

1. A clean per commit resume file
2. The accumulator to print the past

Without the accumulator, you are gonna need to extract a kvhf from the git history trought kvhfutils --git-extract (see later) to produce history plotting. But extracting is gonna be slower and slower for every commits.

### Step 1: Script File Creation

First, you need a way to automate a per commit kvhf file creation. For this you can use:
 1. kvhfutils -k to add keys or attribute to allready existing kvhf file.
 2. kvhfutils -m to combine keys of two allready existing kvhf files.
 3. A third party software that produce kvhf files (eprof)
 4. kvhfutils -v to check than the file is aligned and dont contain any kind of abnormalies that could come from a bug in you generation


According to your build system, create a script or a target that create that commit resume thanks to those tools. Lets call this generate.bash

ex:
```bash
kvhfutils per_commit_resume.kvf -k exe_size:$(du bin/myexe | cut -f1) -k exe_size:unity:Ko
kvhfutils per_commit_resume.kvf -v -k exec_time:$(TIMEFMT=%R; time the_perf_test >/dev/null) -k exec_time:unity:ms
```


### Step 2: Commits hooks management

In general you have to understand that changing labels coming from previous commits is going to be super annoying and dangerous (git rebase). And thus you must really be carefull with the choices of your labels.

This step is not mandatory to use kvhf but any humans are guaranted to make the following mistakes one day:

1. Forgeting to rerun your first step script to overide the per\_commit\_resume file
2. Forgeting to put a label on the new per\_commit\_resume file
3. Forgeting to merge the resume with the accumulator

That's why you should integrate to your commits hooks the following actions.

#### 1 Forcing Regeneration of Resume File
```bash
(pre-commit) generate.bash
```
#### 2 Prevent Misuage of Labels
(pre-commit) kvhfutils --actualized per\_commit\_resume --required-length 1

This will check that the label of the file is existing and not the same as the previous commit one (Will ask you to input a label name if you did not do it in generate). This will also check than each key is of lenght 1

#### 3 Accumulate Resume
```bash
(pre-commit) kvhfutils -o accumulator.kvhf  --historic-merge accumulator.kvhf per\_commit\_resume
```
This save the need to extract the whole history each time you want to plot it. This must be one of the last pre-commit action because if this is executed and a latter action fail, your hkvf file will be polluted with an additional erronous commit. However this error will be detected by the --required-lenght option
#### 4 Amend the changes
(post-commit) git commit --amend accumulator.kvhf per\_commit\_resume
This may be unnecessary if your continuous integration already include your pre-commit modifications in the commit.


## Tricks

### Other way of filtering commits
Choosing wich iteration to plot with the labels regexp selection/filter is not the only way. Alternatively you can use kvhfutils -g to extract a kvhf file from subsets of commits only. You are able to select commits that modified a particular set of file such as in the following exemple:
```bash
kvhfutils --git-extract --path-restrict src/executor.c -p io.c -o important_changes.kvhf
```

You can also specify a list of commits. The labels will be extracted in given order. You can achieve the same results as previous command with:

```bash
kvhfutils -g -c $(git rev-list src/executor.c io.c --reverse)
```

## TODO
3. Allow to execute a command in each commit before extraction. That would allow to generate kvhf files of previous commits with the current generation script. For now you should look into git rebase exec
4. (plotting) Smarter way to choose the stale according to keys values
3. (plotting) New attributes number of occurence, allong with total mode (that print summed value )
4. (plotting) 
5. (utils) Allow -prefix option for merges that would append a prefix to any merged keys
6. Add same keys option, that when recolting/plotting considers somes keys renamed (warning on collision)
7. Undestand what'up with gfe tests not runnable out of my local machine (git submodule machinery messing with it, some necessary file are not versionned)

