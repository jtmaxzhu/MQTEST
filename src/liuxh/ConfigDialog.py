#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from PyQt4 import QtCore, QtGui
import random, mqttimage
import sqlite3, sys, os
# from PyQt4.QtGui import *  
# from PyQt4.QtCore import *  
from PyQt4.Qt import QMessageBox, QRegExpValidator


QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("utf8"))
childlist=[] 
user=''
class ConfigDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window) #设置最大化最小化按钮
        self.setWindowTitle(self.tr("设置"))
        self.resize(800,450)    
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))#设置整体风格
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())#设置整体风格
        mainSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal,self)
        
        amendPushButton = QtGui.QPushButton(self.tr("OK"))
        closePushButton = QtGui.QPushButton(self.tr("Cancel"))
        self.applyPushButton = QtGui.QPushButton(self.tr("Save"))
        self.applyPushButton.setDisabled(True)# 初始化save不可用
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(9)
        buttonLayout.addWidget(self.applyPushButton)
        buttonLayout.addWidget(amendPushButton)
#         buttonLayout.addWidget(closePushButton)  
        
        addButton = QtGui.QPushButton(self.tr(""))
        addButton.setFlat(True)
        addButton.setIcon(QtGui.QIcon(":img/image/plus.png"))   
        delButton = QtGui.QPushButton(self.tr(""))
        delButton.setFlat(True)          
        delButton.setIcon(QtGui.QIcon(":img/image/minus.png")) 
        buttonLayout1 = QtGui.QGridLayout()
        buttonLayout1.addWidget(addButton,0,0)
        buttonLayout1.addWidget(delButton,0,2)  
         

        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setColumnCount(1)#设置列数1
        self.treeWidget.setHeaderLabels([self.tr("Connections")])
        
        self.root= QtGui.QTreeWidgetItem(self.treeWidget)
        self.root.setText(0,self.tr("Profile"))
        self.treeWidget.expandAll() #节点全部展开
        treeLayout = QtGui.QVBoxLayout()
        treeLayout.addWidget(self.treeWidget)
        treeLayout.addLayout(buttonLayout1)
        
        self.Param1 = Param()
        rightQSplitter = QtGui.QFrame(mainSplitter)    
        stack = QtGui.QStackedWidget()
        stack.setFrameStyle(QtGui.QFrame.Panel|QtGui.QFrame.Raised)
        stack.addWidget(self.Param1)

        mainLayout_1 = QtGui.QHBoxLayout()   
        mainLayout_1.addLayout(treeLayout)
        mainLayout_1.addWidget(stack)        
        
        
        mainLayout = QtGui.QVBoxLayout(rightQSplitter)
        mainLayout.setMargin(1)
        mainLayout.setSpacing(6)      
        mainLayout.addLayout(mainLayout_1)

        Layout = QtGui.QVBoxLayout()
        Layout.addWidget(mainSplitter)
        Layout.addLayout(buttonLayout)
        self.setLayout(Layout)
        self.initDB()#初始化数据库     

     
     
        '''槽函数'''
        amendPushButton.clicked.connect(self.accept)
        closePushButton.clicked.connect(self.reject)
        self.applyPushButton.clicked.connect(self.apply)
        addButton.clicked.connect(self.add)
        delButton.clicked.connect(self.delete)
        self.connect(self.treeWidget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"),self.data_query) 
        ''''''   
        
    def getsetdata(self):
        self.ProfileName = self.Param1.nameEdit.text()
        self.Host = self.Param1.HostEdit.text()
        self.portValue = self.Param1.portSpinbox.value()
        self.keepValue = self.Param1.keepaliveSpinbox.value()
        self.client = self.Param1.ClientEdit.text()
        self.user = self.Param1.tab.gen.UserEdit.text()
        self.password = self.Param1.tab.gen.PassWordEdit.text()
        self.visionValue = self.Param1.tab.gen.visionComboBox.currentText()
        self.cleanssionValue = self.Param1.tab.gen.CleanSessionComboBox.currentText()
        if self.cleanssionValue =='True':
            self.cleanssion = True
#             print self.cleanssion
        else:
            self.cleanssion = False
#             print self.cleanssion
        self.napsBooL = self.Param1.tab.gen.groupBox.isChecked()#namepassword 框是否勾选
        self.pascheck = self.Param1.tab.gen.checkBox1.checkState() 
        return  self.ProfileName, self.Host, self.portValue, self.keepValue, self.client, self.user, self.password, self.visionValue,  self.cleanssion, self.napsBooL, self.pascheck
    
    
    def data_query(self, QTreeWidgetItem, int):
        global rot
        parent = QTreeWidgetItem.parent()
        if parent == -1:
            return 1
        elif parent == None:
            self.Param1.nameEdit.setText('')
            self.Param1.HostEdit.setText('')
            self.Param1.portSpinbox.setValue(0)
            self.Param1.keepaliveSpinbox.setValue(0)
            self.Param1.ClientEdit.setText('')
            self.Param1.tab.gen.UserEdit.setText('')
            self.Param1.tab.gen.PassWordEdit.setText('')
            self.applyPushButton.setDisabled(True)
        else:
            try:
                rot = parent.indexOfChild(QTreeWidgetItem)
                self.applyPushButton.setDisabled(False)
            except AttributeError:
                pass
            cur = self.conn.cursor()
            cur.execute('SELECT * FROM MQ')
            self.MQData = cur.fetchall()
            cur.execute('SELECT * FROM MQ1')
            self.MQData1 = cur.fetchall()
            cur.close()
            self.idname = childlist[rot].text(0)
    #         print childlist[rot].text(0)
            self.index = len(self.MQData)
            self.index1 = len(self.MQData1)
            if self.index > 0 :
                for x in range(self.index):
                    if self.MQData[x][0] == self.idname:
                        self.Param1.nameEdit.setText(self.idname)
                        self.Param1.HostEdit.setText(self.MQData[x][1])
                        self.Param1.portSpinbox.setValue(self.MQData[x][2])
                        self.Param1.keepaliveSpinbox.setValue(self.MQData[x][3])
                        self.Param1.ClientEdit.setText(self.MQData[x][4])
                        self.Param1.tab.gen.UserEdit.setText(self.MQData[x][5])
                        self.Param1.tab.gen.PassWordEdit.setText(self.MQData[x][6])
                        if self.MQData[x][7] == 'True':
                            self.Param1.tab.gen.CleanSessionComboBox.setCurrentIndex(0)
                        else:
                            self.Param1.tab.gen.CleanSessionComboBox.setCurrentIndex(1)
                        if self.MQData[x][8] == 'V3.1':
                            self.Param1.tab.gen.visionComboBox.setCurrentIndex(0)
                        else:
                            self.Param1.tab.gen.visionComboBox.setCurrentIndex(1)   
                        if self.MQData[x][9] == True:
                            self.Param1.tab.gen.groupBox.setChecked(True)
                        else:
                            self.Param1.tab.gen.groupBox.setChecked(False)
            if self.index1 > 0 :
                for x in range(self.index1):
                    if self.MQData1[x][0] == self.idname:
                        if self.MQData1[x][1] == 2:
                            self.Param1.tab.gen.checkBox1.setChecked(True)
                        else:
                            self.Param1.tab.gen.checkBox1.setChecked(False)  
                        self.Param1.tab.tls.openFileNameLabel.setText(self.MQData1[x][2])
                                                                                                        
            
#         print type(rot)
#         print rot

    
    @staticmethod
    def data(parent = None):
        dialog = ConfigDialog(parent)
        result = dialog.exec_()
        data = dialog.x()
        return (data, result == ConfigDialog.Accepted)
    
    def apply(self):
        self.name = self.Param1.nameEdit.text()
        self.host = self.Param1.HostEdit.text()
        self.portValue = self.Param1.portSpinbox.value()
        self.keepValue = self.Param1.keepaliveSpinbox.value()
        self.client = self.Param1.ClientEdit.text()
        self.user = self.Param1.tab.gen.UserEdit.text()
        self.password = self.Param1.tab.gen.PassWordEdit.text()
        self.visionValue = self.Param1.tab.gen.visionComboBox.currentText()
        self.cleanssionValue = self.Param1.tab.gen.CleanSessionComboBox.currentText()
        self.napsBooL = self.Param1.tab.gen.groupBox.isChecked()#namepassword 框是否勾选
        self.pascheck = self.Param1.tab.gen.checkBox1.checkState()
        self.file = self.Param1.tab.tls.openFileNameLabel.text()
        print self.file
#         print self.pascheck
#         print self.napsBooL
        if self.cleanssionValue =='True':
            self.cleanssion = True
#             print self.cleanssion
        else:
            self.cleanssion = False
#             print self.cleanssion
        
        count = len(childlist)
        for x in range(count):
            if rot == x :
                childlist[rot].setText(0,self.tr(self.name))
#         print self.idname
        c = self.conn.cursor()
        c.execute('''UPDATE MQ SET CONNAME = '%s' ,HOSTNAME = '%s', PORT = %d, KEEPLIVE = %d, CLIENTID = '%s', USERNAME = '%s', PASSWORD = '%s', CLEANSSID = '%s', MQVISION = '%s', NAPSBOOL = %d\
        where CONNAME = '%s' ''' %(self.name, self.host, self.portValue, self.keepValue, self.client, self.user, self.password, self.cleanssionValue, self.visionValue, self.napsBooL, self.idname))
        c.execute('''UPDATE MQ1 SET CONNAME = '%s' ,PASCHECK = %d, FILE = '%s'\
        where CONNAME = '%s' ''' %(self.name, self.pascheck, self.file, self.idname))
        self.conn.commit()
            
        QMessageBox.information(self, self.tr("提示"),
                                        self.tr("保存成功"))
        
    def add(self):
        self.name = self.Param1.nameEdit.text()
        self.host = self.Param1.HostEdit.text()
        self.portValue = self.Param1.portSpinbox.value()
        self.keepValue = self.Param1.keepaliveSpinbox.value()
        self.client = self.Param1.ClientEdit.text()
        self.user = self.Param1.tab.gen.UserEdit.text()
        self.password = self.Param1.tab.gen.PassWordEdit.text()
        self.visionValue = self.Param1.tab.gen.visionComboBox.currentText()
        self.cleanssionValue = self.Param1.tab.gen.CleanSessionComboBox.currentText()
        self.napsBooL = self.Param1.tab.gen.groupBox.isChecked()
        self.pascheck = self.Param1.tab.gen.checkBox1.checkState()
        self.file = self.Param1.tab.tls.openFileNameLabel.text()
        print self.file
        self.index += 1
        self.child = QtGui.QTreeWidgetItem(self.root)
        randomID = "connect_"+"".join(random.choice("0123456789ADCDEF") for x in range(15-5))
        self.child.setText(0,self.tr(randomID))  
        childlist.append(self.child)
        self.conn.execute("INSERT INTO MQ VALUES ('%s','%s', %d, %d,'%s','%s','%s','%s','%s', %d)"%(randomID, self.host, self.portValue, self.keepValue,\
                                                              self.client, self.user, self.password, self.cleanssionValue, self.visionValue, self.napsBooL))
        self.conn.execute("INSERT INTO MQ1 VALUES ('%s', %d, '%s')"%(randomID, self.pascheck, self.file))
    
    def delete(self):
        count = len(childlist)
        for x in range(count):
            if rot == x :
                self.root.removeChild(childlist[rot])
                childlist.remove(childlist[rot])
        self.conn.execute("DELETE FROM MQ WHERE CONNAME = '%s' " % (self.idname))
        self.conn.execute("DELETE FROM MQ1 WHERE CONNAME = '%s' " % (self.idname))
  
    def initDB(self):
        if os.path.exists('MQ.db'):
            self.conn = sqlite3.connect('MQ.db')
            self.conn.isolation_level = None
        else:
            self.conn = sqlite3.connect('MQ.db')
            self.conn.isolation_level = None
            self.conn.execute('''CREATE TABLE MQ
                        (CONNAME char PRIMARY KEY NOT NULL,
                        HOSTNAME char(255),
                        PORT INT,
                        KEEPLIVE INT,
                        CLIENTID char(255),
                        USERNAME char(255),
                        PASSWORD char(255),
                        CLEANSSID BOOLEAN,
                        MQVISION char(255),
                        NAPSBOOL BOOLEAN)''')
            self.conn.execute('''CREATE TABLE MQ1
                        (CONNAME char PRIMARY KEY NOT NULL,
                        PASCHECK INT,
                        FILE char(255))''')
        self.cur = self.conn.cursor()
        self.cur.execute('SELECT * FROM MQ')
        self.MQData = self.cur.fetchall()
        self.cur.execute('SELECT * FROM MQ1')
        self.MQData1 = self.cur.fetchall()
        self.cur.close()
        self.index = len(self.MQData)
        if self.index > 0 :
            for x in range(self.index):
                self.child = QtGui.QTreeWidgetItem(self.root)
#                 print self.child
                childlist.append(self.child)
                id = self.MQData[x][0]
                self.child.setText(0,self.tr(id))
        
class Param(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Param, self).__init__(parent)
#         self.resize(800,400)
        nameGroup = QtGui.QGroupBox("Name Profile")
        nameLabel = QtGui.QLabel("Connect Name:")
        self.nameEdit = QtGui.QLineEdit()
        '''只允许输入字母和数字'''
        re1=QtCore.QRegExp("[a-zA-Z0-9]+$")
        self.nameEdit.setValidator(QtGui.QRegExpValidator(re1,self))
        ''''''
        ClientGroup = QtGui.QGroupBox("CLient Profile")
        Hostlabel = QtGui.QLabel("HostName:")
        self.HostEdit = QtGui.QLineEdit()
        Portlabel = QtGui.QLabel("Port:")
        ClientIdlabel = QtGui.QLabel("ClientId:")
        self.ClientEdit = QtGui.QLineEdit()
        Keepalivelabel = QtGui.QLabel("Keepalive:")
        checkBox1 = QtGui.QCheckBox("clean_session")
        Button1 = QtGui.QPushButton("Generate")

        amendPushButton = QtGui.QPushButton(self.tr("Apply"))
        closePushButton = QtGui.QPushButton(self.tr("关闭"))
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(0)
#         buttonLayout.addWidget(amendPushButton)
#         buttonLayout.addWidget(closePushButton)
        
        self.portSpinbox = QtGui.QSpinBox()
        self.portSpinbox.setMaximum(9999) 
        self.portSpinbox.setMinimum(0)
#         self.portSpinbox.setValue(1883)
        
        self.keepaliveSpinbox = QtGui.QSpinBox()
        self.keepaliveSpinbox.setMaximum(9999) 
        self.keepaliveSpinbox.setMinimum(0)
#         self.keepaliveSpinbox.setValue(60)

        nameLayout = QtGui.QGridLayout()
        nameLayout.addWidget(nameLabel, 0, 0)
        nameLayout.addWidget(self.nameEdit, 0, 1)
        nameGroup.setLayout(nameLayout)
        
        inputMaskLabel = QtGui.QLabel("MQTT")
        self.inputMaskComboBox = QtGui.QComboBox()
        self.inputMaskComboBox.addItem("V3.1")
        self.inputMaskComboBox.addItem("V3.1.1")
        
        inputMaskLabel1 = QtGui.QLabel("Clean_session")
        self.inputMaskComboBox1 = QtGui.QComboBox()
        self.inputMaskComboBox1.addItem("True")
        self.inputMaskComboBox1.addItem("False")
        
        
        '''槽函数'''
        Button1.clicked.connect(self.gengrate)
        ''''''
        
        clientLayout = QtGui.QGridLayout()
        clientLayout.addWidget(Hostlabel, 0, 0)
        clientLayout.addWidget(self.HostEdit, 0, 1)
        clientLayout.addWidget(Portlabel, 0,2)
        clientLayout.addWidget(self.portSpinbox, 0,3)
        clientLayout.addWidget(Keepalivelabel, 1, 0)
        clientLayout.addWidget(self.keepaliveSpinbox, 1, 1, 1, 3)
        clientLayout.addWidget(ClientIdlabel, 2,0)
        clientLayout.addWidget(self.ClientEdit, 2, 1, 1, 2)
        clientLayout.addWidget(Button1,2,3) 
        ClientGroup.setLayout(clientLayout)
        
        self.tab=TabDialog()
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(nameGroup)
        mainLayout.addWidget(ClientGroup)
        mainLayout.addWidget(self.tab)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addSpacing(2)
        mainLayout.addStretch()

        self.setLayout(mainLayout)
   
   
    def gengrate(self):
        gen = "Admin_" + "".join(random.choice("0123456789ADCDEF") for x in range(23-5))
        self.ClientEdit.setText(gen)

        

class TabDialog(QtGui.QWidget):
    def __init__(self,  parent=None):
        super(TabDialog, self).__init__(parent)
        tabWidget = QtGui.QTabWidget()
        self.gen=GeneralTab()
        self.tls=TLSTab()
        tabWidget.addTab(self.gen, "General")
        tabWidget.addTab(self.tls, "TLS")
    
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)    
        
        
class GeneralTab(QtGui.QWidget):
    def __init__(self,  parent=None):
        super(GeneralTab, self).__init__(parent)
 
#         clean_session_checkBox = QtGui.QCheckBox("clean_session")
        groupBox = QtGui.QGroupBox("UserName && PassWord")
        visionLabel = QtGui.QLabel("MQTT vision:")
        self.visionComboBox = QtGui.QComboBox()
        self.visionComboBox.addItem("V3.1")
        self.visionComboBox.addItem("V3.1.1")
        
        CleanSessionLabel = QtGui.QLabel("Clean session:")
        self.CleanSessionComboBox = QtGui.QComboBox()
        self.CleanSessionComboBox.addItem("True")
        self.CleanSessionComboBox.addItem("False")

        
        VersionLayout = QtGui.QGridLayout()
        VersionLayout.addWidget(CleanSessionLabel,0,0)
        VersionLayout.addWidget(self.CleanSessionComboBox,0,1)
        VersionLayout.addWidget(visionLabel,1,0)
        VersionLayout.addWidget(self.visionComboBox,1,1)
        
        grid = QtGui.QGridLayout()
        grid.addWidget(self.createuserGroup(), 0, 0)
        grid.addLayout(VersionLayout, 1, 0)
        grid.setColumnStretch(1,0)
        self.setLayout(grid)
        
        '''槽函数'''
        
        ''''''
  
    def createuserGroup(self):
        self.groupBox = QtGui.QGroupBox("UserName && PassWord")
        self.groupBox.setCheckable(True)
        self.groupBox.setChecked(True)
        
        UserLabel = QtGui.QLabel("UserName:")
        self.UserEdit = QtGui.QLineEdit()
#         self.UserEdit.setText('liuxh')
        PassWordLabel = QtGui.QLabel("PassWord:")
        self.PassWordEdit = QtGui.QLineEdit()
#         self.PassWordEdit.setText('123456')
        self.checkBox1 = QtGui.QCheckBox("")
#         self.checkBox1.setCheckState(True)      
        '''槽函数'''
        self.checkBox1.stateChanged.connect(self.hide) 
        ''''''
        self.checkBox1.setChecked(True)
         
              
        NamePassLayout = QtGui.QGridLayout()
        NamePassLayout.addWidget(UserLabel,0,0)
        NamePassLayout.addWidget(self.UserEdit,0,1)
        NamePassLayout.addWidget(PassWordLabel,1,0)
        NamePassLayout.addWidget(self.PassWordEdit,1,1)
        NamePassLayout.addWidget(self.checkBox1,1,2)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(NamePassLayout)
        vbox.addStretch()
        self.groupBox.setLayout(vbox)

        return self.groupBox

    def hide(self):
#         print self.checkBox1.checkState()
        if self.checkBox1.checkState() == 2:
            self.PassWordEdit.setEchoMode(QtGui.QLineEdit.Password)
        else:
            self.PassWordEdit.setEchoMode(QtGui.QLineEdit.Normal)
        
class TLSTab(QtGui.QDialog):
    def __init__(self,  parent=None):
        super(TLSTab, self).__init__(parent)   
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        groupBox = QtGui.QGroupBox("CA certificate")  
        self.openFileNameLabel = QtGui.QLabel()
        self.openFileNameButton = QtGui.QPushButton("open")
        self.openFileNameLabel.setFrameStyle(frameStyle)
        self.openFileNameLabel.setStyleSheet("background:white") 
        
        TLSLayout = QtGui.QGridLayout()
        TLSLayout.addWidget(self.openFileNameLabel,0,0,1,5)
        TLSLayout.addWidget(self.openFileNameButton,0,6,1,1)
        groupBox.setLayout(TLSLayout)
        
        SSLLayout1 = QtGui.QGridLayout()
        SSLLayout1.addWidget(groupBox,0,0)
        self.setLayout(SSLLayout1)
    
        self.openFileNameButton.clicked.connect(self.setOpenFileName1)

    
    def setOpenFileName1(self):    
        options = QtGui.QFileDialog.Options()
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                "QFileDialog.getOpenFileName()",
                self.openFileNameLabel.text(),
                "All Files (*);;Text Files (*.txt)")
        if fileName:
            self.openFileNameLabel.setText(fileName)     

        

#         
# 
# if __name__ == '__main__':
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     dialog = ConfigDialog()
#     dialog.show()
#     app.exec_()   
#     dialog.conn.close()