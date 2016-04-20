'''
Created on 25.2.2016

@author: Tuomas
'''

from PyQt4 import QtGui
from random import randint

class Data(object):
    
    
    def __init__(self):
        self.data=0
        self.length=0
        
    def load(self, path):
        
        if path==0:
            return 0
        try:
            file = open(path)
        except(FileNotFoundError):
            file.close()
            return 0
        
        data=[]
        
        for line in file:
            readline=line.strip().split(';')
            data.append(readline)
        
        store=[]
        newlist=[]
        
        type=data[len(data)-1][0]
        
        for y in range(0,len(data[0])):
            for x in range(0,len(data)-1):
                if x==0:
                    newlist.append(data[x][y]) #axis name
                else:
                    if type=="LINE":
                        if data[x][y].lstrip("-+").isnumeric()==1:
                            newlist.append(int(data[x][y])) #valid data
                        else:
                            file.close()
                            return 0 #invalid data
                        
                    if type=="BAR" or type=="PIE":
                        if y==0:
                            newlist.append(data[x][y]) #valid data
                        else:
                            newlist.append(int(data[x][y])) #valid data
                        
                        
            newline=Line(newlist)
            store.append(newline)
            newlist=[]
            
        self.data=store
        self.length=len(store)
        
        file.close()
        return type
    
    def get_data(self,index):
        return self.data[index]
        
    def get_length(self):
        return self.length
    
class Line:
    
    def __init__(self, datalist):
        self._data=datalist
        self._name=datalist[0]
        datalist.pop(0)
        #print(datalist)
        #self._max=max(datalist)
        #self._min=min(datalist)
        
    
    def get_data(self):
        return self._data
    
    def get_name(self):
        return self._name
    
    def get_min(self):
        return self._min
    
    def get_max(self):
        return self._max
    
    def get_len(self):
        return len(self._data)
    
    def get_sum(self):
        asum=0
        try:
            for x in range(0,len(self._data)):
                asum+=self._data[x]
        except(TypeError):
            return -1
        
        return asum
    
    def get_avg(self):
        asum=0
        
        try:
            for x in range(0,len(self._data)):
                asum+=self._data[x]
        except(TypeError):
            return -1
        
        if len(self._data)==0:
            return -1
        
        return asum/len(self._data)
        
        
        