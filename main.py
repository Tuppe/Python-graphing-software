#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui, QtCore

from graph import qpen
from widget import PieWidget, LegendWidget, DataWidget
from loadfile import Data

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.path="data_ok.csv"
        self.set_graph(self.path)
        self.initUI()
    
    def initUI(self):

        #TOOLBAR
        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        
        self.addMenuItem('X-Title',"Change X title",toolbar)
        self.addMenuItem('Y-Title',"Change Y title",toolbar)
        self.addMenuItem('X-Grid',"Toggle X grid",toolbar)
        self.addMenuItem('Y-Grid',"Toggle Y grid",toolbar)
        
        #MENU
        self.legenddock=self.addDock("Legend", self.legendWidget)
        self.datadock=self.addDock("Data", self.dataWidget)
        
        loadAction = QtGui.QAction(QtGui.QIcon(), 'Load file', self)
        loadAction.setStatusTip('Load data')
        loadAction.triggered.connect(self.showFileDialog)
        self.statusBar()
        
        dockAction = QtGui.QAction(QtGui.QIcon(), 'Show legend', self)
        dockAction.setCheckable(1)
        dockAction.setChecked(1)
        dockAction.triggered.connect(self.toggleDock)
        self.statusBar()
        
        dock2Action = QtGui.QAction(QtGui.QIcon(), 'Show data', self)
        dock2Action.triggered.connect(self.toggleDock)
        dock2Action.setCheckable(1)
        dock2Action.setChecked(1)
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(loadAction)
        fileMenu.addAction(exitAction)
        
        windowMenu = menubar.addMenu('&Window')
        windowMenu.addAction(dockAction)
        windowMenu.addAction(dock2Action)
        
        self.setCentralWidget(self.graphWidget)
        
        self.setGeometry(200, 200, 850, 650)
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
        somedata=Data()
        datatype=somedata.load(file)
        
        if datatype=="PIE":
            self.graphWidget = PieWidget(somedata)
        else:
            self.graphWidget = qpen(somedata,datatype)
        
        self.legendWidget = LegendWidget(somedata,datatype)
        self.dataWidget = DataWidget(somedata,datatype)
        self.setCentralWidget(self.graphWidget)
        self.centralWidget().show()
        
        
    def showFileDialog(self):
        fname=QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname!='': #if load cancelled
            self.set_graph(fname)
            QtGui.QApplication.processEvents() #update GUI

    def addDock(self,name,widget):
        dock = QtGui.QDockWidget(name)
        dock.setWidget(QtGui.QListWidget())
        dock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable | QtGui.QDockWidget.DockWidgetMovable)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)
        dock.setWidget(widget)
        return dock
    
    
    def addMenuItem(self,name,statustip,toolbar):
        item = QtGui.QAction(QtGui.QIcon(''), name, self)
        item.triggered.connect(self.showNameDialog)
        item.setStatusTip(statustip)
        toolbar.addAction(item)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()

