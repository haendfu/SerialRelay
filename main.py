import sys
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer
from ui_main import Ui_MainWindow

class RelayController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.serial_port = None

        # 定时器用于定时查询继电器状态
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_relay_states)

        # Populate available COM ports with device names
        for port in serial.tools.list_ports.comports():
            self.ui.comboBox_ports.addItem(f"{port.device} {port.description}")

        # Connect buttons to actions
        self.ui.pushButton_relay1.clicked.connect(lambda: self.toggle_relay(1))
        self.ui.pushButton_relay2.clicked.connect(lambda: self.toggle_relay(2))
        self.ui.pushButton_relay3.clicked.connect(lambda: self.toggle_relay(3))
        self.ui.pushButton_relay4.clicked.connect(lambda: self.toggle_relay(4))

        # 绑定连接按钮到 connect_serial 方法
        self.ui.pushButton_connect.clicked.connect(self.connect_serial)

    def get_available_ports(self):
        """
        获取可用的串口列表。
        """
        try:
            ports = serial.tools.list_ports.comports()
            return [port.device for port in ports]
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取串口列表失败: {e}")
            return []

    def connect_serial(self):
        """
        连接或断开串口。
        """
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.close()
                self.ui.pushButton_connect.setText("连接")
                self.timer.stop()  # 停止状态更新
                QMessageBox.information(self, "信息", "串口已断开")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"断开串口失败: {e}")
        else:
            port = self.ui.comboBox_ports.currentText().split()[0]  # 取第一个单词作为串口号
            if not port:
                QMessageBox.warning(self, "警告", "未选择串口")
                return
            try:
                self.serial_port = serial.Serial(port, baudrate=9600, timeout=1)
                self.ui.pushButton_connect.setText("断开")
                self.timer.start(1000)  # 每秒更新一次状态
                self.update_relay_states()  # 主动更新继电器状态
            except serial.SerialException as e:
                QMessageBox.critical(self, "错误", f"无法连接到串口: {e}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"未知错误: {e}")

    def control_relay(self, relay_number, state):
        """
        控制继电器开关，支持新的通讯协议。
        :param relay_number: 继电器编号 (1-254)
        :param state: True 表示开，False 表示关
        """
        if not self.serial_port or not self.serial_port.is_open:
            QMessageBox.warning(self, "警告", "请先连接串口")
            return
        try:
            # 数据1固定为0xA0
            data1 = 0xA0
            # 数据2为继电器地址码 (1-254)
            data2 = relay_number
            # 数据3为操作数据 (0x00关, 0x01开, 0x03开(反馈), 0x04取反(反馈))
            data3 = 0x01 if state else 0x00
            # 校验和 = (数据1 + 数据2 + 数据3) % 0x100
            checksum = (data1 + data2 + data3) % 0x100
            # 构造命令
            command = bytes([data1, data2, data3, checksum])
            self.serial_port.write(command)
            # 更新滑动开关状态
            self.update_relay_states()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"发送命令失败: {e}")

    def toggle_relay(self, relay_number):
        """
        切换继电器状态。
        :param relay_number: 继电器编号 (1-254)
        """
        if not self.serial_port or not self.serial_port.is_open:
            QMessageBox.warning(self, "警告", "请先连接串口")
            return
        state = self.query_relay_state(relay_number)
        if state is None:
            QMessageBox.warning(self, "警告", f"无法获取继电器{relay_number}的状态")
            return
        self.control_relay(relay_number, not state)

    def update_relay_states(self):
        """
        定时查询所有继电器的状态并更新显示，同时更新按钮的背景色。
        """
        for relay_number in range(1, 5):  # 假设有4路继电器
            state = self.query_relay_state(relay_number)
            if state is not None:
                # 更新按钮背景色
                button = getattr(self.ui, f"pushButton_relay{relay_number}")
                color = "green" if state else "gray"
                button.setStyleSheet(self.ui.get_button_style(color))

    def query_relay_state(self, relay_number):
        """
        查询继电器状态。
        :param relay_number: 继电器编号 (1-254)
        :return: True 表示开，False 表示关，None 表示查询失败
        """
        if not self.serial_port or not self.serial_port.is_open:
            return None
        try:
            # 数据1固定为0xA0
            data1 = 0xA0
            # 数据2为继电器地址码 (1-254)
            data2 = relay_number
            # 数据3为查询状态 (0x05)
            data3 = 0x05
            # 校验和 = (数据1 + 数据2 + 数据3) % 0x100
            checksum = (data1 + data2 + data3) % 0x100
            # 构造命令
            command = bytes([data1, data2, data3, checksum])
            self.serial_port.write(command)
            # 读取返回数据
            response = self.serial_port.read(4)
            if len(response) == 4 and response[0] == data1 and response[1] == data2:
                return response[2] == 0x01  # 返回 True 表示开，False 表示关
        except Exception:
            pass
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RelayController()
    window.show()
    sys.exit(app.exec_())
