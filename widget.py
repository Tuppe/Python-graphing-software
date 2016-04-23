
import sys
from PyQt4 import QtGui, QtCore

from loadfile import Data


class PieWidget(QtGui.QWidget):
  
    def __init__(self):      
        super(PieWidget, self).__init__()
        self._size=200
        self.setMinimumSize(self._size, self._size/2)
        
    def paintEvent(self, e):
      
        self.somedata=Data()
        somedata=self.somedata
        type=somedata.load('data_pie.csv')
        
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPie(qp,somedata)
        qp.end()
      
            
    def drawPie(self,qp,data):

        datalen=data.get_data(1).get_sum()
        
        piedata=[]
        piesum=0
        piesize=self._size
        
        #get data and normalize it to 5760
        for x in range(0,data.get_data(1).get_len()):
            piedata.append(data.get_data(1).get_data()[x]/datalen*5760)
        
        piedata.sort(reverse=True)
        
        #draw pie
        for p in range(0,20):
            for x in range(0,data.get_data(1).get_len()):
                color=QtGui.QColor.fromHsvF(1/data.get_data(1).get_len()*x,0.9,0.9,1)
                qp.setBrush(color)
                qp.setPen(color)
                qp.drawPie(0,20-p,piesize,piesize/2,piesum,piedata[x])
                
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
            datalen=data.get_data(1).get_sum()
            piedata=[]
            
            #get data for sorting and normalize it to 5760
            for x in range(0,data.get_data(1).get_len()):
                piedata.append(data.get_data(1).get_data()[x]/datalen*5760)
            
            piedata.sort(reverse=True)
            
            #draw pie
            for x in range(0,data.get_data(1).get_len()):
                color=QtGui.QColor.fromHsvF(1/data.get_data(1).get_len()*x,0.9,0.9,1) #generate colors
                
                qf = QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold)
                qp.setFont(qf)
                qp.setPen(QtCore.Qt.black)
                qp.drawText(40,25+30*x,'{:.1f}'.format(piedata[x]/57.6)+" % - "+data.get_data(0).get_data()[x])
                
                qp.fillRect(0,10+30*x,30,20,color)
        
        if self.type=='LINE' or self.type=='BAR':
            
            #draw pie
            for x in range(0,data.get_length()-1):
                color=QtGui.QColor.fromHsvF(1/data.get_length()*x,0.9,0.9,1) #generate colors
                
                qf = QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold)
                qp.setFont(qf)
                qp.setPen(QtCore.Qt.black)
                qp.drawText(40,25+30*x,'{:s}'.format(data.get_data(x+1).get_name()))
                
                qp.fillRect(0,10+30*x,30,20,color)