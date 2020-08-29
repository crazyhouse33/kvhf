from warnings import warn
from collections import defaultdict

import matplotlib.pyplot as pyplot
pyplot.style.use('seaborn-dark')


all_series_attributes = ['maxs', 'mins', 'stdevs']
# WARNING Keep means first
all_serie = ['means'] + all_series_attributes


def filter_out_Nones(liste, pos):
    posx = []
    values = []
    max_size = len(liste)
    for position in pos:
        if position < max_size:
            value = liste[position]
            if value is not None:
                values.append(value)
                posx.append(position)
    return posx, values


class Serie_stats:

    def __init__(self, means=None, mins=None,
                 maxs=None, stdevs=None, unity=None):
        self.means = means if means is not None else []
        self.mins = mins if mins is not None else []
        self.maxs = maxs if maxs is not None else []
        self.stdevs = stdevs if stdevs is not None else []
        self.unity = unity if unity is not None else ''

    def pad_list(liste, wanted_len, left=True, padder=None):
        """Remove end items till reaching wanted_len if too big.
           prepend None  till reaching wanted_len if too small.
        """

        diff = wanted_len - len(liste)
        if diff == 0:
            return liste

        if diff > 0:
            if left:
                res = [padder] * diff + liste
            else:
                res = liste + [padder] * diff
            return res
        else:
            return liste[:wanted_len]

    def fragment(self, pos=None):
        if pos is None:
            pos = range(len(self.means))
        res = Serie_stats()
        for attribute in all_serie:
            the_list = getattr(self, attribute)
            size = len(the_list)
            setattr(res, attribute, [the_list[i] for i in pos if i < size])

        res.unity = self.unity
        return res

    def plot(self, label, pos):
        """Plot history at given positions, remove None entries from drawing"""

        if self.unity:
            label += " (" + self.unity + ")"
        substat = self.fragment(pos)  # Taking subpart of pos
        substat.re_equilibrate()  # Fixing label misagnilement

        posmeans, means = filter_out_Nones(substat.means, pos)
        len_means = len(means)

        base_line, = pyplot.plot(posmeans, means, marker='o', label=label)
        current_color = base_line.get_color()

        posbars, stdevs = filter_out_Nones(substat.stdevs, posmeans)
        bar_means = [substat.means[i] for i in posbars]
        pyplot.errorbar(
            posbars,
            bar_means,
            yerr=stdevs,
            capsize=2,
            fmt='none',
            color=current_color)

        posmax, maxs = filter_out_Nones(substat.maxs, posmeans)
        max_means = [substat.means[i] for i in posmax]
        pyplot.fill_between(
            posmax,
            maxs,
            max_means,
            alpha=0.15,
            color=current_color)

        posmin, mins = filter_out_Nones(substat.mins, posmeans)
        min_means = [substat.means[i] for i in posmin]
        pyplot.fill_between(
            posmin,
            mins,
            min_means,
            alpha=0.15,
            color=current_color)

    def plot_one(self, label, drawing_pos, position):
        """Plotting considering only one position (The notmal plot stay just empty). This can be called only on equilibred entries with only one label"""
        if self.unity:
            label += " (" + self.unity + ")"

        substat = self.fragment([position])  # Taking subpart of pos
        substat.re_equilibrate()  # Fixing label misagnilement

        the_mean = substat.means[position]
        the_stdev = substat.stdevs[position]
        the_min = substat.mins[position]
        the_max = substat.maxs[position]

        if not the_mean:
            return

        base_line, = pyplot.plot(
            drawing_pos, the_mean, marker='o', label=label)
        current_color = base_line.get_color()

        if substat.unity:
            label += " (" + substat.unity + ")"

        if the_stdev:
            pyplot.errorbar(
                drawing_pos,
                the_mean,
                yerr=the_stdev,
                capsize=2,
                fmt='none',
                color=current_color)

        # Pyplot height variable is really badely named.
        if the_min:
            pyplot.bar(
                drawing_pos,
                the_mean - the_min,
                bottom=the_min,
                alpha=0.2,
                color=current_color)

        if the_max:
            pyplot.bar(
                drawing_pos,
                the_max - the_mean,
                bottom=the_mean,
                alpha=0.2,
                color=current_color)

    def __str__(self):
        return self.dump("means", " ", ":", "_")

    def dump_filter(self, value, void_str):
        if value is None:
            return void_str
        else:
            return str(value)

    def dump(self, label, value_sep, key_sep, void_str):
        lines = [label + key_sep +
                 value_sep.join([self.dump_filter(value, void_str) for value in self.means])]

        for attribute in all_series_attributes:
            atr_list = getattr(self, attribute)
            if atr_list:
                values_filtered = [
                    self.dump_filter(
                        value, void_str) for value in atr_list]
                lines.append('-' + attribute + key_sep +
                             value_sep.join(values_filtered))
        if self.unity:
            lines.append('-unity' + key_sep + self.unity)
        return '\n'.join(lines)

    def desequilibred_attributes(self):
        """Return attributes than dont have same size as the means"""
        all_serie_lists = [getattr(self, attribute)
                           for attribute in all_series_attributes]
        lens = map(len, all_serie_lists)
        mixed = zip(all_series_attributes, all_serie_lists, lens)

        return [serie for serie in mixed if serie[2] != len(self)]

    def re_equilibrate(self):
        """Align attributes with size. Append None on right"""
        desequilibred = self.desequilibred_attributes()
        for attribute in desequilibred:
            setattr(
                self,
                attribute[0],
                Serie_stats.pad_list(
                    attribute[1],
                    len(self),
                    left=False))

    def __len__(self):
        return len(self.means)

    def mathematic_impossibilities(self):
        """Here goes some check about attributes, for exemple min should always be smaller that mean and stuff like that and return a string about everything"""
        wrong = []
        len_wanted = len(self.means)
        stdevs_list = Serie_stats.pad_list(self.stdevs, len_wanted)
        mins_list = Serie_stats.pad_list(self.mins, len_wanted)
        maxs_list = Serie_stats.pad_list(self.maxs, len_wanted)
        for i in range(len_wanted):
            mean = self.means[i]
            stdevs = stdevs_list[i]
            mins = mins_list[i]
            maxs = maxs_list[i]
            if mean is None:  # Every check is based on mean
                continue

            if maxs is not None:
                if maxs < mean:
                    wrong.append(
                        i, "Attribute max = {} is smaller than the mean ={}".format(
                            maxs, mean))
                if mins is not None:
                    if maxs == mean != mins:
                        wrong.append(
                            i, "Attribute max = {} is equal to mean ={}, but min = {} is different".format(
                                maxs, mean, mins))
                if stdevs is not None:
                    if maxs == mean and stdevs != 0:
                        wrong.append(
                            i,
                            "Attribute max = {} is equal to mean ={} but stdevs = {} is different than 0".format(
                                maxs,
                                mean,
                                stdevs))

            if mins is not None:
                if mins > mean:
                    wrong.append(
                        i, "Attribute min = {} is bigger than the mean ={}".format(
                            mins, mean))

            if stdevs is not None:
                if mins == mean and stdevs != 0:
                    wrong.append(
                        i,
                        "Attribute min= {} is equal to mean ={} but stdevs = {} is different than 0".format(
                            mins,
                            mean,
                            stdevs))

        return wrong

    def extend(self, other):
        if self.unity != other.unity:
            warn("WARNING, extending keys of different units")
        self.means.extend(other.means)
        self.maxs.extend(other.maxs)
        self.mins.extend(other.mins)
        self.stdevs.extend(other.stdevs)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
