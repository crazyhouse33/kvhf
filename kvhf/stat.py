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

    def plot(self, label ):
        """Plot history with given label"""
        if self.unity:
            label += " ("+self.unity+")"
        if self.stdevs:
            base_line=pyplot.errorbar(range(len(self.means)), self.means, yerr=self.stdevs, label=label).lines[0]
        else:
            base_line, = pyplot.plot(self.means, label=label)


        current_color=base_line.get_color()




        if self.maxs:
            pyplot.fill_between (range(len(self.means)), self.maxs, self.means,alpha=0.3,color=current_color )

        if self.mins:
            pyplot.fill_between (range(len(self.means)), self.mins, self.means,alpha=0.3, color=current_color)

        
    def __str__(self):
        lines=["means:"+ " ".join(map(str,self.means)),
                "maxs:"+" ".join(map(str,self.maxs)),
                "mins:"+" ".join(map(str,self.mins)),
                "stdevs:"+" ".join(map(str,self.stdevs))
                ]
        return '\n'.join(lines)

    def extend(self, other):
        self.means.extend(other.means)
        self.maxs.extend(other.maxs)
        self.mins.extend(other.mins)
        self.stdevs.extend(other.stdevs)


    def __eq__(self, other):
        return self.__dict__==other.__dict__
        

