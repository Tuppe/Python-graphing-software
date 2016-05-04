
from PyQt4 import QtGui, QtCore


class PieWidget(QtGui.QWidget):
  
    def __init__(self,data,style):      
        super(PieWidget, self).__init__()
        self.setMinimumSize(200,200)
        self.data=data
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
            piedata.append(float(data.get_datalist(1).get_data()[x])/datalen*5760)
        
        piedata.sort(reverse=True)
        
        #Draw pie
        for p in range(0,thickness):
            for x in range(0,data.get_datalist(1).get_len()):
                if p==thickness-1:
                    #top of the pie
                    color=QtGui.QColor.fromHsvF(float(1)/data.get_datalist(1).get_len()*x,0.9,0.9,1)
                else:
                    #3D side with fade color
                    color=QtGui.QColor.fromHsvF(float(1)/data.get_datalist(1).get_len()*x,0.9,(0.3/thickness)*p+0.5,1)
                
                #draw pie without outlines
                qp.setBrush(color)
                qp.setPen(color)
                piesize=self.height()-100
                if (data.get_datalist(1).is_visible()):
                    qp.drawPie(piesize/5,thickness*5-p,piesize,piesize/halfer,piesum,piedata[x])
                
                piesum+=piedata[x]


#Main class for Legend, store all tabs
class DataTab(QtGui.QTabWidget):
  
    def __init__(self):
        super(DataTab, self).__init__()
        self.setMinimumSize(100, 100)

#Class for data elements stored in tabs
class DataWidget(QtGui.QWidget):
  
    def __init__(self,data,type,color):
        super(DataWidget, self).__init__()
        self.setMinimumSize(100, 100)
        self.data=data
        self.type=type
        self.color=color

        
    def paintEvent(self, e):
        
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawData(qp,self.data)
        qp.end()
          
    def drawData(self,qp,data):
        if self.color!=0:
            qp.fillRect(0,0,self.width(),5,self.color)
            qp.drawText(10,20,'Average {:.1f}'.format(data.get_avg()))
            qp.drawText(10,35,'Max {:.1f}'.format(data.get_max()))
            qp.drawText(10,50,'Min {:.1f}'.format(data.get_min()))

#Class to display basic text
class TextWidget(QtGui.QWidget):
  
    def __init__(self,path,text,color):
        super(TextWidget, self).__init__()
        self.setMinimumSize(150, 150)
        self.path=path
        self.text=text
        self.color=color
        
    def paintEvent(self, e):
        
        qp = QtGui.QPainter()
        qp.begin(self)
        qf = QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold)
        qp.setFont(qf)
        qp.setPen(self.color)
        qp.drawText(20,40,self.text.format(self.path))
        qp.end()


#Class to display about data
class AboutWidget(QtGui.QDialog):
  
    def __init__(self,abouttype): 
        super(AboutWidget, self).__init__()
        self._type=abouttype
        if self._type==1:
            self.setMinimumSize(200, 300)
        if self._type==2:
            self.setMinimumSize(50, 100)
        
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawHelp(qp)
        qp.end()
          
    def drawHelp(self,qp):
        
        if self._type==1:
            qp.setPen(QtCore.Qt.black)
            qp.setFont(QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold))
            qp.drawText(30,30,'Mouse controls in the main graph window:')
            qp.setFont(QtGui.QFont("AnyStyle", 10))
            qp.drawText(30,50,'Left drag: Drag view')
            qp.drawText(30,70,'Right drag: Zoom')
            qp.drawText(30,90,'Center drag: Change grid size')
            qp.drawText(30,110,'Double click: Reset view')
            qp.setFont(QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold))
            qp.drawText(30,150,'Mouse controls in the legend window:')
            qp.setFont(QtGui.QFont("AnyStyle", 10))
            qp.drawText(30,170,'Left click: Disable/Enable')
            qp.drawText(30,190,'Right click: Get data')
        
        if self._type==2:
            qp.drawText(30,30,'Made by: Tuomas Manninen, 2016')
            qp.drawText(30,50,'Wappu edition')
        
#Class to display legend menu graphics
class LegendView(QtGui.QGraphicsView):
    def __init__(self,data,datatype,graphwidget):
        QtGui.QGraphicsView.__init__(self)
        self.scene = QtGui.QGraphicsScene(self)
        self.setBackgroundBrush(QtCore.Qt.lightGray)
        
        
        if datatype=='PIE':
            datalen=data.get_datalist(1).get_sum()
            piedata=[]
            
            #get data for sorting and normalize it to 5760
            for x in range(0,data.get_datalist(1).get_len()):
                piedata.append(float(data.get_datalist(1).get_data()[x])/datalen*5760)
            
            piedata.sort(reverse=True)
            
            #create all legend items with percentage data
            for x in range(0,data.get_datalist(1).get_len()):
                color=QtGui.QColor.fromHsvF(float(1)/data.get_datalist(1).get_len()*x,0.9,0.9,1) #generate colors
                
                text='{:.1f}'.format(piedata[x]/57.6)+" % - "+data.get_datalist(0).get_data()[x]
                self.item = LegendItem(QtCore.QPoint(30,30*x),color,data.get_datalist(1),text,graphwidget)
                self.scene.addItem(self.item)
        
        if datatype=='LINE' or datatype=='BAR':
            #create all legend items with data
            for x in range(0,data.get_length()-1):
                color=QtGui.QColor.fromHsvF(float(1)/data.get_length()*x,0.9,0.9,1) #generate colors
                
                self.item = LegendItem(QtCore.QPoint(30,30*x),color,data.get_datalist(x+1),data.get_datalist(x+1).get_name(),graphwidget)
                self.scene.addItem(self.item)
        
        self.setScene(self.scene)
        
        
#Class for each legend rectangle and text item
class LegendItem(QtGui.QGraphicsItemGroup):
    def __init__(self, pos,color,data,text,mainwindow):
        QtGui.QGraphicsItemGroup.__init__(self)
        qf = QtGui.QFont("AnyStyle", 10)
        
        #create text and rectangles
        rectitem = QtGui.QGraphicsRectItem(pos.x(), pos.y(), 25, 20)
        textitem = QtGui.QGraphicsTextItem(text)
        textitem.setPos(pos.x()+25, pos.y()-2)
        textitem.setFont(qf)
        
        #combine to group
        self.addToGroup(rectitem)
        self.addToGroup(textitem)
        
        self.rect=self.childItems()[0] #this is rectangle in the group
        
        #color the rectangle
        brush=QtGui.QBrush(color)
        pen=QtGui.QPen(QtGui.QColor.fromHsvF(color.hueF(),0.7,0.7,1))
        
        self.rect.setPen(pen)
        self.rect.setBrush(brush)
        self.setAcceptHoverEvents(True)
        
        self.data=data
        self.color=color
        self.mainwindow=mainwindow

    def hoverEnterEvent(self, event):
        #effect when cursor over legend items
        effect = QtGui.QGraphicsDropShadowEffect()
        effect.setOffset(1,1)
        effect.setBlurRadius(6)
        self.setGraphicsEffect(effect)
        QtGui.QGraphicsItemGroup.hoverEnterEvent(self, event)
    
    def hoverLeaveEvent(self, event):
        self.setGraphicsEffect(None)
        QtGui.QGraphicsItemGroup.hoverLeaveEvent(self, event)
    
        
    def mousePressEvent(self, event):
        button=0
        if (type(self.mainwindow.centralWidget()).__name__)!="PieWidget": #no effect for pie diagram
            button=event.button()
        
        if button==1: #left button, hide graphs
            if self.data.is_visible()==1:
                self.setOpacity(0.35)
                self.data.set_visibility(0)
            else:
                self.setOpacity(1)
                self.data.set_visibility(1)
                
            self.mainwindow.centralWidget().update()
            
        if button==2: #right button, open new info tab
            self.setOpacity(1)
            self.data.set_visibility(1)
            self.mainwindow.centralWidget().update()
                
            dataWidget = DataWidget(self.data,0,QtGui.QColor.fromHsvF(self.color.hueF(),0.9,0.9,1))
            self.mainwindow.datadock.widget().addTab(dataWidget,self.data.get_name())
            
