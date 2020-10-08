import matplotlib.pyplot as pyplot
from warnings import warn
from collections import defaultdict
from kvhf.history_entry import Serie_stats, filter_out_Nones
from kvhf.libs.ppath import prepare_path, open_mkdir


class KVH_file:
    default_key_sep = ":"
    default_value_sep = ","
    default_value_generator = float
    default_void_str = '_'

    def __init__(self, file_or_dico=None, key_sep=None,
                 value_sep=None, value_generator=None, void_str=None):
        """Create a super dict from a normal dict, or a file. Empty super dict if nothing"""
        if value_generator is None:
            value_generator = KVH_file.default_value_generator
        if key_sep is None:
            key_sep = KVH_file.default_key_sep
        if value_sep is None:
            value_sep = KVH_file.default_value_sep
        if void_str is None:
            void_str = KVH_file.default_void_str
        self.void_str = void_str
        self.key_sep = key_sep
        self.value_sep = value_sep
        self.value_generator = value_generator
        self.labels = []
        self.dico = defaultdict(Serie_stats)
        self.current_key = ""
        if file_or_dico is None:
            return
        if isinstance(file_or_dico, dict):
            self.dico = file_or_dico
        elif isinstance(file_or_dico, str):
            self.parse_file_name(file_or_dico)
        elif hasattr(file_or_dico, 'read') and callable(file_or_dico.read):  # python 3 cant use file
            if hasattr(file_or_dico, 'name'):
                self.parse_file(file_or_dico, file_or_dico.name)
            else:
                self.parse_file(file_or_dico, "UNKNOWFILE")
        else:
            raise TypeError(
                "Init argument must be nothing, a path (str), a file, or dictionnary, not " +
                str(
                    type(file_or_dico)))

    def dump(self, file, keys=None, key_sep=None,
             value_sep=None, void_str=None):
        """Serialize subset of keys (default all) to given path"""
        if keys is None:
            keys = self.dico.keys()

        if key_sep is None:
            key_sep = self.key_sep

        if value_sep is None:
            value_sep = self.value_sep

        if void_str is None:
            void_str = self.void_str

        if type(file) == str:
            file = open_mkdir(file, "w")

        # dump labels
        if self.labels:
            print ("#" + self.value_sep.join(self.labels), file=file)

        # dump keys
        for key in keys:
            entry = self.dico[key]
            print(entry.dump(key, value_sep, key_sep, void_str), file=file)

    def parse_file(self, file, filename=''):
        """Parse a file"""
        file_content = file.read()
        if not type(file_content) == str:
            file_content = file_content.decode()
        lines = file_content.split('\n')
        if lines[0].startswith("#"):
            self.parse_labels(lines[0])
            start = 1
        else:
            start = 0
        if not self.labels:
            warn("No labels found in file: " + filename)
        cpt = start + 1
        for line in lines[start::]:
            self.parse_line(line, cpt, filename)

    def parse_value(self, str_value):
        """Try to aply the generator (float by default). If fail, return None"""
        str_value = str_value.strip()
        if str_value == self.void_str:
            return None

        return self.value_generator(str_value)

    def parse_values(self, values):
        return [self.parse_value(str_value)
                for str_value in values.strip().split(self.value_sep)]

    def parse_line(self, line, line_num=-1, file_name=''):
        try:
            key, sep, values_str = line.partition(self.key_sep)
            key = key.strip()
            if (not sep):
                if key:
                    warn(
                        "Ignoring line :\n\"" +
                        line +
                        "\"\n because no value separator found")
                return

            if key.startswith("-") and self.current_key:

                if key[1::].strip().startswith("unity"):
                    self.dico[self.current_key].unity = values_str.strip()
                else:
                    values = self.parse_values(values_str)
                    if key[1::].strip().startswith("maxs"):
                        self.dico[self.current_key].maxs = values
                    elif key[1::].strip().startswith("mins"):
                        self.dico[self.current_key].mins = values
                    elif key[1::].strip().startswith("stdev"):
                        self.dico[self.current_key].stdevs = values
                    else:
                        warn("Unknow attribute at line: " + line)
            else:
                self.current_key = key
                stats = self.dico[self.current_key]
                stats.means = self.parse_values(values_str)
        except Exception as e:
            raise ValueError("Cannot parse {}:{}:{}".format(file_name, line_num, line)) from e

    def parse_labels(self, line):
        self.labels = line[1::].split(self.value_sep)

    def parse_file_name(self, path):
        """Open file and parse it. """
        with open(path) as f:
            self.parse_file(f, path)

    def merge_vertical(self, file2, keys=None):
        """Add entries of dico 2 corresponding to keys (by default all). If key is allready present, the new value replace the old one. This is supposed to be the same as concating 2 files and parsing the result"""
        if file2.labels:
            if self.labels and self.labels != file2.labels:
                warn(
                    "Vertical merge on different labels files. New labels replaced old ones)")
            self.labels = file2.labels
        if keys is None:
            keys = file2.dico.keys()

        for key in keys:
            if key in self.dico:
                warn(
                    "Key " +
                    key +
                    " is going to be overwritten by vertical merge")
            self.dico[key] = file2.dico[key]

    def merge_labels(self, file2):
        intersection = [
            value for value in self.labels if value in file2.labels]
        if intersection:
            warn("Label collision on labels: " + '\n'.join(intersection))
        self.labels.extend(file2.labels)

    def merge_horizontal(self, file2, keys=None):
        """Add entries of file2 corresponding to keys (by default all). If key is allready present, append the values of the second dico the existing one"""
        self.merge_labels(file2)
        if keys is None:
            keys = file2.dico.keys()

        for key in keys:
            self.dico[key].extend(file2.dico[key])

    def merge_historic(self, file2, keys=None):
        """Merge second file assuming it's a new time iteration, gestionning key appearance and deletion. Return deletions and appearances"""
        if keys is None:
            keys = file2.dico.keys()

        news = []
        olds = set(self.dico.keys())
        for key in keys:
            if key not in self.dico:
                news.append(key)
            else:
                olds.remove(key)
        self.merge_horizontal(file2)
        max_key, max_len = self.get_max_len()
        self.re_equilibrate(news, max_len, left=True)
        self.re_equilibrate(olds, max_len, left=False)
        return olds, news

    def labels_to_pos(self, labels):
        return [self.labels.index(label) for label in labels]

    def _desequilibred_keys(self, target):
        return [key for key, value in self.dico.items() if len(value)
                != target]

    def desequilibred_keys(self):
        """Return keys that dont have same number of values than number the max len key"""
        max_key, target = self.get_max_len()
        return self._desequilibred_keys(target), max_key, target

    def get_max_len(self):
        """Get Highest key"""
        keys_len_tuple = [(key, len(serie))
                          for key, serie in self.dico.items()]
        if not keys_len_tuple:
            return 'NOKEY', 0
        return max(keys_len_tuple, key=lambda x: x[1])

    def re_equilibrate(self, not_equilibred, target, left=False):
        """Pads any given keys to match target. """
        for key in not_equilibred:
            entry = self.dico[key]
            entry.means = Serie_stats.pad_list(entry.means, target, left=left)

    def draw_shared_prep(title=''):
        fig = pyplot.figure()
        if title:
            pyplot.title(title)
            fig.canvas.set_window_title(title)

    def draw_pie(self, keys=None, title='', it=-1):
        """Plot pie chart of last values of given keys (all by default) at the version given by the index. By default last label is used"""
        if keys is None:
            keys = sorted(self.dico.keys())

        values = []
        for key in keys:
            entry = self.dico[key]
            substat = entry.fragment()  # Working on copy to call re_equilibrate
            substat.re_equilibrate()  # Fixing label misagnilement
            values.append(substat.means[it])

        pos, values = filter_out_Nones(values, range(len(values)))
        labels = [keys[position] for position in pos]

        KVH_file.draw_shared_prep(title)
        pyplot.pie(values, labels=labels, autopct='%1.1f%%')

    def draw_history(self, keys=None, pos=None,
                     ylabel=None, title='', label_rot=0):
        """Plot on same graph every values of given keys (all by default). If only one label is selected, print keys side by side"""
        if ylabel is None:
            ylabel = ""

        if pos is None:
            pos = range(self.get_max_len()[1])

        if keys is None:
            keys = sorted(self.dico.keys())

        if len(pos) == 1:
            # it=-1 crash for empty list or empty attributes
            return self.draw_bars(keys=keys, ylabel=ylabel,
                                  title=title, it=pos[0], label_rot=label_rot)

        labels = [
            self.label_repr(
                self.labels[i]) if i < len(
                self.labels) else '' for i in pos]

        # Ploting nice grid and stuff

        KVH_file.draw_shared_prep(title)
        pyplot.grid(axis="x")
        pyplot.ylabel(ylabel)
        pyplot.xticks(pos, labels, rotation=label_rot)

        for key in keys:
            self.dico[key].plot(key, pos)

        pyplot.legend()

    # TODO integrate unity in labels
    def draw_bars(self, keys=None, ylabel=None, title='', it=-1, label_rot=0):
        """Plot keys sides by side."""

        if ylabel is None:
            ylabel = ""

        if keys is None:
            keys = sorted(self.dico.keys())

        KVH_file.draw_shared_prep(title)

        pyplot.xticks(range(len(keys)), keys, rotation=label_rot)
        pyplot.grid(axis="y")
        pyplot.ylabel(ylabel)

        for i, key, in enumerate(keys):
            self.dico[key].plot_one(key, i, it)

    def label_repr(self, label):
        """Return the part that is supposed to be printed by the plotter in a label"""
        return label.split(self.key_sep)[-1]

    def save_img(self, path, format=None):
        if format is None:
            format = 'svg'
        prepare_path(path)
        pyplot.savefig(path, format=format, transparent=True)

    def plot(self, block=False):
        pyplot.show(block=block)

# Todo split in more functions

    def check_labels(self, max_key=None, max_value=None):
        msg = []
        if max_value is None:
            max_key, max_value = self.get_max_len()

        if not len(self.labels) == max_value:
            msg.append("\nLabels (number={}) does not cover all given iterations (number={} from key{}).\n".format(
                len(self.labels), max_value, max_key))
        return msg

    def check_alignement(self):
        not_equilibred, max_key, target = self.desequilibred_keys()
        msg = []
        if not_equilibred:
            msg.append(
                "All keys dont have same lenght (max={}):\n".format(target))
            for key in not_equilibred:
                entry = self.dico[key]
                msg.append(
                    "\t- Requilibrating necessary for key {} of size {}.".format(key, len(entry)))
            msg.append("\nThis keys will be appended with the void value. This can indicate a bug in your file generation, such a disparion/aparition of a metric.\n")
        return msg, max_key, target

    def check_report(self):
        # Alignement checks
        msg, max_key, target = self.check_alignement()

        # Labels checks
        msg.extend(self.check_labels(max_key, target))

        # Individual keys checks
        msg.extend(self.check_keys())

        return "\n".join(msg)

    def check_keys(self):

        msg = []
        # Individual keys checks
        for key, value in self.dico.items():
            target = len(value)
            desequilibred_attributes = value.desequilibred_attributes()
            desequilibred_attributes = [
                attribute for attribute in desequilibred_attributes if attribute[1]]
            if desequilibred_attributes:
                msg.append(
                    "\nSome attributes of key {} dont have same lenght as the key size({}): \n".format(
                        key, target))

                for attribute_name, the_list, size in desequilibred_attributes:
                    msg.append(
                        "\t- {} is of size {}".format(attribute_name, size))
                msg.append(
                    "\nTheses attributes will be appended with void values. This can indicate a bug in your file generation, that suddently stop recolting some metrics.")
            mathmathic_problems = value.mathematic_impossibilities()
            if mathmathic_problems:
                msg.append(
                    'Some impossibles situations had been detected for key {}:\n'.format(key))
                for index, problem in mathmathic_problems:
                    msg.append('\t Index {}, {}'.format(index, problem))

        return msg

    def __eq__(self, other):
        return self.dico == other.dico
