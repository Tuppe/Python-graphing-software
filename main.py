import sys
from PyQt4 import QtGui, QtCore

from graph import GraphWidget
from widget import PieWidget, DataWidget, TextWidget, LegendView, AboutWidget, DataTab
from loadfile import DataList

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.piestyle=1
        self.path="data_pie.csv"
        #self.path=0
        self.initUI()
        self.set_graph(self.path)
    
    def initUI(self):
        
        #Setup initial empty view
        legendWidget=TextWidget(self.path,"",QtCore.Qt.red)
        dataWidget=TextWidget(self.path,"",QtCore.Qt.red)
        self.graphWidget=TextWidget(self.path,"Start by loading data",QtCore.Qt.black)
        self.setCentralWidget(self.graphWidget)
        
        #------TOOLBAR------#
        toolbar = self.addToolBar('Toolbar')
        
        #toolbar items
        exitAction=self.addMenuItem('Exit','Exit application',toolbar,'exit24.png',self.close)
        self.menu_xtitle=self.addMenuItem('X-Title',"Change X title",toolbar,'',self.showNameDialog)
        self.menu_ytitle=self.addMenuItem('Y-Title',"Change Y title",toolbar,'',self.showNameDialog)
        self.menu_xgrid=self.addMenuItem('X-Grid',"Toggle X grid",toolbar,'',self.showNameDialog)
        self.menu_ygrid=self.addMenuItem('Y-Grid',"Toggle Y grid",toolbar,'',self.showNameDialog)
        self.menu_3d=self.addMenuItem('3D',"Toggle 3D view",toolbar,'',self.showNameDialog)
        self.set_toolbaritem_visibility(0,0,0,0,0)
        
        #-----DROPDOWN MENU-----#
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False) #show menu in linux
        
        #Add menus
        fileMenu = menubar.addMenu('&File')
        windowMenu = menubar.addMenu('&Window')
        aboutMenu = menubar.addMenu('&About')
        
        #add dropdown items
        self.addDropdownItem('Load file',fileMenu, 0,self.showFileDialog)
        self.addDropdownItem('Show legend',windowMenu, 1,self.toggleDock)
        self.addDropdownItem('Show data',windowMenu, 1,self.toggleDock)
        
        fileMenu.addAction(exitAction)
        
        self.addDropdownItem('Help',aboutMenu, 0,self.showNameDialog)
        self.addDropdownItem('Info',aboutMenu, 0,self.showNameDialog)
        self.statusBar() #status tip text shown bottom of screen
        
        #------DOCKS------#
        self.legenddock=self.addDock("Legend", legendWidget,QtCore.Qt.RightDockWidgetArea)
        self.datadock=self.addDock("Data", dataWidget,QtCore.Qt.BottomDockWidgetArea)

        #Window properties
        self.setGeometry(600, 100, 1050, 650)
        self.setMinimumSize(400, 400)
        self.setWindowTitle('Grapher Pro 8000')
        self.setWindowIcon(QtGui.QIcon('icon.tif'))
        self.show()
        
    
    #Toggle dock visibility when selected from menu
    def toggleDock(self):
        sender = self.sender() #get which button was pressed
        
        if sender.text()=="Show legend":
            self.legenddock.setVisible(1-self.legenddock.isVisible())
        if sender.text()=="Show data":
            self.datadock.setVisible(1-self.datadock.isVisible())
    
    #Show input dialog for changing the titles
    def showNameDialog(self):
        
        sender = self.sender()
        
        #setup input dialog layout
        button = QtGui.QPushButton('Dialog', self)
        button.move(20, 20)
        button.clicked.connect(self.showNameDialog)
        
        rinput = QtGui.QLineEdit(self)
        rinput.move(130, 22)
        
        if sender.text()=="X-Title":
            #get input text and selection from dialog
            text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter X-title:')
            
            if ok:
                self.graphWidget.set_xname(str(text))
             
        if sender.text()=="Y-Title":
            text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter Y-title:')
            
            if ok:
                self.graphWidget.set_yname(str(text))
        
        #Toggle grid button action
        if sender.text()=="X-Grid":
            self.graphWidget.toggle_xgrid()
                
        if sender.text()=="Y-Grid":
            self.graphWidget.toggle_ygrid()
            
        if sender.text()=="3D":
            self.piestyle=1-self.piestyle
            self.graphWidget.changeStyle(self.piestyle)
            
        if sender.text()=="Help":
            dialog = AboutWidget(1)
            dialog.resize(500,200)
            dialog.setWindowTitle("Help")
            dialog.exec_()
            
        if sender.text()=="Info":
            dialog = AboutWidget(2)
            dialog.resize(500,200)
            dialog.setWindowTitle("Info")
            dialog.exec_()

    #load new data and update menu, graph, legend and data
    def set_graph(self,file):
        
        #delete old widgets
        self.graphWidget.destroy()
        self.legenddock.destroy()
        self.datadock.destroy()
        
        #load data
        newdata=DataList()
        datatype=newdata.load(file)
        
        #setup main graph
        if datatype=="PIE":
            self.graphWidget = PieWidget(newdata,self.piestyle)
            self.set_toolbaritem_visibility(0,0,0,0,1)
        elif datatype=="LINE" or datatype=="BAR":
            self.graphWidget = GraphWidget(newdata,datatype)
            self.set_toolbaritem_visibility(1,1,1,1,0)
        else:
            self.graphWidget = TextWidget(file,'Data Error {:s}',QtCore.Qt.red)
            
            self.set_toolbaritem_visibility(0,0,0,0,0)
            self.setCentralWidget(self.graphWidget)
            self.centralWidget().show()
            return 0
        
        self.setCentralWidget(self.graphWidget)
        self.centralWidget().show()
        
        #setup widgets
        legendWidget = LegendView(newdata,datatype,self)
        dataWidget = DataWidget(newdata,datatype,QtCore.Qt.white)
        dataTab = DataTab()
        dataTab.addTab(dataWidget, "Total")
        
        self.legenddock.setWidget(legendWidget)
        self.datadock.setWidget(dataTab)
        
    
    #Show and hide toolbar items
    def set_toolbaritem_visibility(self,xgrid,ygrid,xtitle,ytitle,view_3d):
        self.menu_xgrid.setVisible(xgrid)
        self.menu_ygrid.setVisible(ygrid)
        self.menu_xtitle.setVisible(xtitle)
        self.menu_ytitle.setVisible(ytitle)
        self.menu_3d.setVisible(view_3d)
    
    #Show file browser window and get new data file name
    def showFileDialog(self):
        fname=QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname!='': #if load cancelled
            self.set_graph(fname)
            QtGui.QApplication.processEvents() #update GUI
    
    def addDock(self,name,widget,area):
        dock = QtGui.QDockWidget(name) #create dock
        dock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable | QtGui.QDockWidget.DockWidgetMovable)
        self.addDockWidget(area, dock) #add dock
        dock.setWidget(widget) #insert widget to dock
        return dock
    
    def addDropdownItem(self,name,menubar,checkable,action):
        addAction = QtGui.QAction(QtGui.QIcon(), name, self) #init item
        addAction.setCheckable(checkable)
        addAction.setChecked(1)
        addAction.triggered.connect(action) #set action when clicked
        menubar.addAction(addAction)
        return addAction
    
    def addMenuItem(self,name,statustip,toolbar,icon,action):
        item = QtGui.QAction(QtGui.QIcon(icon), name, self)
        item.triggered.connect(action)
        item.setStatusTip(statustip)
        toolbar.addAction(item)
        return item

#main loop
def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()

