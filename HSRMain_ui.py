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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(682, 540)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fileButton = QPushButton(self.widget)
        self.fileButton.setObjectName(u"fileButton")
        self.fileButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.fileButton)

        self.fileLabel = QLabel(self.widget)
        self.fileLabel.setObjectName(u"fileLabel")

        self.horizontalLayout.addWidget(self.fileLabel)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)

        self.horizontalLayout_8.addLayout(self.horizontalLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)

        self.maxUidLabel = QLabel(self.widget)
        self.maxUidLabel.setObjectName(u"maxUidLabel")
        self.maxUidLabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.horizontalLayout_8.addWidget(self.maxUidLabel)

        self.horizontalLayout_8.setStretch(0, 3)
        self.horizontalLayout_8.setStretch(1, 1)
        self.horizontalLayout_8.setStretch(2, 2)

        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.groupBox = QGroupBox(self.widget)
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
        self.label_cn.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

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
        self.label_b.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

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
        self.label_ya.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

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
        self.label_ou.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

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
        self.label_mei.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

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
        self.label_gat.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

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

        self.verticalLayout_3.addWidget(self.groupBox)

        self.infoBrowser = QTextBrowser(self.widget)
        self.infoBrowser.setObjectName(u"infoBrowser")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(11)
        self.infoBrowser.setFont(font)

        self.verticalLayout_3.addWidget(self.infoBrowser)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.progressBar = QProgressBar(self.widget)
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

        self.progressLabel = QLabel(self.widget)
        self.progressLabel.setObjectName(u"progressLabel")
        self.progressLabel.setAlignment(Qt.AlignCenter)
        self.progressLabel.setWordWrap(False)
        self.progressLabel.setMargin(0)

        self.horizontalLayout_11.addWidget(self.progressLabel)

        self.timeLabel = QLabel(self.widget)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.timeLabel)

        self.horizontalLayout_11.setStretch(0, 6)
        self.horizontalLayout_11.setStretch(1, 1)
        self.horizontalLayout_11.setStretch(2, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.fileExeButton = QPushButton(self.widget)
        self.fileExeButton.setObjectName(u"fileExeButton")
        self.fileExeButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_12.addWidget(self.fileExeButton)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.randomUidButton = QPushButton(self.widget)
        self.randomUidButton.setObjectName(u"randomUidButton")
        self.randomUidButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_10.addWidget(self.randomUidButton)

        self.maxLenLineEdit = QLineEdit(self.widget)
        self.maxLenLineEdit.setObjectName(u"maxLenLineEdit")
        self.maxLenLineEdit.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_10.addWidget(self.maxLenLineEdit)

        self.horizontalLayout_10.setStretch(0, 2)
        self.horizontalLayout_10.setStretch(1, 1)

        self.horizontalLayout_12.addLayout(self.horizontalLayout_10)

        self.interruptButton = QPushButton(self.widget)
        self.interruptButton.setObjectName(u"interruptButton")
        self.interruptButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_12.addWidget(self.interruptButton)

        self.continueButton = QPushButton(self.widget)
        self.continueButton.setObjectName(u"continueButton")
        self.continueButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_12.addWidget(self.continueButton)

        self.horizontalLayout_12.setStretch(0, 3)
        self.horizontalLayout_12.setStretch(1, 3)
        self.horizontalLayout_12.setStretch(2, 1)
        self.horizontalLayout_12.setStretch(3, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_12)


        self.verticalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 682, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setAcceptDrops(False)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"HSR\u6570\u636e\u722c\u53d6", None))
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
    # retranslateUi

