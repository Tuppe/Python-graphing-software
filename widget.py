
import sys
from PyQt4 import QtGui, QtCore

from PyQt4.QtGui import QGraphicsItem
from graph import GraphWidget

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
                piesize=self.height()-100
                
                qp.drawPie(piesize/5,thickness*5-p,piesize,piesize/halfer,piesum,piedata[x])
                
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
            
            #draw legend
            for x in range(0,data.get_datalist(1).get_len()):
                color=QtGui.QColor.fromHsvF(1/data.get_datalist(1).get_len()*x,0.9,0.9,1) #generate colors
                
                qf = QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold)
                qp.setFont(qf)
                qp.setPen(QtCore.Qt.black)
                qp.drawText(40,25+30*x,'{:.1f}'.format(piedata[x]/57.6)+" % - "+data.get_datalist(0).get_data()[x])
                
                #Color rectangles
                qp.fillRect(0,10+30*x,30,20,color)
        
        if self.type=='LINE' or self.type=='BAR':
            
            #draw legend
            for x in range(0,data.get_length()-1):
                color=QtGui.QColor.fromHsvF(1/data.get_length()*x,0.9,0.9,1) #generate colors
                
                qf = QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold)
                qp.setFont(qf)
                qp.setPen(QtCore.Qt.black)
                qp.drawText(40,25+30*x,'{:s}'.format(data.get_datalist(x+1).get_name()))
                
                qp.fillRect(0,10+30*x,30,20,color)
                
    
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
        qp.drawText(0,40,self.text.format(self.path))
        qp.end()



class HelpWidget(QtGui.QDialog):
  
    def __init__(self):      
        super(HelpWidget, self).__init__()
        self.setMinimumSize(200, 300)
        
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawHelp(qp)
        qp.end()
          
    def drawHelp(self,qp):
        
        qp.setPen(QtCore.Qt.black)
        qp.setFont(QtGui.QFont("AnyStyle", 10, QtGui.QFont.Bold))
        qp.drawText(30,30,'Mouse controls in the main graph window:')
        qp.setFont(QtGui.QFont("AnyStyle", 10))
        qp.drawText(30,50,'Left drag: Drag view')
        qp.drawText(30,70,'Right drag: Zoom')
        qp.drawText(30,90,'Center drag: Change grid size')
        qp.drawText(30,110,'Double click: Reset view')
        
        qp.drawText(30,150,'Click legend items to select individual graphs')
                
        
        
class LegendView(QtGui.QGraphicsView):
    def __init__(self,data,datatype,graphwidget):
        QtGui.QGraphicsView.__init__(self)
        self.scene = QtGui.QGraphicsScene(self)
        self.setBackgroundBrush(QtCore.Qt.lightGray)
        
        #draw legend
        for x in range(0,data.get_length()-1):
            color=QtGui.QColor.fromHsvF(1/data.get_length()*x,0.9,0.9,1) #generate colors
            
            self.item = LegendItem(QtCore.QPoint(30,30*x),color,data.get_datalist(x+1),graphwidget)
            self.scene.addItem(self.item)
        
        self.setScene(self.scene)
        

class LegendItem(QtGui.QGraphicsItemGroup):
    def __init__(self, pos,color,data,mainwindow):
        QtGui.QGraphicsItemGroup.__init__(self)
        #self.setRect(pos.x(), pos.y(), 20, 20)
        qf = QtGui.QFont("AnyStyle", 10)
        rectitem = QtGui.QGraphicsRectItem(pos.x(), pos.y(), 25, 20)
        textitem = QtGui.QGraphicsTextItem(data.get_name())
        textitem.setPos(pos.x()+25, pos.y()-2)
        textitem.setFont(qf)
        self.addToGroup(rectitem)
        self.addToGroup(textitem)
        
        self.rect=self.childItems()[0]
        
        brush=QtGui.QBrush(color)
        pen=QtGui.QPen(QtGui.QColor.fromHsvF(color.hueF(),0.7,0.7,1))
        
        self.rect.setPen(pen)
        self.rect.setBrush(brush)
        self.setAcceptHoverEvents(True)
        
        self.data=data
        self.color=color
        self.mainwindow=mainwindow

    def hoverEnterEvent(self, event):
        effect = QtGui.QGraphicsDropShadowEffect()
        effect.setOffset(1,1)
        effect.setBlurRadius(6)
        self.setGraphicsEffect(effect)
        QtGui.QGraphicsItemGroup.hoverEnterEvent(self, event)
    
    def hoverLeaveEvent(self, event):
        self.setGraphicsEffect(None)
        QtGui.QGraphicsItemGroup.hoverLeaveEvent(self, event)
    
    def mouseDoubleClickEvent(self, event):
        self.setOpacity(1)
        self.data.set_visibility(1)
        self.mainwindow.centralWidget().update()
        
        dataWidget = DataWidget(self.data,0,QtGui.QColor.fromHsvF(self.color.hueF(),0.9,0.9,1))
        dock=self.mainwindow.addDock(self.data.get_name(), dataWidget,QtCore.Qt.BottomDockWidgetArea)
        dock.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        
    def mousePressEvent(self, event):
        if self.data.is_visible()==1:
            self.setOpacity(0.35)
            self.data.set_visibility(0)
        else:
            self.setOpacity(1)
            self.data.set_visibility(1)
            
        self.mainwindow.centralWidget().update()