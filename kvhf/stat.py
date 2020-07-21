from warnings import warn
from collections import defaultdict

import matplotlib.pyplot as pyplot


class Serie_stats:
    def __init__(self):
        self.means=[]
        self.maxs=[]
        self.mins=[]
        self.stdevs=[]
        self.unity=""



    def fragment(self,pos=None):
        if pos==None:
            pos= range(len(self.means))
        res= Serie_stats()
        res.means=[self.means[i] for i in pos if i<len(self.means) ]
        res.stdevs=[self.stdevs[i]  for i in pos if i<len(self.stdevs)]
        res.maxs=[self.maxs[i] for i in pos if i<len(self.maxs) ]
        res.mins= [self.mins[i] for i in pos if i<len(self.mins) ]
        res.unity=self.unity
        return res

    def plot(self, label, pos=None ):
        """Plot history at given positions"""
        substat=self.fragment(pos)

        if substat.unity:
            label += " ("+substat.unity+")"

        if substat.stdevs:
            base_line=pyplot.errorbar(pos,substat.means,yerr=substat.stdevs, label=label).lines[0]
        else:
            base_line, = pyplot.plot(substat.means, label=label)

        current_color=base_line.get_color()
        if substat.maxs:
            pyplot.fill_between (pos, substat.maxs, substat.means,alpha=0.3,color=current_color )

        if substat.mins:
            pyplot.fill_between (pos,substat.mins ,substat.means, alpha=0.3, color=current_color)

        
    def __str__(self):
        return self.dump("means", " ", ":")

    def dump(self, label, value_sep, key_sep):
        lines=[label + key_sep + value_sep.join(map(str,self.means))]
        if self.maxs:
            lines.append('-maxs'+key_sep+ value_sep.join(map(str,self.maxs)))
        if self.mins:
            lines.append('-mins'+key_sep+ value_sep.join(map(str, self.mins)))
        if self.stdevs:
            lines.append('-stdevs'+key_sep+ value_sep.join(map(str, self.stdevs)))
        if self.unity:
            lines.append('-unity'+key_sep+ self.unity )
        return '\n'.join(lines)


    def extend(self, other):
        if self.unity != other.unity:
            warn("WARNING, extending keys of different units")
        self.means.extend(other.means)
        self.maxs.extend(other.maxs)
        self.mins.extend(other.mins)
        self.stdevs.extend(other.stdevs)


    def __eq__(self, other):
        return self.__dict__==other.__dict__
        

