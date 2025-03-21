from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        MainWindow.setFixedSize(400, 300)  # 固定窗口大小
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.comboBox_ports = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_ports.setGeometry(QtCore.QRect(50, 20, 300, 30))
        self.comboBox_ports.setObjectName("comboBox_ports")
        self.comboBox_ports.setStyleSheet("font-size: 14px; padding: 5px;")

        self.pushButton_connect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connect.setGeometry(QtCore.QRect(150, 60, 100, 30))
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.pushButton_connect.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(50, 100, 50, 50)
        self.gridLayout.setSpacing(20)

        self.pushButton_relay1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_relay1.setObjectName("pushButton_relay1")
        self.pushButton_relay1.setStyleSheet(self.get_button_style("gray"))
        self.gridLayout.addWidget(self.pushButton_relay1, 0, 0)

        self.pushButton_relay2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_relay2.setObjectName("pushButton_relay2")
        self.pushButton_relay2.setStyleSheet(self.get_button_style("gray"))
        self.gridLayout.addWidget(self.pushButton_relay2, 0, 1)

        self.pushButton_relay3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_relay3.setObjectName("pushButton_relay3")
        self.pushButton_relay3.setStyleSheet(self.get_button_style("gray"))
        self.gridLayout.addWidget(self.pushButton_relay3, 1, 0)

        self.pushButton_relay4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_relay4.setObjectName("pushButton_relay4")
        self.pushButton_relay4.setStyleSheet(self.get_button_style("gray"))
        self.gridLayout.addWidget(self.pushButton_relay4, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def get_button_style(self, color):
        return f"""
            QPushButton {{
                font-size: 14px;
                background-color: {color};
                color: white;
                border-radius: 5px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {color}; /* 禁用鼠标悬停时的颜色变化 */
            }}
        """

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "继电器控制"))
        self.pushButton_connect.setText(_translate("MainWindow", "连接"))
        self.pushButton_relay1.setText(_translate("MainWindow", "继电器1"))
        self.pushButton_relay2.setText(_translate("MainWindow", "继电器2"))
        self.pushButton_relay3.setText(_translate("MainWindow", "继电器3"))
        self.pushButton_relay4.setText(_translate("MainWindow", "继电器4"))
