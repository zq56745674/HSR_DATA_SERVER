# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HSRMain.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1007, 687)
        self.actionLogin = QAction(MainWindow)
        self.actionLogin.setObjectName(u"actionLogin")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAqua = QAction(MainWindow)
        self.actionAqua.setObjectName(u"actionAqua")
        self.actionMacOS = QAction(MainWindow)
        self.actionMacOS.setObjectName(u"actionMacOS")
        self.actionNeonButtons = QAction(MainWindow)
        self.actionNeonButtons.setObjectName(u"actionNeonButtons")
        self.actionUbuntu = QAction(MainWindow)
        self.actionUbuntu.setObjectName(u"actionUbuntu")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setContextMenuPolicy(Qt.NoContextMenu)
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tabWidget = QTabWidget(self.widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidgetPage1 = QWidget()
        self.tabWidgetPage1.setObjectName(u"tabWidgetPage1")
        self.verticalLayout_4 = QVBoxLayout(self.tabWidgetPage1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fileButton = QPushButton(self.tabWidgetPage1)
        self.fileButton.setObjectName(u"fileButton")
        self.fileButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.fileButton)

        self.fileLabel = QLabel(self.tabWidgetPage1)
        self.fileLabel.setObjectName(u"fileLabel")

        self.horizontalLayout.addWidget(self.fileLabel)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)

        self.horizontalLayout_8.addLayout(self.horizontalLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)

        self.maxUidLabel = QLabel(self.tabWidgetPage1)
        self.maxUidLabel.setObjectName(u"maxUidLabel")
        self.maxUidLabel.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_8.addWidget(self.maxUidLabel)

        self.horizontalLayout_8.setStretch(0, 3)
        self.horizontalLayout_8.setStretch(1, 1)
        self.horizontalLayout_8.setStretch(2, 2)

        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.groupBox = QGroupBox(self.tabWidgetPage1)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_9 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioButton_cn = QRadioButton(self.groupBox)
        self.radioButton_cn.setObjectName(u"radioButton_cn")

        self.horizontalLayout_2.addWidget(self.radioButton_cn)

        self.label_cn = QLabel(self.groupBox)
        self.label_cn.setObjectName(u"label_cn")
        self.label_cn.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_2.addWidget(self.label_cn)

        self.minUidEdit_cn = QLineEdit(self.groupBox)
        self.minUidEdit_cn.setObjectName(u"minUidEdit_cn")
        self.minUidEdit_cn.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_2.addWidget(self.minUidEdit_cn)

        self.maxUidEdit_cn = QLineEdit(self.groupBox)
        self.maxUidEdit_cn.setObjectName(u"maxUidEdit_cn")
        self.maxUidEdit_cn.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_2.addWidget(self.maxUidEdit_cn)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton_b = QRadioButton(self.groupBox)
        self.radioButton_b.setObjectName(u"radioButton_b")

        self.horizontalLayout_3.addWidget(self.radioButton_b)

        self.label_b = QLabel(self.groupBox)
        self.label_b.setObjectName(u"label_b")
        self.label_b.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_3.addWidget(self.label_b)

        self.minUidEdit_b = QLineEdit(self.groupBox)
        self.minUidEdit_b.setObjectName(u"minUidEdit_b")
        self.minUidEdit_b.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_3.addWidget(self.minUidEdit_b)

        self.maxUidEdit_b = QLineEdit(self.groupBox)
        self.maxUidEdit_b.setObjectName(u"maxUidEdit_b")
        self.maxUidEdit_b.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_3.addWidget(self.maxUidEdit_b)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.horizontalLayout_3.setStretch(2, 1)
        self.horizontalLayout_3.setStretch(3, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radioButton_ya = QRadioButton(self.groupBox)
        self.radioButton_ya.setObjectName(u"radioButton_ya")

        self.horizontalLayout_4.addWidget(self.radioButton_ya)

        self.label_ya = QLabel(self.groupBox)
        self.label_ya.setObjectName(u"label_ya")
        self.label_ya.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_4.addWidget(self.label_ya)

        self.minUidEdit_ya = QLineEdit(self.groupBox)
        self.minUidEdit_ya.setObjectName(u"minUidEdit_ya")
        self.minUidEdit_ya.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_4.addWidget(self.minUidEdit_ya)

        self.maxUidEdit_ya = QLineEdit(self.groupBox)
        self.maxUidEdit_ya.setObjectName(u"maxUidEdit_ya")
        self.maxUidEdit_ya.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_4.addWidget(self.maxUidEdit_ya)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 3)
        self.horizontalLayout_4.setStretch(2, 1)
        self.horizontalLayout_4.setStretch(3, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.radioButton_ou = QRadioButton(self.groupBox)
        self.radioButton_ou.setObjectName(u"radioButton_ou")

        self.horizontalLayout_5.addWidget(self.radioButton_ou)

        self.label_ou = QLabel(self.groupBox)
        self.label_ou.setObjectName(u"label_ou")
        self.label_ou.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_5.addWidget(self.label_ou)

        self.minUidEdit_ou = QLineEdit(self.groupBox)
        self.minUidEdit_ou.setObjectName(u"minUidEdit_ou")
        self.minUidEdit_ou.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_5.addWidget(self.minUidEdit_ou)

        self.maxUidEdit_ou = QLineEdit(self.groupBox)
        self.maxUidEdit_ou.setObjectName(u"maxUidEdit_ou")
        self.maxUidEdit_ou.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_5.addWidget(self.maxUidEdit_ou)

        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 3)
        self.horizontalLayout_5.setStretch(2, 1)
        self.horizontalLayout_5.setStretch(3, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.radioButton_mei = QRadioButton(self.groupBox)
        self.radioButton_mei.setObjectName(u"radioButton_mei")

        self.horizontalLayout_6.addWidget(self.radioButton_mei)

        self.label_mei = QLabel(self.groupBox)
        self.label_mei.setObjectName(u"label_mei")
        self.label_mei.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_6.addWidget(self.label_mei)

        self.minUidEdit_mei = QLineEdit(self.groupBox)
        self.minUidEdit_mei.setObjectName(u"minUidEdit_mei")
        self.minUidEdit_mei.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_6.addWidget(self.minUidEdit_mei)

        self.maxUidEdit_mei = QLineEdit(self.groupBox)
        self.maxUidEdit_mei.setObjectName(u"maxUidEdit_mei")
        self.maxUidEdit_mei.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_6.addWidget(self.maxUidEdit_mei)

        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 3)
        self.horizontalLayout_6.setStretch(2, 1)
        self.horizontalLayout_6.setStretch(3, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.radioButton_gat = QRadioButton(self.groupBox)
        self.radioButton_gat.setObjectName(u"radioButton_gat")

        self.horizontalLayout_7.addWidget(self.radioButton_gat)

        self.label_gat = QLabel(self.groupBox)
        self.label_gat.setObjectName(u"label_gat")
        self.label_gat.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_7.addWidget(self.label_gat)

        self.minUidEdit_gat = QLineEdit(self.groupBox)
        self.minUidEdit_gat.setObjectName(u"minUidEdit_gat")
        self.minUidEdit_gat.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_7.addWidget(self.minUidEdit_gat)

        self.maxUidEdit_gat = QLineEdit(self.groupBox)
        self.maxUidEdit_gat.setObjectName(u"maxUidEdit_gat")
        self.maxUidEdit_gat.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_7.addWidget(self.maxUidEdit_gat)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 3)
        self.horizontalLayout_7.setStretch(2, 1)
        self.horizontalLayout_7.setStretch(3, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_9.addLayout(self.verticalLayout_2)

        self.horizontalLayout_9.setStretch(0, 3)

        self.verticalLayout_4.addWidget(self.groupBox)

        self.infoBrowser = QTextBrowser(self.tabWidgetPage1)
        self.infoBrowser.setObjectName(u"infoBrowser")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(11)
        self.infoBrowser.setFont(font)

        self.verticalLayout_4.addWidget(self.infoBrowser)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.progressBar = QProgressBar(self.tabWidgetPage1)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(0, 0))
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"            border: 2px solid grey;\n"
"            border-radius: 5px;\n"
"            text-align: center;\n"
"        }\n"
"\n"
"        QProgressBar::chunk {\n"
"            background-color: #05B8CC;\n"
"            width: 20px;\n"
"        }")
        self.progressBar.setValue(0)

        self.horizontalLayout_11.addWidget(self.progressBar)

        self.progressLabel = QLabel(self.tabWidgetPage1)
        self.progressLabel.setObjectName(u"progressLabel")
        self.progressLabel.setWordWrap(False)
        self.progressLabel.setMargin(0)

        self.horizontalLayout_11.addWidget(self.progressLabel)

        self.timeLabel = QLabel(self.tabWidgetPage1)
        self.timeLabel.setObjectName(u"timeLabel")

        self.horizontalLayout_11.addWidget(self.timeLabel)

        self.horizontalLayout_11.setStretch(0, 6)
        self.horizontalLayout_11.setStretch(1, 1)
        self.horizontalLayout_11.setStretch(2, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.fileExeButton = QPushButton(self.tabWidgetPage1)
        self.fileExeButton.setObjectName(u"fileExeButton")
        self.fileExeButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_12.addWidget(self.fileExeButton)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.randomUidButton = QPushButton(self.tabWidgetPage1)
        self.randomUidButton.setObjectName(u"randomUidButton")
        self.randomUidButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_10.addWidget(self.randomUidButton)

        self.maxLenLineEdit = QLineEdit(self.tabWidgetPage1)
        self.maxLenLineEdit.setObjectName(u"maxLenLineEdit")
        self.maxLenLineEdit.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_10.addWidget(self.maxLenLineEdit)

        self.horizontalLayout_10.setStretch(0, 2)
        self.horizontalLayout_10.setStretch(1, 1)

        self.horizontalLayout_12.addLayout(self.horizontalLayout_10)

        self.interruptButton = QPushButton(self.tabWidgetPage1)
        self.interruptButton.setObjectName(u"interruptButton")
        self.interruptButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_12.addWidget(self.interruptButton)

        self.continueButton = QPushButton(self.tabWidgetPage1)
        self.continueButton.setObjectName(u"continueButton")
        self.continueButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_12.addWidget(self.continueButton)

        self.horizontalLayout_12.setStretch(0, 3)
        self.horizontalLayout_12.setStretch(1, 3)
        self.horizontalLayout_12.setStretch(2, 1)
        self.horizontalLayout_12.setStretch(3, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_12)

        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tabWidgetPage2 = QWidget()
        self.tabWidgetPage2.setObjectName(u"tabWidgetPage2")
        self.verticalLayout_5 = QVBoxLayout(self.tabWidgetPage2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.fileButton_2 = QPushButton(self.tabWidgetPage2)
        self.fileButton_2.setObjectName(u"fileButton_2")
        self.fileButton_2.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_13.addWidget(self.fileButton_2)

        self.fileLabel_2 = QLabel(self.tabWidgetPage2)
        self.fileLabel_2.setObjectName(u"fileLabel_2")

        self.horizontalLayout_13.addWidget(self.fileLabel_2)

        self.fileZZZExeButton = QPushButton(self.tabWidgetPage2)
        self.fileZZZExeButton.setObjectName(u"fileZZZExeButton")
        self.fileZZZExeButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_13.addWidget(self.fileZZZExeButton)

        self.horizontalLayout_13.setStretch(0, 1)
        self.horizontalLayout_13.setStretch(1, 3)
        self.horizontalLayout_13.setStretch(2, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_13)

        self.textBrowser = QTextBrowser(self.tabWidgetPage2)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_5.addWidget(self.textBrowser)

        self.tabWidget.addTab(self.tabWidgetPage2, "")
        self.tabWidgetPage3 = QWidget()
        self.tabWidgetPage3.setObjectName(u"tabWidgetPage3")
        self.verticalLayout_6 = QVBoxLayout(self.tabWidgetPage3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label = QLabel(self.tabWidgetPage3)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"\u9ed1\u4f53"])
        font1.setPointSize(12)
        self.label.setFont(font1)

        self.verticalLayout_6.addWidget(self.label)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.fromComboBox = QComboBox(self.tabWidgetPage3)
        self.fromComboBox.addItem("")
        self.fromComboBox.addItem("")
        self.fromComboBox.addItem("")
        self.fromComboBox.setObjectName(u"fromComboBox")
        self.fromComboBox.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_16.addWidget(self.fromComboBox)

        self.toComboBox = QComboBox(self.tabWidgetPage3)
        self.toComboBox.addItem("")
        self.toComboBox.addItem("")
        self.toComboBox.setObjectName(u"toComboBox")
        self.toComboBox.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_16.addWidget(self.toComboBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_2)

        self.translateButton = QPushButton(self.tabWidgetPage3)
        self.translateButton.setObjectName(u"translateButton")
        self.translateButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_16.addWidget(self.translateButton)

        self.horizontalLayout_16.setStretch(0, 1)
        self.horizontalLayout_16.setStretch(1, 1)
        self.horizontalLayout_16.setStretch(2, 4)

        self.verticalLayout_6.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.fromTextEdit = QPlainTextEdit(self.tabWidgetPage3)
        self.fromTextEdit.setObjectName(u"fromTextEdit")
        font2 = QFont()
        font2.setPointSize(13)
        self.fromTextEdit.setFont(font2)

        self.horizontalLayout_14.addWidget(self.fromTextEdit)

        self.toTextBrowser = QTextBrowser(self.tabWidgetPage3)
        self.toTextBrowser.setObjectName(u"toTextBrowser")
        self.toTextBrowser.setFont(font2)

        self.horizontalLayout_14.addWidget(self.toTextBrowser)

        self.horizontalLayout_14.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_2 = QLabel(self.tabWidgetPage3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.horizontalLayout_17.addWidget(self.label_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_3)

        self.sendAIButton = QPushButton(self.tabWidgetPage3)
        self.sendAIButton.setObjectName(u"sendAIButton")
        self.sendAIButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_17.addWidget(self.sendAIButton)

        self.horizontalLayout_17.setStretch(0, 1)
        self.horizontalLayout_17.setStretch(1, 2)

        self.verticalLayout_6.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.fromTextEdit_2 = QPlainTextEdit(self.tabWidgetPage3)
        self.fromTextEdit_2.setObjectName(u"fromTextEdit_2")
        self.fromTextEdit_2.setFont(font2)

        self.horizontalLayout_15.addWidget(self.fromTextEdit_2)

        self.toTextBrowser_2 = QTextBrowser(self.tabWidgetPage3)
        self.toTextBrowser_2.setObjectName(u"toTextBrowser_2")
        self.toTextBrowser_2.setFont(font2)

        self.horizontalLayout_15.addWidget(self.toTextBrowser_2)

        self.horizontalLayout_15.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_15)

        self.tabWidget.addTab(self.tabWidgetPage3, "")
        self.tabWidgetPage4 = QWidget()
        self.tabWidgetPage4.setObjectName(u"tabWidgetPage4")
        self.verticalLayout_8 = QVBoxLayout(self.tabWidgetPage4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.fileButton_3 = QPushButton(self.tabWidgetPage4)
        self.fileButton_3.setObjectName(u"fileButton_3")
        self.fileButton_3.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_19.addWidget(self.fileButton_3)

        self.fileLabel_3 = QLabel(self.tabWidgetPage4)
        self.fileLabel_3.setObjectName(u"fileLabel_3")

        self.horizontalLayout_19.addWidget(self.fileLabel_3)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_4)

        self.dataAnalysisButton = QPushButton(self.tabWidgetPage4)
        self.dataAnalysisButton.setObjectName(u"dataAnalysisButton")
        self.dataAnalysisButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_19.addWidget(self.dataAnalysisButton)

        self.horizontalLayout_19.setStretch(0, 1)
        self.horizontalLayout_19.setStretch(1, 2)
        self.horizontalLayout_19.setStretch(2, 2)

        self.verticalLayout_7.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.tableWidget = QTableWidget(self.tabWidgetPage4)
        self.tableWidget.setObjectName(u"tableWidget")

        self.horizontalLayout_18.addWidget(self.tableWidget)

        self.widget_2 = QWidget(self.tabWidgetPage4)
        self.widget_2.setObjectName(u"widget_2")

        self.horizontalLayout_18.addWidget(self.widget_2)

        self.horizontalLayout_18.setStretch(0, 1)
        self.horizontalLayout_18.setStretch(1, 2)

        self.verticalLayout_7.addLayout(self.horizontalLayout_18)


        self.verticalLayout_8.addLayout(self.verticalLayout_7)

        self.tabWidget.addTab(self.tabWidgetPage4, "")

        self.verticalLayout_3.addWidget(self.tabWidget)


        self.verticalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1007, 26))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu.setMinimumSize(QSize(0, 0))
        self.menu.setSizeIncrement(QSize(0, 0))
        self.menu.setBaseSize(QSize(0, 0))
        self.menuToggle = QMenu(self.menu)
        self.menuToggle.setObjectName(u"menuToggle")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setAcceptDrops(False)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionLogin)
        self.menu.addSeparator()
        self.menu.addAction(self.menuToggle.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.actionExit)
        self.menuToggle.addAction(self.actionAqua)
        self.menuToggle.addAction(self.actionMacOS)
        self.menuToggle.addAction(self.actionNeonButtons)
        self.menuToggle.addAction(self.actionUbuntu)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"HSR\u6570\u636e\u722c\u53d6", None))
        self.actionLogin.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionAqua.setText(QCoreApplication.translate("MainWindow", u"Aqua", None))
        self.actionMacOS.setText(QCoreApplication.translate("MainWindow", u"MacOS", None))
        self.actionNeonButtons.setText(QCoreApplication.translate("MainWindow", u"NeonButtons", None))
        self.actionUbuntu.setText(QCoreApplication.translate("MainWindow", u"Ubuntu", None))
        self.fileButton.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4f20\u6587\u4ef6", None))
        self.fileLabel.setText(QCoreApplication.translate("MainWindow", u"\u672a\u9009\u62e9\u6587\u4ef6", None))
        self.maxUidLabel.setText(QCoreApplication.translate("MainWindow", u"\u6700\u5927uid\uff1a", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u5d29\u574f\uff1a\u661f\u7a79\u94c1\u9053 - UID", None))
        self.radioButton_cn.setText(QCoreApplication.translate("MainWindow", u"\u56fd\u670d", None))
        self.label_cn.setText("")
        self.minUidEdit_cn.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.minUidEdit_cn.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.maxUidEdit_cn.setText(QCoreApplication.translate("MainWindow", u"100000", None))
        self.maxUidEdit_cn.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.radioButton_b.setText(QCoreApplication.translate("MainWindow", u"B\u670d", None))
        self.label_b.setText("")
        self.minUidEdit_b.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.minUidEdit_b.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.maxUidEdit_b.setText(QCoreApplication.translate("MainWindow", u"100000", None))
        self.maxUidEdit_b.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.radioButton_ya.setText(QCoreApplication.translate("MainWindow", u"\u4e9a\u670d", None))
        self.label_ya.setText("")
        self.minUidEdit_ya.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.minUidEdit_ya.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.maxUidEdit_ya.setText(QCoreApplication.translate("MainWindow", u"100000", None))
        self.maxUidEdit_ya.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.radioButton_ou.setText(QCoreApplication.translate("MainWindow", u"\u6b27\u670d", None))
        self.label_ou.setText("")
        self.minUidEdit_ou.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.minUidEdit_ou.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.maxUidEdit_ou.setText(QCoreApplication.translate("MainWindow", u"100000", None))
        self.maxUidEdit_ou.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.radioButton_mei.setText(QCoreApplication.translate("MainWindow", u"\u7f8e\u670d", None))
        self.label_mei.setText("")
        self.minUidEdit_mei.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.minUidEdit_mei.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.maxUidEdit_mei.setText(QCoreApplication.translate("MainWindow", u"100000", None))
        self.maxUidEdit_mei.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.radioButton_gat.setText(QCoreApplication.translate("MainWindow", u"\u6e2f\u6fb3\u53f0\u670d", None))
        self.label_gat.setText("")
        self.minUidEdit_gat.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.minUidEdit_gat.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.maxUidEdit_gat.setText(QCoreApplication.translate("MainWindow", u"100000", None))
        self.maxUidEdit_gat.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.infoBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Arial'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.progressLabel.setText(QCoreApplication.translate("MainWindow", u"0/0", None))
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.fileExeButton.setText(QCoreApplication.translate("MainWindow", u"\u6267\u884c\u6587\u4ef6", None))
        self.randomUidButton.setText(QCoreApplication.translate("MainWindow", u"\u968f\u673a\u722c\u53d6UID", None))
        self.maxLenLineEdit.setText(QCoreApplication.translate("MainWindow", u"10000", None))
        self.maxLenLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165...", None))
        self.interruptButton.setText(QCoreApplication.translate("MainWindow", u"\u4e2d\u65ad", None))
        self.continueButton.setText(QCoreApplication.translate("MainWindow", u"\u7ee7\u7eed", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), QCoreApplication.translate("MainWindow", u"HSR\u6570\u636e\u722c\u53d6", None))
        self.fileButton_2.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4f20\u6587\u4ef6", None))
        self.fileLabel_2.setText(QCoreApplication.translate("MainWindow", u"\u672a\u9009\u62e9\u6587\u4ef6", None))
        self.fileZZZExeButton.setText(QCoreApplication.translate("MainWindow", u"\u5904\u7406", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage2), QCoreApplication.translate("MainWindow", u"ZZZ\u6587\u4ef6\u5904\u7406", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u767e\u5ea6\u7ffb\u8bd1", None))
        self.fromComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u81ea\u52a8", None))
        self.fromComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u4e2d\u6587", None))
        self.fromComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"\u82f1\u6587", None))

        self.toComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u4e2d\u6587", None))
        self.toComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u82f1\u6587", None))

        self.translateButton.setText(QCoreApplication.translate("MainWindow", u"\u7ffb\u8bd1", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"AI\u5bf9\u8bdd", None))
        self.sendAIButton.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage3), QCoreApplication.translate("MainWindow", u"\u767e\u5ea6API", None))
        self.fileButton_3.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4f20\u6587\u4ef6", None))
        self.fileLabel_3.setText(QCoreApplication.translate("MainWindow", u"\u672a\u9009\u62e9\u6587\u4ef6", None))
        self.dataAnalysisButton.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5904\u7406", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage4), QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5206\u6790", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u83dc\u5355", None))
        self.menuToggle.setTitle(QCoreApplication.translate("MainWindow", u"Theme", None))
    # retranslateUi

