#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui, QtCore

from graph import qpen

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super().__init__()
        #self.showDialog()
        self.graphWidget=0
        self.set_graph('data_pie.csv')
        self.initUI()
    
    def initUI(self):

        #TOOLBAR
        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        
        #MENU
        loadAction = QtGui.QAction(QtGui.QIcon(), 'Load file', self)
        loadAction.setStatusTip('Load data')
        loadAction.triggered.connect(self.showDialog)
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(loadAction)
        fileMenu.addAction(exitAction)
        
        
        self.setGeometry(200, 200, 850, 550)
        self.setWindowTitle('Grapher Pro 8000')
        self.show()
        
    def set_graph(self,file):
        self.graphWidget = qpen(file) #'data_ok2.csv'
        
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
        
        
    def showDialog(self):
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

