

import sys
from PyQt4 import QtGui, QtCore

from random import randint
from loadfile import Data

class qpen(QtGui.QWidget):
    
    def __init__(self,path):
        super().__init__()
        
        self.initUI()
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
        
        #Draw line graph from X and Y coordinates
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
        
        pen = QtGui.QPen(QtCore.Qt.black, thickness, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        
        time=data.get_data(0).get_data()
        line=data.get_data(1).get_data()
        
        avg=data.get_data(1).get_avg()
        
        
        #Draw bars
        for x in range(0,len(time)):
            x1=x*self.xgridsize+self.leftmargin+self.xgridsize/2+self.xoffset
            y1=self.height()-self.lowmargin-thickness/2+self.yoffset
            
            qp.fillRect(x1-self.xgridsize/2+5,y1,self.xgridsize-10,-line[x],QtCore.Qt.green)
        
        
    def drawGrid(self, qp, data, type):
        
        time=data.get_data(0)
        line=data.get_data(1)
        
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DotLine)
        qp.setPen(pen)
        
        xgridsize=self.xgridsize
        ygridsize=self.ygridsize
        
        starty=self.height()-self.lowmargin
        
        #drawing range
        ymin=int(self.yoffset/ygridsize)
        xmin=int(-self.xoffset/xgridsize)+1
        ymax=int(self.yoffset/ygridsize)+int(self.height()/self.ygridsize)
        xmax=int(-self.xoffset/xgridsize)+int(self.width()/self.xgridsize)
        
        
        ##LINES##
        #horizontal
        for y in range(int(self.yoffset/ygridsize),ymax):
            qp.drawLine(self.leftmargin,starty-y*ygridsize+self.yoffset,self.width(),self.height()-self.lowmargin-y*ygridsize+self.yoffset)
        
        #vertical
        for x in range(xmin,xmax):
            xpos=self.leftmargin+x*xgridsize+self.xoffset
            qp.drawLine(xpos,starty,xpos,0)
        
        ##TEXT##
        #horizontal
        if type=='LINE':
            for x in range(xmin-1,xmax):
                xpos=self.leftmargin+x*xgridsize+self.xoffset
                qp.drawText(xpos,starty+20,str(x))
                
        if type=='BAR':
            for x in range(xmin-1,len(time.get_data())):
                xpos=self.leftmargin+x*xgridsize+self.xoffset
                qp.drawText(xpos,starty+20,str(time.get_data()[x]))
        
        #vertical
        for y in range(ymin,ymax):
            qp.drawText(20,starty-y*ygridsize+self.yoffset+5,str(y*ygridsize))
            
        ##TITLES##
        #horizontal
        qp.drawText(self.width()/2,self.height()-5,str(time.get_name()))
        
        #vertical
        qp.translate(15,self.height()/2)
        qp.rotate(-90)
        qp.drawText(0,0,str(line.get_name()))
        qp.rotate(90)
        qp.translate(-15,-self.height()/2)
        
        
        
            
            
'''      
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    exd = qpen("data_ok2.csv")
    sys.exit(app.exec_())
'''