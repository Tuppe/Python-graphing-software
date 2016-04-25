
import sys
from PyQt4 import QtGui, QtCore

from loadfile import Data

class PieWidget(QtGui.QWidget):
  
    def __init__(self,data,style):      
        super(PieWidget, self).__init__()
        self.setMinimumSize(200,200)
        self.data=data
        self.piesize=self.height()-80
        self.style=style
        
    def paintEvent(self, e):
      
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing,True) #smoothing
        self.drawPie(qp,self.data)
        qp.end()
    
    #change between 2D and 3D
    def changeStyle(self,style):
        self.style=style
        self.update()
        
    def drawPie(self,qp,data):

        datalen=data.get_datalist(1).get_sum()
        
        piedata=[]
        piesum=0
        
        if self.style==1:
            halfer=2
            thickness=20
        else:
            halfer=1
            thickness=1
        
        #get data for sorting and normalize it with 5760
        for x in range(0,data.get_datalist(1).get_len()):
            piedata.append(data.get_datalist(1).get_data()[x]/datalen*5760)
        
        piedata.sort(reverse=True)
        
        #Draw pie
        for p in range(0,thickness):
            for x in range(0,data.get_datalist(1).get_len()):
                if p==thickness-1:
                    #top of the pie
                    color=QtGui.QColor.fromHsvF(1/data.get_datalist(1).get_len()*x,0.9,0.9,1)
                else:
                    #3D side with fade color
                    color=QtGui.QColor.fromHsvF(1/data.get_datalist(1).get_len()*x,0.9,(0.3/thickness)*p+0.5,1)
                
                #draw pie without outlines
                qp.setBrush(color)
                qp.setPen(color)
                
                #push out small percentages from pie for readability
                if (piedata[x]/57.6)<1:
                    piesize=self.piesize+x
                else:
                    piesize=self.piesize
                    
                qp.drawPie(piesize/5,piesize/10-p,piesize,piesize/halfer,piesum,piedata[x])
                
                piesum+=piedata[x]

class LegendWidget(QtGui.QWidget):
  
    def __init__(self,data,type):      
        super(LegendWidget, self).__init__()
        self.setMinimumSize(100, 100)
        self.data=data
        self.type=type
        
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLegend(qp,self.data)
        qp.end()
          
    def drawLegend(self,qp,data):

        if self.type=='PIE':
            datalen=data.get_datalist(1).get_sum()
            piedata=[]
            
            #get data for sorting and normalize it to 5760
            for x in range(0,data.get_datalist(1).get_len()):
                piedata.append(data.get_datalist(1).get_data()[x]/datalen*5760)
            
            piedata.sort(reverse=True)
            
            #draw pie
            for x in range(0,data.get_datalist(1).get_len()):
                color=QtGui.QColor.fromHsvF(1/data.get_datalist(1).get_len()*x,0.9,0.9,1) #generate colors
                
                qf = QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold)
                qp.setFont(qf)
                qp.setPen(QtCore.Qt.black)
                qp.drawText(40,25+30*x,'{:.1f}'.format(piedata[x]/57.6)+" % - "+data.get_datalist(0).get_data()[x])
                
                #Color rectangles
                qp.fillRect(0,10+30*x,30,20,color)
        
        if self.type=='LINE' or self.type=='BAR':
            
            #draw pie
            for x in range(0,data.get_length()-1):
                color=QtGui.QColor.fromHsvF(1/data.get_length()*x,0.9,0.9,1) #generate colors
                
                qf = QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold)
                qp.setFont(qf)
                qp.setPen(QtCore.Qt.black)
                qp.drawText(40,25+30*x,'{:s}'.format(data.get_datalist(x+1).get_name()))
                
                qp.fillRect(0,10+30*x,30,20,color)
                
    
class DataWidget(QtGui.QWidget):
  
    def __init__(self,data,type):
        super(DataWidget, self).__init__()
        self.setMinimumSize(100, 100)
        self.data=data
        self.type=type
        
    def paintEvent(self, e):
        
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawData(qp,self.data)
        qp.end()
          
    def drawData(self,qp,data):
        qp.drawText(10,10,'Average {:.1f}'.format(data.get_avg()))
        qp.drawText(10,25,'Max {:.1f}'.format(data.get_max()))
        qp.drawText(10,40,'Min {:.1f}'.format(data.get_min()))


class TextWidget(QtGui.QWidget):
  
    def __init__(self,path,text,color):
        super(TextWidget, self).__init__()
        self.setMinimumSize(100, 100)
        self.path=path
        self.text=text
        self.color=color
        
    def paintEvent(self, e):
        
        qp = QtGui.QPainter()
        qp.begin(self)
        qf = QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold)
        qp.setFont(qf)
        qp.setPen(self.color)
        qp.drawText(0,40,self.text.format(self.path))
        qp.end()
