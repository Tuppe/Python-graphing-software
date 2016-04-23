#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui, QtCore

from graph import qpen
from widget import PieWidget, LegendWidget
from loadfile import Data

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super().__init__()
        #self.showDialog()
        self.graphWidget=0
        self.path="data_ok2.csv"
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
        
        exitAction2 = QtGui.QAction(QtGui.QIcon(''), 'X-Title', self)
        exitAction2.triggered.connect(self.showNameDialog)
        toolbar.addAction(exitAction2)
        
        exitAction3 = QtGui.QAction(QtGui.QIcon(''), 'Y-Title', self)
        exitAction3.triggered.connect(self.showNameDialog)
        toolbar.addAction(exitAction3)
        
        xgrid = QtGui.QAction(QtGui.QIcon(''), 'X-Grid', self)
        xgrid.triggered.connect(self.showNameDialog)
        toolbar.addAction(xgrid)
        
        ygrid = QtGui.QAction(QtGui.QIcon(''), 'Y-Grid', self)
        ygrid.triggered.connect(self.showNameDialog)
        toolbar.addAction(ygrid)
        
        #MENU
        loadAction = QtGui.QAction(QtGui.QIcon(), 'Load file', self)
        loadAction.setStatusTip('Load data')
        loadAction.triggered.connect(self.showFileDialog)
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(loadAction)
        fileMenu.addAction(exitAction)
        
        
        self.setGeometry(200, 200, 850, 550)
        self.setWindowTitle('Grapher Pro 8000')
        self.show()
       
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
        
        self.graphWidget = qpen(somedata,datatype)
        #self.graphWidget = LegendWidget()
        
        top = QtGui.QFrame(self)
        top.setFrameShape(QtGui.QFrame.StyledPanel)

        bottom = QtGui.QFrame(self)
        bottom.setFrameShape(QtGui.QFrame.StyledPanel)

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(top)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(self.graphWidget)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
        splitter2.setSizes([80,20])
        
        self.setCentralWidget(splitter2)
        
        self.graphWidget.show()
        
        
    def showFileDialog(self):
        fname=QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname!='': #if load cancelled
            self.set_graph(fname)
            QtGui.QApplication.processEvents() #update GUI


def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    #print(ex.showDialog())
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()

