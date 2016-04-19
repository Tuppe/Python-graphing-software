

import sys
from PyQt4 import QtGui, QtCore

import random
from loadfile import Data

class qpen(QtGui.QWidget):
    
    def __init__(self,path):
        super().__init__()
        
        self.initUI()
        self.xgridsize=50
        self.ygridsize=25
        self.yscale=1
        self.leftmargin=50
        self.lowmargin=40
        self.yoffset=0
        self.xoffset=1
        self.path=path
        
    def initUI(self):
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        self.show()
        
    def mousePressEvent(self, event):
        super(qpen, self).mousePressEvent(event)
        self.button=event.button()
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
        
        if self.button==1:
            self.yoffset+=y-self.ystart
            self.xoffset+=x-self.xstart
            
        if self.button==2:
            self.ygridsize-=int((y-self.ystart)/2)
            self.xgridsize+=int((x-self.xstart)/2)
            if self.ygridsize<5:
                self.ygridsize=5
            if self.xgridsize<5:
                self.xgridsize=5
                
        if self.button==4:
            self.yscale-=(y-self.ystart)/100
            if self.yscale<1:
                self.yscale=1
        
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
        qp.setRenderHint(QtGui.QPainter.Antialiasing,True)
        
        if type!=0:
            if type!="PIE":
                self.drawGrid(qp, somedata, type)
            
            if type=="LINE":
                self.drawLines(qp, somedata)
            if type=="BAR":
                self.drawBars(qp, somedata)
            if type=="PIE":
                self.drawPie(qp, somedata)
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
            color=QtGui.QColor.fromHsvF(1/data.get_data(1).get_len()*y,0.9,0.9,0.9)
            pen = QtGui.QPen(color, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            
            for x in range(0,len(time)-1):
                x1=time[x]*self.xgridsize+self.leftmargin+self.xoffset
                y1=-lines[y][x]+self.height()-self.lowmargin+self.yoffset
                x2=time[x+1]*self.xgridsize+self.leftmargin+self.xoffset
                y2=-lines[y][x+1]+self.height()-self.lowmargin+self.yoffset
                qp.drawLine(x1,y1,x2,y2)
        
    def drawBars(self, qp, data):
        
        pen = QtGui.QPen(QtCore.Qt.black, 5, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        
        time=data.get_data(0).get_data()
        line=data.get_data(1).get_data()
        
        avg=data.get_data(1).get_avg()
        
        
        #Draw bars
        for x in range(0,len(time)):
            x1=x*self.xgridsize+self.leftmargin+self.xoffset
            y1=self.height()-self.lowmargin+self.yoffset
            
            qp.fillRect(x1+1,y1,self.xgridsize-2,-line[x]*self.yscale,QtCore.Qt.blue)
        
    def drawPie(self,qp,data):

        datalen=data.get_data(1).get_sum()
        
        piedata=[]
        piesum=0
        piesize=self.height()-80
        
        #get data and normalize it to 5760
        for x in range(0,data.get_data(1).get_len()):
            piedata.append(data.get_data(1).get_data()[x]/datalen*5760)
        
        piedata.sort(reverse=True)
        
        #draw pie
        for p in range(0,30):
            for x in range(0,data.get_data(1).get_len()):
                color=QtGui.QColor.fromHsvF(1/data.get_data(1).get_len()*x,0.9,0.9,1)
                qp.setBrush(color)
                qp.setPen(color)
                qp.drawPie(piesize/5,self.height()/2-piesize/3-p,piesize,piesize/2,piesum,piedata[x])
                
                piesum+=piedata[x]
                
                qp.fillRect(self.width()/2,10+30*x,30,20,color)
                
                if p==0:
                    qf = QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold)
                    qp.setFont(qf)
                    qp.setPen(QtCore.Qt.black)
                    qp.drawText(self.width()/2+40,25+30*x,'{:.1f}'.format(piedata[x]/57.6)+" % - "+data.get_data(0).get_data()[x])
                
        
        #title label
        qf = QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold)
        qp.setFont(qf)
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 5, QtCore.Qt.SolidLine))
        qp.drawText(self.width()/2,self.height()-5,str(data.get_data(1).get_name()))
        
            
        
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
        
        if self.xoffset>0:
            xmin=xmin-1
        
        if self.yoffset>0:
            ymin=ymin+1
            
        ##LINES##
        #horizontal
        for y in range(ymin,ymax):
            x1=self.leftmargin
            y1=starty-y*ygridsize+self.yoffset
            x2=self.width()
            y2=self.height()-self.lowmargin-y*ygridsize+self.yoffset
            qp.drawLine(x1,y1,x2,y2)
            qp.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
            qp.drawLine(x1-6,y1,self.leftmargin,y2) #short value guidelines
            qp.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DotLine))
        
        #vertical
        for x in range(xmin,xmax):
            xpos=self.leftmargin+x*xgridsize+self.xoffset
            qp.drawLine(xpos,starty,xpos,0)
        
        #draw sold axes
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 1.5, QtCore.Qt.SolidLine))
        qp.drawLine(self.leftmargin,starty,self.leftmargin,0) #left limiter
        #qp.drawLine(self.leftmargin+self.xoffset,starty,self.leftmargin+self.xoffset,0) #starting axis
        qp.drawLine(self.leftmargin,starty+self.yoffset,self.width(),self.height()-self.lowmargin+self.yoffset) #zero line
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DotLine))
        
        ##TEXT##
        #horizontal
        
        if type=='LINE':
            for x in range(xmin,xmax):
                xpos=self.leftmargin+x*xgridsize+self.xoffset
                qp.drawText(xpos,starty+20,str(x))
        
        if type=='BAR':
            if xmin<0:
                xmin=0
            for x in range(xmin,len(time.get_data())):
                xpos=self.leftmargin+x*xgridsize+self.xoffset
                qp.drawText(xpos,starty+20,str(time.get_data()[x]))
        
        #vertical
        for y in range(ymin,ymax):
            qp.drawText(20,starty-y*ygridsize+self.yoffset+5,str(y*ygridsize))
        
        
        ##TITLES##
        #horizontal
        qp.drawText(self.width()/2,self.height()-5,str(time.get_name()))
        
        #vertical
        self.rotated_text(qp,15,self.height()/2,str(self.somedata.get_data(1).get_name()))
        
    def rotated_text(self,qp,x,y,text):
        qp.translate(x,y)
        qp.rotate(-90)
        qp.drawText(0,0,text)
        qp.rotate(90)
        qp.translate(-x,-y)
            
            
'''      
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    exd = qpen("data_ok2.csv")
    sys.exit(app.exec_())
'''