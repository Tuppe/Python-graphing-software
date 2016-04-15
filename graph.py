

import sys
from PyQt4 import QtGui, QtCore

from random import randint
from loadfile import Data

class qpen(QtGui.QWidget):
    
    def __init__(self,path):
        super().__init__()
        
        self.initUI()
        self.yoffset=0
        self.gridsize=20
        self.xgridsize=50
        self.ygridsize=60
        self.leftmargin=50
        self.lowmargin=40
        self.path=path
        
        
    def initUI(self):      

        self.setGeometry(300, 300, 280, 170)
        self.show()
        

    def paintEvent(self, e):

        somedata=Data()
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
        self.yoffset=self.height()-self.lowmargin
        
        for y in range(1,data.get_length()):
            color=QtGui.QColor(randint(0,255),randint(0,255),randint(0,255))
            pen = QtGui.QPen(color, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            for x in range(0,len(time)-1):
                x1=time[x]*self.xgridsize+self.leftmargin
                y1=-lines[y][x]+self.yoffset
                x2=time[x+1]*self.xgridsize+self.leftmargin
                y2=-lines[y][x+1]+self.yoffset
                qp.drawLine(x1,y1,x2,y2)
        
    def drawBars(self, qp, data):
        
        pen = QtGui.QPen(QtCore.Qt.red, self.gridsize/2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        
        
        time=data.get_data(0).get_data()
        line=data.get_data(1).get_data()
        line2=data.get_data(2).get_data()
        avg=data.get_data(1).get_avg()
        
        
        self.yoffset=avg/2
        
        print(line)
        
        for x in range(0,len(time)):
            x1=x*self.gridsize+40+self.gridsize/2
            y1=-line[x]+self.yoffset*10
            qp.drawLine(x1,self.yoffset*10,x1,y1)
        
            
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
        
        for y in range(0,50):
            qp.drawLine(startx,starty-y*ygridsize,self.width(),self.height()-self.lowmargin-y*ygridsize)
            
        for x in range(0,50):
            qp.drawLine(startx+x*xgridsize,starty,startx+x*xgridsize,0)
            
        for y in range(0,50):
            qp.drawText(20,starty-y*ygridsize,str(y*ygridsize))
            
        for x in range(0,50):
            qp.drawText(startx+x*xgridsize,starty+20,str(x))
            
        '''
        if type=="LINE":
            #values
            for x in range(4,int(width/xgridsize)+1):
                if (x%2==0):
                    qp.drawText(x*xgridsize,height-xgridsize,str(x-4))
            
            for y in range(0,int(height/ygridsize)):
                if (y%1==0):
                    qp.drawText(10,y*ygridsize+10*self.yoffset,str(-y*ygridsize))
                    qp.drawText(10,-y*ygridsize+10*self.yoffset,str(y*ygridsize))
        
        if type=="BAR":
            print(time)
            #values
            for x in range(0,len(time)):
                qp.drawText(x*gridsize+40,height-gridsize,str(time[x]))
            
            for y in range(0,int(height/gridsize)):
                if (y%1==0):
                    qp.drawText(10,y*gridsize+10*self.yoffset,str(-y*gridsize))
                    qp.drawText(10,-y*gridsize+10*self.yoffset,str(y*gridsize))
        '''
            
'''      
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    exd = qpen("data_ok2.csv")
    sys.exit(app.exec_())
'''