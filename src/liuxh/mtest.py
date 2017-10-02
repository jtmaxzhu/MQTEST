#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4 import QtCore, QtGui
import sys, socket, binascii
import mqttimage,time
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from ConfigDialog import *
import ctypes 

QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("utf8"))
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid") #状态栏单独显示


class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setWindowTitle(self.tr("MQ TEST"))
        self.setWindowIcon(QtGui.QIcon(":img/image/mq.png"));
        QtCore.QThread.sleep(0)#启动画面停留时间
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))#设置整体风格
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())#设置整体风格
        self.resize(800,550)#####设置窗口大小
#         self.statusBar().showMessage(self.tr("未建立连接"))
#         self.StackDialog=StackDialog()
        # 开始装载样式表
#         qss_file = open('style.qss').read()
#         self.setStyleSheet(qss_file)
        self.a = A()
        self.setCentralWidget(self.a)
        self.createActions()
        self.createMenus()
        self.createToolBars()
 

        
    def createActions(self):
#         self.fileOpenAction=QtGui.QAction(QtGui.QIcon(":pic/image/xitong/folder_blue.png"),self.tr("打开"),self)
#         self.fileOpenAction.setShortcut("Ctrl+O")
#         self.fileOpenAction.setStatusTip(self.tr("打开一个文件"))
#         self.connect(self.fileOpenAction,QtCore.SIGNAL("triggered()"),self.slotOpenFile)
        
        self.fileSaveAction=QtGui.QAction(QtGui.QIcon(":pic/image/xitong/save.png"),self.tr("保存"),self)
        self.fileSaveAction.setShortcut("Ctrl+S")
        self.fileSaveAction.setStatusTip(self.tr("保存文件"))
        self.connect(self.fileSaveAction,QtCore.SIGNAL("triggered()"),self.fileSaveAs)
        
        self.settingAction=QtGui.QAction(QtGui.QIcon(":img/image/setting.png"),self.tr("设置"),self)
        self.settingAction.setShortcut("Ctrl+H")
        self.settingAction.setStatusTip(self.tr("设置"))
        self.settingAction.triggered.connect(self.a.osd)
        
        self.aboutAction=QtGui.QAction(QtGui.QIcon(":img/image/mq.png"),self.tr("关于"),self)
        self.aboutAction.setShortcut("Ctrl+j")
        self.aboutAction.triggered.connect(self.about)
        
        self.actionQuit = QtGui.QAction(self.tr("退出"), self, shortcut=QtGui.QKeySequence.Quit)
        self.actionQuit.triggered.connect(self.close)
    
    
    def createMenus(self):
        fileMenu = self.menuBar().addMenu(self.tr("文件"))
#         fileMenu.addAction(self.fileOpenAction)
#         fileMenu.addAction(self.fileSaveAction)
        fileMenu.addAction(self.settingAction)
        fileMenu.addAction(self.actionQuit)
        helpMenu = self.menuBar().addMenu(self.tr("帮助"))
        helpMenu.addAction(self.aboutAction)
        
        
    def createToolBars(self):
        fileToolBar=self.addToolBar("File")
#         fileToolBar.addAction(self.fileOpenAction)
#         fileToolBar.addAction(self.fileSaveAction)
        fileToolBar.addAction(self.settingAction)

    def slotOpenFile(self):
        fileName=QtGui.QFileDialog.getOpenFileName(self)
        if fileName.isEmpty()==False:
            if self.text.document().isEmpty():
                self.loadFile(fileName)
            else:
                newWin=MainWindow()
                newWin.show()
                newWin.loadFile(fileName)

    def slotSaveFile(self):
        pass
    
    def fileSave(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        browser.document().print_(printer)
    
    def fileSaveAs(self):   
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        dlg = QtGui.QPrintDialog(printer, self)

#         if self.textEdit.textCursor().hasSelection():
#             dlg.addEnabledOption(QtGui.QAbstractPrintDialog.PrintSelection)

        dlg.setWindowTitle("Print Document")

        if dlg.exec_() == QtGui.QDialog.Accepted:
            browser.print_(printer)

        del dlg
    
    def about(self):
        QtGui.QMessageBox.about(self, "About", 
                "author:liuxiaohu\n"
                "vision:V1.0.0\n"
                "by Python 2.7 && PyQt4")  
        
class A(QtGui.QWidget):
    def __init__(self, parent=None):
        super(A, self).__init__(parent)

        nameLabel = QtGui.QLabel()
        nameLabel.setPixmap(QtGui.QPixmap(":img/image/note.png"))
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        self.nameEdit = QtGui.QLineEdit()
        self.nameEdit.setStyleSheet(" height:20px;width: 60px;background:white")
        self.nameEdit.setEnabled(False)
        global dataflag#数据刷新标志
        
        self.ConnectButton = QtGui.QPushButton(self.tr("连接"))
#         self.ConnectButton.setStyleSheet(" width: 60px;")
        self.ConnectButton.setIcon(QtGui.QIcon(":img/image/tuxiang/connected.png"))
        self.DisConnectButton = QtGui.QPushButton(self.tr("断开"))
        self.DisConnectButton.setDisabled(True)
#         self.DisConnectButton.setStyleSheet(" width: 60px;")
        self.DisConnectButton.setIcon(QtGui.QIcon(":img/image/tuxiang/disconnected.png"))
        
        self.SettingButton = QtGui.QPushButton()
        self.SettingButton.setIcon(QtGui.QIcon(":img/image/disconnect.png"))
        self.SettingButton.setFlat(True)
        
        '''槽函数''' 
#         self.SettingButton.clicked.connect(self.osd)
        self.ConnectButton.clicked.connect(self.conne)
        self.DisConnectButton.clicked.connect(self.disconne)

        ''''''
#         self.PubLabel = QtGui.QLabel("Retained")

        
        
        self.portSpinbox = QtGui.QSpinBox()
        self.portSpinbox.setMaximum(9999) 
        self.portSpinbox.setMinimum(0)
        self.portSpinbox.setValue(1883)
        
        self.keepaliveSpinbox = QtGui.QSpinBox()
        self.keepaliveSpinbox.setMaximum(9999) 
        self.keepaliveSpinbox.setMinimum(0)
        self.keepaliveSpinbox.setValue(60)

        nameLayout = QtGui.QGridLayout()
        nameLayout.addWidget(nameLabel, 0, 0,)
        nameLayout.addWidget(self.nameEdit, 0, 1)
        nameLayout.addWidget(self.SettingButton,0, 2)
        nameLayout.addWidget(self.ConnectButton, 0, 3)
        nameLayout.addWidget(self.DisConnectButton, 0, 4)  
         
        self.tab=TabDialog()
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(nameLayout)
        mainLayout.addWidget(self.tab)
        mainLayout.addSpacing(6)
#         mainLayout.setMargin(0)
#         mainLayout.addStretch()

        self.setLayout(mainLayout)
   
    def osd(self):  
        global ProfileName, Host, portValue, keepValue, clientids, user, password, visionValue, cleanssionValue, napsBooL, pascheck 
        dialog=ConfigDialog(self)
        result = dialog.exec_()
        for x in range(len(childlist)):
            childlist.remove(childlist[0])
        if result:
            ProfileName, Host, portValue, keepValue, clientids, user, password, visionValue,  cleanssionValue, napsBooL, pascheck = dialog.getsetdata()
            print ProfileName, Host, portValue, keepValue, clientids, user, password, visionValue,  cleanssionValue, napsBooL, pascheck   
            self.nameEdit.setText(ProfileName)
        dialog.destroy()


    def on_connect(self, client, obj, flags, rc):
        print("rc: "+str(rc))
        if str(rc) == '0':
            self.bwThread.updatedicon.emit()#发送信号
           
    
    def icon(self):     
        self.SettingButton.setIcon(QtGui.QIcon(":img/image/connect.png"))  
        self.ConnectButton.setDisabled(True) 
        pub.setDisabled(False)
        sub.setDisabled(False)
    
    def disconne(self): 
        pub.setDisabled(True)
        sub.setDisabled(True)  
        client.disconnect()
        self.bwThread.stop()
        self.SettingButton.setIcon(QtGui.QIcon(":img/image/disconnect.png"))  
        self.ConnectButton.setDisabled(False)
#         self.stopTimer()
    
    def initTimer(self):    
        self.timer = QtCore.QTimer(self) #初始化一个定时器
        self.timer.timeout.connect(self.pingreq) #计时结束调用operate()方法
        self.timer.start((keepValue-1)*1000) #设置计时间隔并启动
    
    def stopTimer(self):    
        self.timer.stop() 
               
    def conne(self):
        try:
            if visionValue == QtCore.QString('V3.1.1'):
                self.mqttvision = mqtt.MQTTv311
            else:
                self.mqttvision = mqtt.MQTTv31
                
            hostname = unicode(QtCore.QString(Host).toUtf8(),'utf8','ignore')
            clientid = unicode(QtCore.QString(clientids).toUtf8(),'utf8','ignore')
            self.username = unicode(QtCore.QString(user).toUtf8(),'utf8','ignore')
            self.pswd = unicode(QtCore.QString(password).toUtf8(),'utf8','ignore')
#             print type(hostname)
            self.DisConnectButton.setDisabled(False)
            
            global client
            client = mqtt.Client(client_id=clientid, clean_session=cleanssionValue, userdata=None, protocol=self.mqttvision)
            client.on_publish = self.on_publish
            client.on_connect = self.on_connect 
            client.on_message = self.on_message
            client.on_subscribe = self.on_subscribe
            
            if napsBooL == True:
                self.setAutho() #设置用户名和密码
            try:

                client.connect(hostname, keepalive = keepValue) #向服务器发起连接
#                 self.initTimer()
                self.bwThread = WorkThread()
                self.bwThread.updated.connect(self.append)
                self.bwThread.updatedicon.connect(self.icon)
                rc = self.bwThread.start()
                return rc
            except socket.error:
                QMessageBox.information(self, self.tr("提示"), self.tr("服务器地址不存在，请重新输入"))
            except ValueError:
                QMessageBox.critical(self, self.tr("提示"), self.tr("请输入正确服务器地址"))
        except NameError:
            QMessageBox.information(self, self.tr("提示"), self.tr("请在设置页面选择相应的配置文件"))
    
    def pingreq(self):
        client.send_pingreq()

    def on_message(self, mqttc, obj, msg):
        global a,b,c
        a = msg.topic
        b = msg.qos
        c = msg.payload
        self.bwThread.updated.emit()#发送信号
#         print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))


    def strformathex(self, str):
        self.index=0
        self.a=list()
        self.b=list(str)
        self.len = len(str)/2
        for i in range(self.len):
            self.a.append(self.b[self.index]+self.b[self.index+1])
            self.a.append(" ")
            self.index=self.index+2
        return ''.join(self.a)
        
    def append(self):
        browser.append(a+" "+str(b)+" "+str(c))    
        m = binascii.b2a_hex(c)
        h = self.strformathex(m)
        h.rstrip()
        t = time.asctime( time.localtime(time.time()) )
        browser.append(a+" "+str(b)+" "+ h + " "+t)  
  

    
    def on_publish(self, mqttc, obj, mid):
        print("message mid is: "+str(mid))
    
    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))
    
    def on_log(self, mqttc, obj, level, string):
        print(string)
    
    def setAutho(self):
        client.username_pw_set(self.username, self.pswd)   


class WorkThread(QtCore.QThread):
    updated  = QtCore.pyqtSignal()#自定义信号，更新数据
    updatedicon  = QtCore.pyqtSignal()#自定义信号，更新图标
    def __init__(self, parent=None):
        super(WorkThread, self).__init__(parent)
        self.flag = 1
        
    def run(self):
        while True:
            if self.flag == 1:
                client.loop()
            else:
                break
            
    def stop(self):  
        print 'setting flag false'  
        self.flag = 0  
        print self.flag  
                        
                
class TabDialog(QtGui.QWidget):
    def __init__(self,  parent=None):
        super(TabDialog, self).__init__(parent)
#         self.setGeometry(300,30,30,30)
#         self.show()
        tabWidget = QtGui.QTabWidget()
        style = "QTabWidget::pane{border:none;\
                 QTabWidget::tab-bar{alignment:left;}}\
                 QTabBar::tab{background:#FFF5EE;color:black;min-width:30ex;min-height:10ex;}\
                 QTabBar::tab:hover{background:rgb(255, 255, 255, 255);}\
                 QTabBar::tab:selected{border-color:white;background:#00BFFF;color:white;}"
        tabWidget.setStyleSheet(style)    
        global pub, sub              
        pub=PublishTab()
        sub=SubTab()
        pub.setDisabled(True)
        sub.setDisabled(True)
        tabWidget.addTab(pub, "Publish")
        tabWidget.addTab(sub, "Subcribe")
    
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(tabWidget,5,1)
        mainLayout.setMargin(1)
        mainLayout.setSpacing(6) 
        self.setLayout(mainLayout) 
        
class PublishTab(QtGui.QWidget):    
    def __init__(self,  parent=None):
        super(PublishTab, self).__init__(parent)     
        publishGroup = QtGui.QGroupBox("Publish Message")
        self.PubLabel = QtGui.QLabel("PubTopic:")
        self.Playload = QtGui.QLabel("Message :")
        self.pubEdit = QtGui.QLineEdit()
        self.pubEdit.setText('/u/R8700/bae45a25f900')
#         self.pubEdit.setText('/u/R8700/bae45524e500')
        self.PlayloadEdit = QtGui.QLineEdit()
        self.PlayloadEdit.setStyleSheet(" height: 37px;")
        self.PlayloadEdit.setText('RKDRDYlQ6oYu9QsY2\x88\v712347682\00\01')
        self.PlayloadEdit.setText('52 4b 44 52 44 59 6c 51 36 6f 59 75 39 51 73 59 32 86 0b 35 39 39 33 36 39 37 31 39 00 01')
        self.PushButton = QtGui.QPushButton(self.tr("Publish"))
        self.PushButton.setStyleSheet(" height: 50px;background:#D3D3D3")
        global pubbrowser
        pubbrowser = QtGui.QTextBrowser()
        pubbrowser.setFrameStyle(QtGui.QFrame.Panel|QtGui.QFrame.Sunken)
#         style = "color: rgb(127, 0, 63);\
#                 background-image: url(:img/image/3.jpg);"
        style = "color:#7CFC00;background:#4D4D4D"
        pubbrowser.setStyleSheet(style)
             
        self.QosLabel = QtGui.QLabel("Qos")
        self.QosComboBox = QtGui.QComboBox()
        self.QosComboBox.addItem("0")
        self.QosComboBox.addItem("1")
        self.QosComboBox.addItem("2") 
        
        self.formatLabel = QtGui.QLabel("Send Format")
        self.formatComboBox = QtGui.QComboBox()
        self.formatComboBox.addItem("HEX")
        self.formatComboBox.addItem("Plain")
        
        self.Retained = QtGui.QCheckBox("Retained")
        
        self.pubLayout = QtGui.QGridLayout()
        self.pubLayout.addWidget(self.PubLabel,0,0)
        self.pubLayout.addWidget(self.pubEdit,0,1)
        self.pubLayout.addWidget(self.QosLabel,0,2)
        self.pubLayout.addWidget(self.QosComboBox,0,3)
        self.pubLayout.addWidget(self.Retained,0,4)
        self.pubLayout.addWidget(self.Playload,1,0)
        self.pubLayout.addWidget(self.PlayloadEdit,1,1)   
        self.pubLayout.addWidget(self.formatLabel,1,2)
        self.pubLayout.addWidget(self.formatComboBox,1,3,1,2)
        self.pubLayout.setSpacing(10)
        
        self.Vlineframe = QtGui.QFrame()
        self.Vlineframe.setFrameStyle(QtGui.QFrame.VLine|QtGui.QFrame.Sunken)
        
        saveButton = QtGui.QPushButton(self.tr("保存"))
        saveButton.setFlat(True)
        saveButton.setIcon(QtGui.QIcon(":img/image/pdf.png"))   
        delButton = QtGui.QPushButton(self.tr("清空"))
        delButton.setFlat(True)          
        delButton.setIcon(QtGui.QIcon(":img/image/recycle.png")) 
        self.buttonLayout1 = QtGui.QGridLayout()
        self.buttonLayout1.addWidget(saveButton,0,0)
        self.buttonLayout1.addWidget(delButton,0,2) 
        
        '''槽函数''' 
        self.PushButton.clicked.connect(self.push)
        saveButton.clicked.connect(self.save)
        delButton.clicked.connect(self.clear)
        ''''''
        
        clientLayout = QtGui.QGridLayout()
        clientLayout.addLayout(self.pubLayout, 0, 0)
        clientLayout.addWidget(self.Vlineframe, 0, 1)
        clientLayout.addWidget(self.PushButton, 0, 2)
        publishGroup.setLayout(clientLayout)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(publishGroup)
        mainLayout.addWidget(pubbrowser)
        mainLayout.addLayout(self.buttonLayout1)
        mainLayout.addSpacing(2)
        self.setLayout(mainLayout)
    
    
           
    def push(self):  
        x = time.asctime( time.localtime(time.time()) )
        self.pubtopic = self.pubEdit.text()
        self.pubtopic = unicode(QtCore.QString(self.pubtopic).toUtf8(),'utf8','ignore')
        self.pubmessage = self.PlayloadEdit.text() 
        self.pubmessage = unicode(self.pubmessage)
        pubbrowser.append('[Pubtopic]:---' + self.pubtopic + '---[' + x + ']')
        pubbrowser.append('[Message]:---' + self.pubmessage + '---[' + x + ']')  
        if self.formatComboBox.currentIndex()  == 0:  
#             self.pubmessage = unicode(self.pubmessage)
            self.pubmessage = bytearray().fromhex(self.pubmessage)

        if self.QosComboBox.currentText()  == QtCore.QString('0'):
            self.qos = 0 
        elif self.QosComboBox.currentText()  == QtCore.QString('1'):
            self.qos = 1 
        if self.QosComboBox.currentText()  == QtCore.QString('2'):
            self.qos = 2 
        self.Retain = self.Retained.checkState() 
#         print self.pubtopic, self.pubmessage, self.qos, self.Retain
        client.publish(self.pubtopic, self.pubmessage)
    
    def save(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        dlg = QtGui.QPrintDialog(printer, self)
        dlg.setWindowTitle("Print Document")
        if dlg.exec_() == QtGui.QDialog.Accepted:
            pubbrowser.print_(printer)
        del dlg
            
    def clear(self):  
        pubbrowser.clear()   
              
        
class SubTab(QtGui.QWidget):    
    def __init__(self,  parent=None):
        super(SubTab, self).__init__(parent)  
        SublishGroup = QtGui.QGroupBox("Subscribe")
        self.SubLabel = QtGui.QLabel("SubTopic:")
        self.SubEdit = QtGui.QLineEdit()
        self.SubEdit.setText('/b/R8700/bae45a25f900')
#         self.SubEdit.setText('/b/R8700/bae45a25f900')
        self.SubEdit.setText('$SYS/broker/bytes/received')
#         self.SubEdit.setText('/u/RKDRD/YlQ6oYu9QsY2')
        self.SubButton = QtGui.QPushButton(self.tr("Subscribe"))
        self.SubButton.setStyleSheet(" height: 50px;background:#D3D3D3")
        global browser
        browser = QtGui.QTextBrowser()
        browser.setFrameStyle(QtGui.QFrame.Panel|QtGui.QFrame.Sunken)
        browser.ensureCursorVisible()#滚动条自动
#         style = "color: rgb(127, 0, 63);\
#                 background-image: url(:img/image/3.jpg);"
        style = "color:#ffffff;background:#000000"
        browser.setStyleSheet(style)
        
        self.QosLabel = QtGui.QLabel("Qos")
        self.QosComboBox = QtGui.QComboBox()
        self.QosComboBox.addItem("0")
        self.QosComboBox.addItem("1")
        self.QosComboBox.addItem("2") 
        
        
        self.pubLayout = QtGui.QGridLayout()
        self.pubLayout.addWidget(self.SubLabel,0,0)
        self.pubLayout.addWidget(self.SubEdit,0,1)
        self.pubLayout.addWidget(self.QosLabel,0,2)
        self.pubLayout.addWidget(self.QosComboBox,0,3) 
        self.pubLayout.setSpacing(10)
        
        self.Vlineframe = QtGui.QFrame()
        self.Vlineframe.setFrameStyle(QtGui.QFrame.VLine|QtGui.QFrame.Sunken)
        
        saveButton = QtGui.QPushButton(self.tr("保存"))
        saveButton.setFlat(True)
        saveButton.setIcon(QtGui.QIcon(":img/image/pdf.png"))   
        delButton = QtGui.QPushButton(self.tr("清空"))
        delButton.setFlat(True)          
        delButton.setIcon(QtGui.QIcon(":img/image/recycle.png")) 
        self.buttonLayout1 = QtGui.QGridLayout()
        self.buttonLayout1.addWidget(saveButton,0,0)
        self.buttonLayout1.addWidget(delButton,0,2) 
        
        '''槽函数''' 
        self.SubButton.clicked.connect(self.sub)
        saveButton.clicked.connect(self.save)
        delButton.clicked.connect(self.clear)
        ''''''
        
        clientLayout = QtGui.QGridLayout()
        clientLayout.addLayout(self.pubLayout, 0, 0)
        clientLayout.addWidget(self.Vlineframe, 0, 1)
        clientLayout.addWidget(self.SubButton, 0, 2)
#         clientLayout.addWidget(self.browser, 1, 0, 1, 3)
#         self.pubLayout.setSpacing(2)
        SublishGroup.setLayout(clientLayout)
        
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(SublishGroup)
        mainLayout.addWidget(browser)
        mainLayout.addLayout(self.buttonLayout1)
        mainLayout.addSpacing(2)
        self.setLayout(mainLayout)
          
    def sub(self):  
        x = time.asctime( time.localtime(time.time()) )
        self.subtopic = self.SubEdit.text()
        self.subtopic = str(self.subtopic)#类型转换很重要
        browser.append('[Subtopic]:---' + self.subtopic +'---[' + x + ']')    
        if self.QosComboBox.currentText()  == QtCore.QString('0'):
            self.qos = 0 
        elif self.QosComboBox.currentText()  == QtCore.QString('1'):
            self.qos = 1 
        if self.QosComboBox.currentText()  == QtCore.QString('2'):
            self.qos = 2 
        client.subscribe(self.subtopic,self.qos)

    def save(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        dlg = QtGui.QPrintDialog(printer, self)
        dlg.setWindowTitle("Print Document")
        if dlg.exec_() == QtGui.QDialog.Accepted:
            browser.print_(printer)
        del dlg
    
    def clear(self):  
        browser.clear()   
        
            
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    splash = QtGui.QSplashScreen(QtGui.QPixmap(":img/image/mqtt.GIF"))
    splash.show()
    app.processEvents()
    mainWin = A()
    mainWin = MainWindow()
    mainWin.show()
    splash.finish(mainWin)
    sys.exit(app.exec_())   