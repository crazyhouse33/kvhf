from warnings import warn
from collections import defaultdict

import matplotlib.pyplot as pyplot
pyplot.style.use('seaborn-dark')


all_series_attributes=['maxs','mins','stdevs']
#WARNING Keep means first
all_serie= ['means']+all_series_attributes


def filter_out_Nones(liste,pos):
    posx=[]
    values=[]
    for position in pos:
        value=liste[position] if position<len(liste) else None 
        if value!=None:
            posx.append(position)
            values.append(value)
    return posx, values




class Serie_stats:
    def pad_list(liste, wanted_len,left=True,padder=None):
        """Remove end items till reaching wanted_len if too big.
           prepend None  till reaching wanted_len if too small.
        """

        diff =  wanted_len -len(liste) 
        if diff==0:
            return liste

        if diff>0:
            if left:
                res=[padder]*diff + liste
            else:
                res= liste+ [padder]*diff
            return res
        else:
            return liste[:wanted_len]

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
        for attribute in all_serie:
            the_list=getattr(self,attribute)
            size= len(the_list)
            setattr(res,attribute, [the_list[i] for i in pos if i < size])
            
        res.unity=self.unity
        return res


    def plot(self, label, pos ):
        """Plot history at given positions, remove None entries from drawing"""

        substat=self.fragment(pos) # Taking subpart of pos
        substat.re_equilibrate() # Fixing label misagnilement 

        posmeans, means= filter_out_Nones(substat.means, pos) 

        base_line, = pyplot.plot(posmeans,means,marker='o', label=label)
        current_color=base_line.get_color()

        if substat.unity:
            label += " ("+substat.unity+")"


        posbars, stdevs= filter_out_Nones(substat.stdevs, posmeans)
        bar_means= [means[i] for i in posbars]
        base_line=pyplot.errorbar(posbars,bar_means,yerr=stdevs, capsize=2,fmt='none', color= current_color).lines[0]
        

        posmax, maxs= filter_out_Nones(substat.maxs, posmeans)
        max_means= [means[i] for i in posmax]
        pyplot.fill_between (posmax, maxs, max_means,alpha=0.15,color=current_color )

        posmin, mins= filter_out_Nones(substat.mins, posmeans)
        min_means= [means[i] for i in posmin]
        pyplot.fill_between (posmin, mins, min_means,alpha=0.15,color=current_color )


        
    def __str__(self):
        return self.dump("means", " ", ":")

    def dump_filter(self, value, void_str):
        if value==None:
            return void_str
        else:
            return str(value)


    def dump(self, label, value_sep, key_sep, void_str):
        lines=[label + key_sep + value_sep.join([self.dump_filter(value, void_str) for value in self.means])]
        
        
        for attribute in all_series_attributes:
            atr_list=getattr(self, attribute)
            if atr_list:
                lines.append('-'+attribute+key_sep+ value_sep.join(map(str,atr_list)))
        if self.unity:
            lines.append('-unity'+key_sep+ self.unity )
        return '\n'.join(lines)

    def desequilibred_attributes(self):
        """Return attributes than dont have same size as the means"""
        all_serie_lists=[getattr(self,attribute) for attribute in all_series_attributes]
        lens=map(len, all_serie_lists)
        mixed= zip(all_serie, all_serie_lists, lens)

        return [serie for serie in mixed if serie[2] != 0 and serie[2] !=len(self)  ]



    def re_equilibrate(self):
        """Align attributes with size. Append None on right"""
        desequilibred = self.desequilibred_attributes()
        for attribute in desequilibred:
            setattr(self,attribute[0],Serie_stats.pad_list(attribute[1], len(self), left=False)) 

    def __len__(self):
        return len(self.means)
    



    def mathematic_impossibilities(self):
        """Here goes some check about attributes, for exemple min should always be smaller that mean and stuff like that and return a string about everything"""
        wrong=[]
        len_wanted= len(self.means)
        stdevs_list = Serie_stats.pad_list(self.stdevs, len_wanted)
        mins_list = Serie_stats.pad_list(self.mins, len_wanted)
        maxs_list = Serie_stats.pad_list(self.maxs, len_wanted)
        for i in range(len_wanted):
            mean = self.means[i]
            stdevs= stdevs_list[i]
            mins = mins_list[i]
            maxs= maxs_list[i] 
            if mean==None:# Every check is based on mean
                continue

            if maxs!=None:
                if maxs<mean:
                    wrong.append( i, "Attribute max = {} is smaller than the mean ={}".format(maxs,mean))
                if mins!=None:
                    if maxs==mean!=mins:
                        wrong.append(i, "Attribute max = {} is equal to mean ={}, but min = {} is different".format(maxs,mean,mins))
                if stdevs!=None:
                    if maxs==mean and stdevs!=0:
                        wrong.append(i, "Attribute max = {} is equal to mean ={} but stdevs = {} is different than 0".format(maxs, mean, stdevs))

            if mins!=None:
                if mins>mean:
                    wrong.append(i,"Attribute min = {} is bigger than the mean ={}".format(mins,mean))

            if stdevs!=None:
                if mins==mean and stdevs!=0:
                    wrong.append(i,"Attribute min= {} is equal to mean ={} but stdevs = {} is different than 0".format(mins,mean,stdevs))

        return wrong




    def extend(self, other):
        if self.unity != other.unity:
            warn("WARNING, extending keys of different units")
        self.means.extend(other.means)
        self.maxs.extend(other.maxs)
        self.mins.extend(other.mins)
        self.stdevs.extend(other.stdevs)


    def __eq__(self, other):
        return self.__dict__==other.__dict__
        

