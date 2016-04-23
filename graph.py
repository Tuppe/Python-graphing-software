

import sys
from PyQt4 import QtGui, QtCore

import random
from loadfile import Data

class qpen(QtGui.QWidget):
    
    def __init__(self,data,type):
        super().__init__()
        
        self.initUI()
        self.xscale=50
        self.ygridsize=25
        self.xgridsize=25
        self.showxgrid=1
        self.showygrid=1
        self.yscale=1
        self.leftmargin=50
        self.lowmargin=40
        self.yoffset=0
        self.xoffset=1
        self.somedata=data
        self.datatype=type
        self.xtitle=str(self.somedata.get_data(0).get_name())
        self.ytitle=str(self.somedata.get_data(1).get_name())
        
        self.min_xscale=1
        self.min_yscale=0.1
        self.min_ygridsize=1
        self.min_xgridsize=1
        
        self.max_xscale=200
        self.max_yscale=10
        self.max_ygridsize=500
        self.max_xgridsize=50
        
        
        if self.datatype=='BAR':
            self.lowmargin=self.somedata.get_maxname()*6
        
    def initUI(self):
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        self.show()
    
    def toggle_ygrid(self):
        self.showxgrid=1-self.showxgrid
        self.update()
        
    def toggle_xgrid(self):
        self.showygrid=1-self.showygrid
        self.update()
        
    def set_yname(self,yname):
        self.ytitle=yname
        
    def set_xname(self,xname):
        self.xtitle=xname
        
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
        self.yscale=1
        self.update()
        
    def wheelEvent(self, event):
        super(qpen, self).wheelEvent(event)
        if event.delta()>0: #wheel up
            self.yscale+=0.2
            self.xscale+=5
        if event.delta()<0: #wheel down
            if self.yscale>.1 and self.xscale>10:
                self.yscale-=0.2
                self.xscale-=5
            
        self.update() #update graph
            
        
    def mouseMoveEvent(self, event):
        super(qpen, self).mouseMoveEvent(event)
        
        #track mouse dragging
        x=event.globalX()
        y=event.globalY()
        
        if self.button==1: #mouse1
            self.yoffset+=y-self.ystart
            self.xoffset+=x-self.xstart
            
        if self.button==4: #middle click
            self.xgridsize-=int((x-self.xstart)/2)
            self.ygridsize-=int((y-self.ystart)/2)
            
            #set limits
            if self.xgridsize<self.min_xgridsize:
                self.xgridsize=self.min_xgridsize
            if self.ygridsize<self.min_ygridsize:
                self.ygridsize=self.min_ygridsize
                
            if self.xgridsize>self.max_xgridsize:
                self.xgridsize=self.max_xgridsize
            if self.ygridsize>self.max_ygridsize:
                self.ygridsize=self.max_ygridsize
                
        if self.button==2: #mouse2
            self.xscale+=(x-self.xstart)/15
            self.yscale-=(y-self.ystart)/100
            
            #set limits
            if self.xscale<self.min_xscale:
                self.xscale=self.min_xscale
            if self.yscale<self.min_yscale:
                self.yscale=self.min_yscale
                
            if self.xscale>self.max_xscale:
                self.xscale=self.max_xscale
            if self.yscale>self.max_yscale:
                self.yscale=self.max_yscale
            
            #change margins when text rotates
            if self.xscale<self.somedata.get_maxname()*6:
                self.lowmargin=self.somedata.get_maxname()*6
                self.update()
            else:
                self.lowmargin=40
        
        #reset offset counter
        self.ystart=y
        self.xstart=x
        self.update() #update graph
    
    def paintEvent(self, e):

        #self.loadData()
        
        if self.datatype!=0:
            qp = QtGui.QPainter()
            qp.begin(self)
            qp.setRenderHint(QtGui.QPainter.Antialiasing,True)
        
            if self.datatype!="PIE":
                self.drawGrid(qp, self.somedata)
            
            qp.setClipRect(self.leftmargin,0,self.width(),self.height()-self.lowmargin) #drawing limits for margins
            
            qp.setRenderHint(QtGui.QPainter.Antialiasing,True) #smoothing
            
            if self.datatype=="LINE":
                self.drawGraphs(qp, self.somedata)
            if self.datatype=="BAR":
                self.drawBars(qp, self.somedata)
            if self.datatype=="PIE":
                self.drawPie(qp, self.somedata)
                
            qp.end()
        else:
            print("poor file")
        
        
    def drawGraphs(self, qp, data):
        
        #insert data into list
        lines=[]
        for x in range(0,data.get_length()):
            lines.append(data.get_data(x).get_data())
        
        time=lines[0]
        
        #Draw line graph from X and Y coordinates
        for y in range(1,data.get_length()):
            color=QtGui.QColor.fromHsvF(1/data.get_length()*y,0.9,0.9,0.9) #generate colors
            pen = QtGui.QPen(color, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            
            for x in range(0,len(time)-1):
                x1=time[x]*self.xscale+self.leftmargin+self.xoffset
                y1=-lines[y][x]*self.yscale+self.height()-self.lowmargin+self.yoffset
                x2=time[x+1]*self.xscale+self.leftmargin+self.xoffset
                y2=-lines[y][x+1]*self.yscale+self.height()-self.lowmargin+self.yoffset
                qp.drawLine(x1,y1,x2,y2)
        
    def drawBars(self, qp, data):
        
        pen = QtGui.QPen(QtCore.Qt.black, 5, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        
        #insert data into list
        bars=[]
        for x in range(0,data.get_length()):
            bars.append(data.get_data(x).get_data())
        
        barcount=len(bars)-1
        
        #Draw bars
        for p in range(0,barcount):
            for x in range(0,len(bars[0])):
                x1=x*self.xscale+self.leftmargin+self.xoffset
                y1=self.height()-self.lowmargin+self.yoffset
                barw=self.xscale/barcount-2
                qp.fillRect(x1+1+p*self.xscale/barcount,y1,barw,-bars[p+1][x]*self.yscale,QtGui.QColor.fromHsvF(1/barcount*p,0.9,0.9,0.9))
        
        
    def drawPie(self,qp,data):

        datalen=data.get_data(1).get_sum()
        
        piedata=[]
        piesum=0
        piesize=self.height()-80
        
        #get data and normalize it with 5760
        for x in range(0,data.get_data(1).get_len()):
            piedata.append(data.get_data(1).get_data()[x]/datalen*5760)
        
        piedata.sort(reverse=True)
        
        #Draw pie
        for p in range(0,21):
            for x in range(0,data.get_data(1).get_len()):
                if p==20:
                    color=QtGui.QColor.fromHsvF(1/data.get_data(1).get_len()*x,0.9,0.9,1) #generate colors
                    
                    qf = QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold)
                    qp.setFont(qf)
                    qp.setPen(QtCore.Qt.black)
                    qp.drawText(self.width()/2+40,25+30*x,'{:.1f}'.format(piedata[x]/57.6)+" % - "+data.get_data(0).get_data()[x])
                    
                    qp.fillRect(self.width()/2,10+30*x,30,20,color)
                else:
                    color=QtGui.QColor.fromHsvF(1/data.get_data(1).get_len()*x,0.9,0.5,1)
                
                #draw pie without outlines
                qp.setBrush(color)
                qp.setPen(color)
                qp.drawPie(piesize/5,self.height()/2-piesize/3-p,piesize,piesize/2,piesum,piedata[x])
                
                piesum+=piedata[x]
                
        
        #title label
        qf = QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold)
        qp.setFont(qf)
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 5, QtCore.Qt.SolidLine))
        qp.drawText(self.width()/2,self.height()-5,str(data.get_data(1).get_name()))
        
            
        
    def drawGrid(self, qp, data):
        
        time=data.get_data(0)
        
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DotLine)
        qp.setPen(pen)
        
        xscale=self.xscale
        yscale=self.yscale
        ygridsize=self.ygridsize
        
        starty=self.height()-self.lowmargin
        
        #drawing range
        ymin=int(self.yoffset/(ygridsize*yscale))
        ymax=int(self.yoffset/(ygridsize*yscale))+int(self.height()/(ygridsize*yscale))
        
        xmin=int(-self.xoffset/xscale)+1
        xmax=int(-self.xoffset/xscale)+int(self.width()/self.xscale)+1
        
        #fix draw range
        if self.xoffset>0:
            xmin-=1
        
        if self.yoffset>0:
            ymin+=1
            ymax+=1
        
        ##--------------LINES------------##
        
        #reduce text with ydivider
        ydivider=int(18/(yscale*ygridsize))
        if ydivider<1:
            ydivider=1
        
        xdivider=int(25/xscale)
        if xdivider<1:
            xdivider=1
        
        #horizontal
        if self.showygrid==1:
            for y in range(ymin,ymax):
                x1=self.leftmargin
                y1=starty-y*ygridsize*self.yscale+self.yoffset
                x2=self.width()
                y2=self.height()-self.lowmargin-y*ygridsize*self.yscale+self.yoffset
                
                if y%ydivider==0:
                    qp.drawLine(x1,y1,x2,y2)
                    qp.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
                    qp.drawLine(x1-7,y1,self.leftmargin,y2) #draw short solid guidelines for values
                    qp.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DotLine))
        
        #vertical
        if self.showxgrid==1:
            for x in range(xmin,xmax):
                if x%xdivider==0:
                    xpos=self.leftmargin+x*xscale+self.xoffset
                    qp.drawLine(xpos,starty,xpos,0)
            
        #draw additional solid axes for nicer visual effect
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 1.5, QtCore.Qt.SolidLine))
        qp.drawLine(self.leftmargin,starty,self.leftmargin,0) #left limiter
        
        qp.setPen(QtGui.QPen(QtCore.Qt.gray, 1.5, QtCore.Qt.SolidLine))
        if self.xoffset>0: #don't draw when out of sight
            qp.drawLine(self.leftmargin+self.xoffset,starty,self.leftmargin+self.xoffset,0) #starting axis
        if self.yoffset<0:
            qp.drawLine(self.leftmargin,starty+self.yoffset,self.width(),self.height()-self.lowmargin+self.yoffset) #zero line
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DotLine))
        
        ##------------TEXT------------##
        
        #horizontal
        if self.datatype=='LINE':
            for x in range(xmin,xmax):
                if x%xdivider==0:
                    xpos=self.leftmargin+x*xscale+self.xoffset
                    qp.drawText(xpos,starty+20,str(x))
        
        
        if self.datatype=='BAR':
            if xmin<0:
                xmin=0
            for x in range(xmin,len(time.get_data())):
                xpos=self.leftmargin+x*xscale+self.xoffset
                if len(str(time.get_data()[x]))*5<self.xscale:
                    qp.drawText(xpos,starty+20,str(time.get_data()[x]))
                else:
                    self.rotated_text(qp,xpos+10,self.height()-15,str(time.get_data()[x]))
            
        #vertical
        for y in range(ymin,ymax):
            if y%ydivider==0:
                qp.drawText(18,starty-y*ygridsize*self.yscale+self.yoffset+5,str(y*ygridsize))
        
        
        ##------------TITLES------------##
        #horizontal
        qp.drawText(self.width()/2,self.height()-5,self.xtitle)
        #vertical
        self.rotated_text(qp,15,self.height()/2,self.ytitle)
        
        
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