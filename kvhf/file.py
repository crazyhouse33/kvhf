import matplotlib.pyplot as pyplot
from warnings import warn
__version__= "@version@"
 

class Key_Value_History_File:
    default_key_sep = ":"
    default_value_sep = " "
    def __init__(self, file_or_dico=None, key_sep=default_key_sep, value_sep=default_value_sep):
        """Create a super dict from a normal dict, or a file. Empty super dict if nothing"""
        self.key_sep=key_sep;
        self.value_sep=value_sep;
        self.labels=[]
        if not file_or_dico:
            self.dico = dictdefault(list)  
        elif isinstance(file_or_dico,dict):
            self.dico = file_or_dico
        elif isinstance (file_or_dico, str):
            self.dico = parse_file_name(file_or_dico)
        elif isinstance (file_or_dico, file):
            self.dico = parse_file(file_or_dico)
        else:
            raise RuntimeError("Init file or dico must be a path (str), a file, or dictionnary, not"+ str(type(file_or_dico)))


    
    def dump(self, file, keys=None, key_sep=default_key_sep, value_sep=default_value_sep):
        """Serialize subset of keys (default all) to given path"""
        if keys == None:
            keys= self.dico.keys()

        with open(file,"w") as f:
            for key in keys:
                print("{}{}{}".format(key, key_sep, value_sep.join(self.dico[key])),file=f)

    def parse_file(file, key_sep, value_sep):
        """Parse a file"""
        dico=Key_Value_History_File(key_sep = key_sep, value_sep = value_sep)
        lines= file.read().split('\n')
        dico.parse_labels(lines[0])
        if not dico.labels:
            warn("No labels found in file ", file)
        for line in lines[1::]: 
            dico.parse_line(line)

        if line.startwith('#'):
            self.labels.append((cpt, line[1:].split(key_sep)))
        return dico

    def parse_line(dico, line):
        key, sep, values= line.partition(dico.key_sep)
        if sep:
            dico[key]= values.split(dico.value_sep)

    def parse_labels(dico, line):
        if line.startwith("#"):
            dico.labels=line[1::].split(dico.key_sep)



    def parse_file_name(path, key_sep, value_sep):
        """Open file and parse it. """
        with open(path) as f:
            return parse_file(f, key_sep, value_sep)

    def merge_vertical(self,dico2, keys=None):
        """Add entries of dico 2 corresponding to keys (by default all). If key is allready present, the new value replace the old one. This is supposed to be the same as concating 2 files and parsing the result"""
        if self.labels != dico2.labels:
            warn("Vertical merge on different labels files. New label are the one of the first)")
        if keys == None:
            keys = dico2.dico.keys()

        for key in keys:
            if self.dico[key]:
                warn("Key ", key, " is going to be overwritten by vertical merge")
            self.dico[key]= dico2.dico[key]

    def merge_horizontal(self, dico2, keys = None):
        """Add entries of dico2 corresponding to keys (by default all). If key is allready present, append the values of the second dico the existing one"""
        intersection = [value for value in self.labels if value in dico2.labels]
        if intersection:
            warn("Label collision on labels: " + '\n'.join(intersection))
        self.labels.extend(dico2.labels)
        if keys== None:
            keys = dico2.dico.keys()

        for key in keys:
            self.dico[key].extend(dico2.dico[key])

    def plot(self, keys=None):
        """Plot on same graph every values of given keys (all by default)"""
        if  keys==None:
            keys= self.dico.keys()

        plt.xticks(x, self.labels)

        for key in keys:
            pyplot.plot(self.dico[key], label=key)

        pyplot.legend()

    def plot_pie(self, keys=None, label=None, it=-1):
        """Plot pie chart of last values of given keys (all by default) at the version given either by the label, either by the index. By default last label is used"""
        if keys ==None:
            keys=self.dico.keys()

        if label!=None:
            it = self.labels.index(label)

        values = [self.dico[key][it] for key in keys]
        pyplot.pie(values, labels=keys)

    
    def __eq__(self, other):
        return self.labels == other.labels and self.dico == other.dico






