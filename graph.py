

import sys
from PyQt4 import QtGui, QtCore

from random import randint
from loadfile import Data

class qpen(QtGui.QWidget):
    
    def __init__(self,path):
        super().__init__()
        
        self.initUI()
        self.gridsize=20
        self.xgridsize=50
        self.ygridsize=10
        self.leftmargin=50
        self.lowmargin=40
        self.yoffset=0
        self.xoffset=0
        self.path=path
        
    def initUI(self):
        self.show()
        
    def mousePressEvent(self, event):
        super(qpen, self).mousePressEvent(event)
        #get global window position when mouse pressed
        self.xstart=event.globalX()
        self.ystart=event.globalY()
    
    def mouseDoubleClickEvent(self, event):
        super(qpen, self).mouseDoubleClickEvent(event)
        #reset offset
        self.yoffset=0
        self.xoffset=0
        self.update()
        
    def mouseMoveEvent(self, event):
        super(qpen, self).mouseMoveEvent(event)
        #track mouse dragging
        x=event.globalX()
        y=event.globalY()
        self.yoffset+=y-self.ystart
        self.xoffset+=x-self.xstart
        
        if self.xoffset>0:
            self.xoffset=0
        
        #reset offset counter
        self.ystart=y
        self.xstart=x
        self.update() #update graph
        
    def paintEvent(self, e):

        self.somedata=Data()
        somedata=self.somedata
        type=somedata.load(self.path)
        #print(self.path)
        #print(somedata)
        
        qp = QtGui.QPainter()
        qp.begin(self)
        
        if type!=0:
            self.drawGrid(qp, somedata, type)
            
            if type=="LINE":
                self.drawLines(qp, somedata)
            if type=="BAR":
                self.drawBars(qp, somedata)
        else:
            print("poor file")
        

        qp.end()
        
    def drawLines(self, qp, data):
        
        lines=[]
        
        for x in range(0,data.get_length()):
            lines.append(data.get_data(x).get_data())
        
        time=lines[0]
        
        line=data.get_data(1).get_data()
        
        avg=data.get_data(1).get_avg()
        
        for y in range(1,data.get_length()):
            color=QtGui.QColor(randint(0,255),randint(0,255),randint(0,255))
            pen = QtGui.QPen(color, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            for x in range(0,len(time)-1):
                x1=time[x]*self.xgridsize+self.leftmargin+self.xoffset
                y1=-lines[y][x]+self.height()-self.lowmargin+self.yoffset
                x2=time[x+1]*self.xgridsize+self.leftmargin+self.xoffset
                y2=-lines[y][x+1]+self.height()-self.lowmargin+self.yoffset
                qp.drawLine(x1,y1,x2,y2)
        
    def drawBars(self, qp, data):
        
        thickness=2
        
        pen = QtGui.QPen(QtCore.Qt.red, thickness, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        
        time=data.get_data(0).get_data()
        line=data.get_data(1).get_data()
        #line2=data.get_data(2).get_data()
        avg=data.get_data(1).get_avg()
        
        for x in range(0,len(time)):
            x1=x*self.xgridsize+self.leftmargin+self.xgridsize/2+self.xoffset
            y1=self.height()-self.lowmargin-thickness/2+self.yoffset
            y2=-line[x]+self.height()-self.lowmargin+thickness/2+self.yoffset
                
            print(line[x])
            qp.drawLine(x1,y1,x1,y2)
        
            
    def drawGrid(self, qp, data, type):
        
        time=data.get_data(0).get_data()
        
        gridsize=self.gridsize
        xgridsize=self.xgridsize
        ygridsize=self.ygridsize
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DotLine)
        qp.setPen(pen)
        
        #grid lines
        #40 - 1
        #20 - 2
        #10 - 4
        
        width=self.width()
        height=self.height()
        
        startx=self.width()-self.width()+self.leftmargin
        starty=self.height()-self.lowmargin
        
        yrange=int(self.yoffset/ygridsize)+int(self.height()/self.ygridsize)
        xrange=int(-self.xoffset/xgridsize)+int(self.width()/self.xgridsize)
        
        #LINES
        #horizontal
        for y in range(int(self.yoffset/ygridsize),yrange):
            qp.drawLine(startx,starty-y*ygridsize+self.yoffset,self.width(),self.height()-self.lowmargin-y*ygridsize+self.yoffset)
        
        #vertical
        for x in range(int(-self.xoffset/xgridsize)+1,xrange):
            qp.drawLine(startx+x*xgridsize+self.xoffset,starty,startx+x*xgridsize+self.xoffset,0)
        
        #TEXT
        #horizontal
        for x in range(int(-self.xoffset/xgridsize)+1,xrange):
            qp.drawText(startx+x*xgridsize+self.xoffset,starty+20,str(x))
            
        #vertical
        for y in range(int(self.yoffset/ygridsize),yrange):
            qp.drawText(20,starty-y*ygridsize+self.yoffset,str(y*ygridsize))
            
            
            
'''      
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    exd = qpen("data_ok2.csv")
    sys.exit(app.exec_())
'''