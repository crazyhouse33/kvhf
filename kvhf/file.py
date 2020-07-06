import matplotlib.pyplot as pyplot
from warnings import warn
from collections import defaultdict
from kvhf.stat import Serie_stats

 

class KVH_file:
    default_key_sep = ":"
    default_value_sep = " "
    default_value_generator=float
    def __init__(self, file_or_dico=None, key_sep=default_key_sep, value_sep=default_value_sep, value_generator= default_value_generator):
        """Create a super dict from a normal dict, or a file. Empty super dict if nothing"""
        self.key_sep=key_sep;
        self.value_sep=value_sep;
        self.value_generator= value_generator
        self.labels=[]
        self.dico = defaultdict(Serie_stats)  
        self.current_key=""
        if file_or_dico==None:
            return
        if isinstance(file_or_dico,dict):
            self.dico = file_or_dico
        elif isinstance (file_or_dico, str):
            self.parse_file_name(file_or_dico)
        else:#python 3 cant use file 
            try:
                self.parse_file(file_or_dico)
            except:
                raise TypeError("Init argument must be nothing, a path (str), a file, or dictionnary, not"+ str(type(file_or_dico)))


    
    def dump(self, file, keys=None, key_sep=default_key_sep, value_sep=default_value_sep):
        """Serialize subset of keys (default all) to given path"""
        if keys == None:
            keys= self.dico.keys()

        with open(file,"w") as f:
            for key in keys:
                print("{}{}{}".format(key, key_sep, value_sep.join(self.dico[key])),file=f)

    def parse_file(self, file):
        """Parse a file"""
        lines= file.read().split('\n')
        self.parse_labels(lines[0])
        if not self.labels:
            warn("No labels found in file ", file)
        for line in lines[1::]: 
            self.parse_line(line)

        if line.startswith('#'):
            self.labels.append((cpt, line[1:].split(self.key_sep)))

    def parse_values(self, values):
        return [self.value_generator(str_value) for str_value in  values.strip().split(self.value_sep)]


    def parse_line(self, line):
        key, sep, values= line.partition(self.key_sep)
        key=key.strip()
        if (not sep):
            if key:
                warn("Ignoring line :\n\"" + line + "\"\n because no value separator found")
            return 
        if key.startswith("-") and self.current_key:
            values= self.parse_values(values)
            if key[1::].strip().startswith( "maxs"):
                    self.dico[self.current_key].maxs=values 
            elif key[1::].strip().startswith( "mins"):
                    self.dico[self.current_key].mins= values
            elif key[1::].strip().startswith( "stdev"):
                    self.dico[self.current_key].stdevs= values
            else:
                warn("Unknow attribute at line: "+line)
        else:
            self.current_key=key
            stats= self.dico[self.current_key]
            stats.means= self.parse_values(values)

    def parse_labels(self, line):
        if line.startswith("#"):
            self.labels=line[1::].split(self.key_sep)



    def parse_file_name(self, path):
        """Open file and parse it. """
        with open(path) as f:
            self.parse_file(f)

    def merge_vertical(self,file2, keys=None):
        """Add entries of dico 2 corresponding to keys (by default all). If key is allready present, the new value replace the old one. This is supposed to be the same as concating 2 files and parsing the result"""
        if self.labels != file2.labels:
            warn("Vertical merge on different labels files. New label are the one of the first)")
        if keys == None:
            keys = file2.dico.keys()

        for key in keys:
            if self.dico[key]:
                warn("Key "+ key+ " is going to be overwritten by vertical merge")
            self.dico[key]= file2.dico[key]

    def merge_horizontal(self, file2, keys = None):
        """Add entries of file2 corresponding to keys (by default all). If key is allready present, append the values of the second dico the existing one"""
        intersection = [value for value in self.labels if value in file2.labels]
        if intersection:
            warn("Label collision on labels: " + '\n'.join(intersection))
        self.labels.extend(file2.labels)
        if keys== None:
            keys = file2.dico.keys()

        for key in keys:
            self.key_extend(key, file2.dico[key])

    def key_extend(self, key, stats):
        self.dico[key].extend(stats)

    

    def plot(self, keys=None, path="kvh_plot.svg", format="svg", ylabel=""):
        """Plot on same graph every values of given keys (all by default)"""
        #Ploting nice grid and stuff
        pyplot.figure()
        pyplot.xticks(range(len(self.labels)), self.labels)
        pyplot.grid(axis="x")
        pyplot.ylabel(ylabel)

        if  keys==None:
            keys= self.dico.keys()
        
        for key in keys:
            self.dico[key].plot(key)

        pyplot.legend()

        pyplot.savefig(path,format=format)


    def pie_plot(self, keys=None, path="kvh_pie_plot.svg", format="svg",  label=None, it=-1):
        """Plot pie chart of last values of given keys (all by default) at the version given either by the label, either by the index. By default last label is used"""
        if keys ==None:
            keys=self.dico.keys()

        if label!=None:
            it = self.labels.index(label)

        values = [self.dico[key].means[it] for key in keys]

        pyplot.figure()
        pyplot.pie(values, labels=keys)
        pyplot.savefig(path, format=format)

    
    def __eq__(self, other):
        return self.dico == other.dico
