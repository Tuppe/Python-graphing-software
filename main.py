#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui, QtCore

from graph import GraphWidget
from widget import PieWidget, LegendWidget, DataWidget, TextWidget
from loadfile import Data

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.path="data_ok22.csv"
        self.legendWidget=TextWidget(self.path,"")
        self.dataWidget=TextWidget(self.path,"")
        self.graphWidget=TextWidget(self.path,"")
        self.initUI()
        self.set_graph(self.path)
    
    def initUI(self):

        #TOOLBAR
        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        
        self.menu_xtitle=self.addMenuItem('X-Title',"Change X title",toolbar)
        self.menu_ytitle=self.addMenuItem('Y-Title',"Change Y title",toolbar)
        self.menu_xgrid=self.addMenuItem('X-Grid',"Toggle X grid",toolbar)
        self.menu_ygrid=self.addMenuItem('Y-Grid',"Toggle Y grid",toolbar)
        
        #MENU
        self.legenddock=self.addDock("Legend", self.legendWidget,QtCore.Qt.RightDockWidgetArea)
        self.datadock=self.addDock("Data", self.dataWidget,QtCore.Qt.BottomDockWidgetArea)
        
        loadAction=self.addSelectionItem('Load file', 0)
        loadAction.triggered.connect(self.showFileDialog)
        dockAction=self.addSelectionItem('Show legend', 1)
        dock2Action=self.addSelectionItem('Show data', 1)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(loadAction)
        fileMenu.addAction(exitAction)
        
        windowMenu = menubar.addMenu('&Window')
        windowMenu.addAction(dockAction)
        windowMenu.addAction(dock2Action)
        
        self.setCentralWidget(self.graphWidget)
        
        self.setGeometry(200, 200, 1050, 650)
        self.setWindowTitle('Grapher Pro 8000')
        self.show()
        
    
    def toggleDock(self):
        sender = self.sender()
        if sender.text()=="Show legend":
            self.legenddock.setVisible(1-self.legenddock.isVisible())
        if sender.text()=="Show data":
            self.datadock.setVisible(1-self.datadock.isVisible())
    
    def showNameDialog(self):
        
        sender = self.sender()
        
        self.button = QtGui.QPushButton('Dialog', self)
        self.button.move(20, 20)
        self.button.clicked.connect(self.showNameDialog)
        
        self.input = QtGui.QLineEdit(self)
        self.input.move(130, 22)
        
        if sender.text()=="X-Title":
            text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter X-title:')
            
            if ok:
                self.graphWidget.set_xname(str(text))
             
        if sender.text()=="Y-Title":
            text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter Y-title:')
            
            if ok:
                self.graphWidget.set_yname(str(text))
        
        if sender.text()=="X-Grid":
            self.graphWidget.toggle_xgrid()
                
        if sender.text()=="Y-Grid":
            self.graphWidget.toggle_ygrid()

    def set_graph(self,file):
        newdata=Data()
        datatype=newdata.load(file)
        
        if datatype=="PIE":
            self.menu_xgrid.setVisible(0)
            self.menu_ygrid.setVisible(0)
            self.menu_xtitle.setVisible(0)
            self.menu_ytitle.setVisible(0)
            self.graphWidget = PieWidget(newdata)
        elif datatype=="LINE" or datatype=="BAR":
            self.menu_xgrid.setVisible(1)
            self.menu_ygrid.setVisible(1)
            self.menu_xtitle.setVisible(1)
            self.menu_ytitle.setVisible(1)
            self.graphWidget = GraphWidget(newdata,datatype)
        else:
            self.graphWidget = TextWidget(file,'Data Error {:s}')
        
        self.legendWidget = LegendWidget(newdata,datatype)
        self.dataWidget = DataWidget(newdata,datatype)
        self.legenddock.setWidget(self.legendWidget)
        
        self.setCentralWidget(self.graphWidget)
        self.centralWidget().show()
        
        
    def showFileDialog(self):
        fname=QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname!='': #if load cancelled
            self.set_graph(fname)
            QtGui.QApplication.processEvents() #update GUI

    def addDock(self,name,widget,area):
        dock = QtGui.QDockWidget(name)
        dock.setWidget(QtGui.QListWidget())
        dock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable | QtGui.QDockWidget.DockWidgetMovable)
        self.addDockWidget(area, dock)
        dock.setWidget(widget)
        return dock
    
    def addSelectionItem(self,name,checkable):
        dockAction = QtGui.QAction(QtGui.QIcon(), name, self)
        dockAction.setCheckable(checkable)
        dockAction.setChecked(1)
        dockAction.triggered.connect(self.toggleDock)
        self.statusBar()
        return dockAction
    
    def addMenuItem(self,name,statustip,toolbar):
        item = QtGui.QAction(QtGui.QIcon(''), name, self)
        item.triggered.connect(self.showNameDialog)
        item.setStatusTip(statustip)
        toolbar.addAction(item)
        return item

def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()

