

import sys
from PyQt4 import QtGui, QtCore

from random import randint
from loadfile import Data

class qpen(QtGui.QWidget):
    
    def __init__(self,path):
        super().__init__()
        
        self.initUI()
        self.yoffset=0
        self.gridsize=10
        self.path=path
        
        
    def initUI(self):      

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Grapher Pro 8000')
        self.show()
        

    def paintEvent(self, e):

        somedata=Data()
        type=somedata.load(self.path)
        #print(self.path)
        #print(somedata)
        #if (type==0):
            #print("poor file")
        
        qp = QtGui.QPainter()
        qp.begin(self)
        
        if type!=0:
            self.drawGrid(qp, somedata, type)
            
            if type=="LINE":
                self.drawLines(qp, somedata)
            if type=="BAR":
                self.drawBars(qp, somedata)
        
        qp.end()
        
    def drawLines(self, qp, data):
        
        lines=[]
        
        for x in range(0,data.get_length()):
            lines.append(data.get_data(x).get_data())
        
        time=lines[0]
        
        line=data.get_data(1).get_data()
        
        avg=data.get_data(1).get_avg()
        self.yoffset=20
        
        for y in range(1,data.get_length()):
            color=QtGui.QColor(randint(0,255),randint(0,255),randint(0,255))
            pen = QtGui.QPen(color, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            for x in range(0,len(time)-1):
                x1=time[x]*10+40
                y1=-lines[y][x]+self.yoffset*10
                x2=time[x+1]*10+40
                y2=-lines[y][x+1]+self.yoffset*10
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
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DotLine)
        qp.setPen(pen)
        
        #grid lines
        #40 - 1
        #20 - 2
        #10 - 4
        
        
        width=self.width()
        height=self.height()
        
        for x in range(4,int(width/gridsize)+1):
            qp.drawLine(x*gridsize,0,x*gridsize,height-gridsize*2)
        
        for y in range(0,int(height/gridsize)-1):
            qp.drawLine(40,y*gridsize,width,y*gridsize)
        
        if type=="LINE":
            #values
            for x in range(4,int(width/gridsize)+1):
                if (x%2==0):
                    qp.drawText(x*gridsize,height-gridsize,str(x-4))
            
            for y in range(0,int(height/gridsize)):
                if (y%1==0):
                    qp.drawText(10,y*gridsize+10*self.yoffset,str(-y*gridsize))
                    qp.drawText(10,-y*gridsize+10*self.yoffset,str(y*gridsize))
        
        
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
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    exd = qpen("data_ok2.csv")
    sys.exit(app.exec_())
'''