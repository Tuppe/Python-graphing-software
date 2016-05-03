'''
Created on 25.2.2016

@author: Tuomas
'''

class DataList(object):
    def __init__(self):
        super(DataList,self).__init__()
        self.data=0
        self.length=0
        self._maxname=0
        
    def load(self, path):
        
        if path==0:
            return 0 #cancel
        try:
            file = open(path)
        except(IOError):
            return 0 #not found
        
        data=[]
        
        #parse file
        for line in file:
            readline=line.strip().split(';')
            data.append(readline)
        
        full_list=[]
        newlist=[]
        self._maxname=0
        
        #data layout:
        #[len(data)-1][0] - last row first column: data type
        #[0][y] - first row: graph names
        #[x][0] - first column: vertical axle names
        
        type=data[len(data)-1][0] #read data type from the last cell


        if type=="LINE":
            for y in range(0,len(data[0])):
                newlist.append(data[0][y]) #graph names

                for x in range(1,len(data)-1):
                    #check for invalid data
                    try: #Linux
                        datachk=data[x][y].lstrip("-+").decode('utf-8').isnumeric()
                    except(AttributeError): #Windows
                        datachk=data[x][y].lstrip("-+").isnumeric()
                    
                    if datachk==0:
                        file.close()
                        return 0 #data error
                    
                    newlist.append(int(data[x][y]))
                        
                newline=Line(newlist)
                full_list.append(newline)
                newlist=[]
            
        elif type=="BAR" or type=="PIE":
            for y in range(0,len(data[0])):
                newlist.append(data[0][y]) #graph names
                
                for x in range(1,len(data)-1):
                    if y==0:
                        newlist.append(data[x][0])
                        if len(data[x][0])>self._maxname:
                            self._maxname=len(data[x][0])
                    else:
                        newlist.append(int(data[x][y]))
                        
                newline=Line(newlist)
                full_list.append(newline)
                newlist=[]
        else:
            file.close()
            return 0 #empty file
        
        self.data=full_list
        self.length=len(full_list)
        
        file.close()
        return type
    
    def get_datalist(self,index):
        return self.data[index]
        
    def get_avg(self):
        asum=0
        
        try:
            for x in range(1,self.get_length()):
                asum+=self.get_datalist(x).get_avg()
        except(TypeError):
            return -1
        
        return asum/(self.get_length()-1)
    
    def get_min(self):
        _min=self.get_datalist(1).get_min()
        
        try:
            for x in range(1,self.get_length()):
                if self.get_datalist(x).get_min()<_min:
                    _min=self.get_datalist(x).get_min()
        except(TypeError):
            return -1
        
        return _min
    
    def get_max(self):
        _max=self.get_datalist(1).get_max()
        
        try:
            for x in range(1,self.get_length()):
                if self.get_datalist(x).get_max()>_max:
                    _max=self.get_datalist(x).get_max()
        except(TypeError):
            return -1
        
        return _max
    
    def get_duration(self):
        return self.get_datalist(0).get_len()
    
    def get_length(self):
        return self.length
    
    def get_maxname(self):
        return self._maxname
    
class Line:
    
    def __init__(self, datalist):
        self._data=datalist
        self._name=datalist[0]
        datalist.pop(0)
        self._max=max(datalist)
        self._min=min(datalist)
        self._visible=1
    
    def set_visibility(self,state):
        self._visible=state
    
    def is_visible(self):
        return self._visible
        
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
        
        
