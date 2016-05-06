

from PyQt4 import QtGui, QtCore

#Class to draw graphics to graph view
class GraphWidget(QtGui.QWidget):
    
    def __init__(self,data,type):
        super(GraphWidget,self).__init__()
        self.setMinimumSize(100, 100)
        
        self.initUI()
        
        self.yoffset=0
        self.xoffset=0
        self.ygridsize=1
        self.xgridsize=1
        self.xscale=1
        self.yscale=1
        
        self.leftmargin=70
        self.lowmargin=40
        self.showxgrid=1
        self.showygrid=1
        self.somedata=data
        self.datatype=type
        
        self.xtitle=str(self.somedata.get_datalist(0).get_name())
        self.ytitle=str(self.somedata.get_datalist(1).get_name())
        
        #set boundary values
        self.min_ygridsize=1
        self.max_ygridsize=500
        
        self.min_xgridsize=1
        self.max_xgridsize=50
        
        self.min_yscale=0.01
        self.max_yscale=50
        
        self.max_yoffset=90000
        self.max_xoffset=9000
        
        
        if type=="LINE":
            self.min_xscale=1
        else:
            self.min_xscale=15 #limit minimum for bar graphs
            
        self.max_xscale=200
        
        if self.datatype=='BAR':
            self.lowmargin=self.somedata.get_maxname()*6
            
        self.set_initview()
        
        self.update()
        
    def initUI(self):
        self.show()
    
    
    def paintEvent(self, e):
        
        if self.datatype!=0:
            #init painter
            qp = QtGui.QPainter()
            qp.begin(self)
            qp.setRenderHint(QtGui.QPainter.Antialiasing,True)
        
            if self.datatype!="PIE": #no grid for pie diagram
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
    
    
    def setLimits(self):
        #limit gridsize
        if self.xgridsize<self.min_xgridsize:
            self.xgridsize=self.min_xgridsize
        if self.ygridsize<self.min_ygridsize:
            self.ygridsize=self.min_ygridsize
            
        if self.xgridsize>self.max_xgridsize:
            self.xgridsize=self.max_xgridsize
        if self.ygridsize>self.max_ygridsize:
            self.ygridsize=self.max_ygridsize
        
        #limit scaling
        if self.xscale<self.min_xscale:
            self.xscale=self.min_xscale
        if self.yscale<self.min_yscale:
            self.yscale=self.min_yscale
            
        if self.xscale>self.max_xscale:
            self.xscale=self.max_xscale
        if self.yscale>self.max_yscale:
            self.yscale=self.max_yscale
            
        #Limit for offset
        if self.yoffset/self.yscale>self.max_yoffset:
            self.yoffset=self.max_yoffset*self.yscale
        
        if self.yoffset/self.yscale<-self.max_yoffset:
            self.yoffset=-self.max_yoffset*self.yscale
            
        if self.xoffset/self.xscale>self.max_xoffset:
            self.xoffset=self.max_xoffset*self.xscale
        
        if self.xoffset/self.xscale<-self.max_xoffset:
            self.xoffset=-self.max_xoffset*self.xscale
            
        if self.lowmargin<40:
            self.lowmargin=40
                          
        #change margins when text rotates
        if self.xscale<self.somedata.get_maxname()*9:
            self.lowmargin=self.somedata.get_maxname()*6+20
            self.update()
        else:
            self.lowmargin=40
            self.update()
        
        
        
    def drawGraphs(self, qp, data):
        
        datalen=data.get_length()

        #Draw line graph from X and Y coordinates
        for y in range(1,datalen):
            if (data.get_datalist(y).is_visible()==1):
                color=QtGui.QColor.fromHsvF(float(1)/datalen*(y-1),0.9,0.9,0.9) #generate colors
                
                pen = QtGui.QPen(color, 2, QtCore.Qt.SolidLine)
                qp.setPen(pen)
                
                len=data.get_datalist(0).get_len()-1
                for x in range(0,len):
                    time=data.get_datalist(0).get_data()
                    value=data.get_datalist(y).get_data()
                    
                    #get line coordinates from data and adjust by offset
                    x1=time[x]*self.xscale+self.leftmargin+self.xoffset
                    y1=-value[x]*self.yscale+self.height()-self.lowmargin+self.yoffset
                    x2=time[x+1]*self.xscale+self.leftmargin+self.xoffset
                    y2=-value[x+1]*self.yscale+self.height()-self.lowmargin+self.yoffset
                    
                    qp.drawLine(x1,y1,x2,y2)
        
    def drawBars(self, qp, data):
        
        pen = QtGui.QPen(QtCore.Qt.black, 5, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        
        barcount=data.get_length()-1
        
        #Draw bars
        for p in range(0,barcount):
            for x in range(0,data.get_datalist(0).get_len()):
                if (data.get_datalist(p+1).is_visible()==1):
                    values=-data.get_datalist(p+1).get_data()[x]
                    
                    #coordinates, height and width
                    x1=x*self.xscale+self.leftmargin+self.xoffset
                    y1=self.height()-self.lowmargin+self.yoffset
                    barw=self.xscale/barcount-2 #adjust width by number of bars
                    height=values*self.yscale
                    
                    qp.fillRect(x1+1+p*self.xscale/barcount,y1,barw,height,QtGui.QColor.fromHsvF(float(1)/(barcount+1)*p,0.9,0.9,0.9))
        
        
        
    def drawGrid(self, qp, data):
        
        time=data.get_datalist(0)
        
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DotLine)
        qp.setPen(pen)
        
        xscale=self.xscale
        yscale=self.yscale
        ygridsize=self.ygridsize
        
        starty=self.height()-self.lowmargin
        
        #calculate drawing range
        ymin=int(self.yoffset/(ygridsize*yscale))+1
        ymax=int(self.yoffset/(ygridsize*yscale))+int(self.height()/(ygridsize*yscale))+5
        
        xmin=int(-self.xoffset/xscale)+1
        xmax=int(-self.xoffset/xscale)+int(self.width()/self.xscale)+1

        #correction to drawing range
        if self.yoffset<0:
            ymin-=1

        if self.xoffset>0:
            xmin-=1

        ##--------------LINES------------##
        
        #reduce text if cannot fit
        ydivider=int(22/(yscale*ygridsize))
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
        
        #draw additional solid axes for visual effect
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
                
                #rotate text if cannot fit
                if len(str(time.get_data()[x]))*9<self.xscale:
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
    
    #adjust the default view according to min and max values
    def set_initview(self):
        #adjust gridsize to proper density
        self.ygridsize=int((self.somedata.get_max()-self.somedata.get_min())/10)
        
        self.yoffset=self.somedata.get_min()
        self.yscale=float(400)/(self.somedata.get_max()-self.yoffset) #adjust top side
        self.yoffset=self.somedata.get_min()*self.yscale
        
        self.xoffset=1
        self.xscale=float(800)/(self.somedata.get_duration()) #adjust right side
        self.setLimits() #set autoscale within limits


    #------MOUSE EVENTS--------#
        
    def mousePressEvent(self, event):
        #store mouse position and offset when first pressed
        self.button=event.button()
        self.xstart=event.globalX()
        self.ystart=event.globalY()
        
        self.yoffstart=self.yoffset
        self.yscalestart=self.yscale
        
        self.xoffstart=self.xoffset
        self.xscalestart=self.xscale
    
    def mouseDoubleClickEvent(self, event):
        #reset offset
        self.set_initview()
        
        self.update()
        
    def wheelEvent(self, event):
        #store initial values
        self.yoffstart=self.yoffset
        self.yscalestart=self.yscale
        self.xoffstart=self.xoffset
        self.xscalestart=self.xscale
        
        if event.delta()>0: #wheel up
            #scaling coefficient to adjust scaling speed to current scale
            self.yscale+=self.yscale*0.05
            self.xscale+=self.xscale*0.05
        if event.delta()<0: #wheel down
            self.yscale-=self.yscale*0.05
            self.xscale-=self.xscale*0.05
            
        self.setLimits() #check that within limits
        
        #adjust offset when zooming
        self.yoffset=(self.yoffstart/self.yscalestart)*self.yscale
        self.xoffset=(self.xoffstart/self.xscalestart)*self.xscale
        self.update() #update graph
            
        
    def mouseMoveEvent(self, event):
        #track mouse dragging
        x=event.globalX()
        y=event.globalY()
        
        if self.button==1: #mouse1
            #drag view
            self.yoffset+=y-self.ystart
            self.xoffset+=x-self.xstart
            
        if self.button==4: #middle click
            #change gridsize
            self.xgridsize-=int((x-self.xstart)/2)
            self.ygridsize-=int((y-self.ystart)/2)
            
        if self.button==2: #mouse2
            #zoom
            self.xscale+=float(x-self.xstart)*(self.xscale/400) #adjust sensitivity with current scale
            self.yscale-=float(y-self.ystart)*(self.yscale/300)
            self.setLimits()
            
            #adjust offset when zooming, otherwise view will shift
            self.yoffset=(self.yoffstart/self.yscalestart)*self.yscale
            self.xoffset=(self.xoffstart/self.xscalestart)*self.xscale
                           
        
        self.setLimits()
        #reset offset counter
        self.ystart=y
        self.xstart=x
        self.update() #update graph