## Ex 5-10. QGroupBox.

import sys

from PyQt5.QtCore import QTimer, QEvent
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtWidgets import (QApplication, QWidget, QGroupBox, QRadioButton, QPushButton, QGridLayout, QVBoxLayout,
                             QLabel, QLineEdit, QTextEdit, QComboBox, QMessageBox)
from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus.server import ModbusTcpServer, ModbusSerialServer
import time


# MODBUS RTU 만들어야할것. 1. SLAVE ID가 같아야만 적용되야한다. SERIAL PORT가 동일해야한다.(그래야 연결가능하니)
class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        app.exec_()

    def initUI(self):
        mainLayout = QGridLayout()

        # Header Section
        headerLayout = QGridLayout()
        headerLayout.addWidget(self.createFirstExclusiveGroup(), 0, 0)
        headerLayout.addWidget(self.createMasterGroup(), 0, 1)
        headerLayout.addWidget(self.createMaster2Group(), 0, 2)
        headerLayout.addWidget(self.createTcpGroup(), 0, 3)
        mainLayout.addLayout(headerLayout, 0, 0)

        # Content Section
        middleLayout = QGridLayout()
        middleLayout.addWidget(self.createModBusPollGroup(), 0, 0)
        middleLayout.addWidget(self.createModBusSlaveGroup(), 0, 1)
        mainLayout.addLayout(middleLayout, 1, 0)

        # Footer Section
        footerLayout = QGridLayout()
        footerLayout.addWidget(self.createLogGroup(), 0, 0)
        mainLayout.addLayout(footerLayout, 2, 0)
        # mainLayout = Layout의역할

        self.setLayout(mainLayout)
        self.setWindowTitle('Box Layout')
        self.setGeometry(300, 300, 1480, 640)
        self.show()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.connect_to_modbus)

    def createFirstExclusiveGroup(self):
        groupbox = QGroupBox('TCP MODE & Master MODE SELECT')
        groupbox.setFixedSize(350, 200)

        ip_label = QLabel('IP', groupbox)
        ip_label.move(15, 20)

        self.ip_input = QLineEdit(groupbox)
        self.ip_input.setFixedWidth(100)
        self.ip_input.setPlaceholderText("127.0.0.1")
        self.ip_input.move(65, 15)

        port_label = QLabel('Port', groupbox)
        port_label.move(15, 40)

        self.port_input = QLineEdit(groupbox)
        self.port_input.setFixedWidth(100)
        self.port_input.setPlaceholderText("502")
        self.port_input.move(65, 35)

        self.mbtn1 = QRadioButton('Master1', groupbox)
        self.mbtn1.move(15, 70)
        self.mbtn1.setChecked(True)

        self.mbtn2 = QRadioButton('Master2', groupbox)
        self.mbtn2.move(100, 70)

        self.serial_label = QLabel('Serial', groupbox)
        self.serial_label.move(180, 70)

        self.sr_input = QComboBox(groupbox)

        self.populate_serial_ports()

        self.sr_input.move(220, 65)
        self.sr_input.setFixedWidth(70)
        self.sr_input.setPlaceholderText("COM_")

        self.br_label = QLabel('BaudRate', groupbox)
        self.br_label.move(15, 90)
        self.dt_label = QLabel('Databit', groupbox)
        self.dt_label.move(15, 110)
        self.st_label = QLabel('Stopbit', groupbox)
        self.st_label.move(15, 130)
        self.pr_label = QLabel('parity', groupbox)
        self.pr_label.move(15, 150)
        self.fc_label = QLabel('Function', groupbox)
        self.fc_label.move(155, 90)
        self.sl_label = QLabel('SlaveID', groupbox)
        self.sl_label.move(155, 110)
        self.ad_label = QLabel('Address', groupbox)
        self.ad_label.move(155, 130)
        self.qt_label = QLabel('Quantity', groupbox)
        self.qt_label.move(155, 150)

        self.br_input = QLineEdit(groupbox)

        self.br_input.move(85, 85)
        self.br_input.setFixedWidth(60)
        self.br_input.setPlaceholderText("115200")

        self.db_input = QLineEdit(groupbox)

        self.db_input.move(85, 105)
        self.db_input.setFixedWidth(60)
        self.db_input.setPlaceholderText("8")

        self.sb_input = QLineEdit(groupbox)

        self.sb_input.move(85, 125)
        self.sb_input.setFixedWidth(60)
        self.sb_input.setPlaceholderText("1")

        self.pr_input = QComboBox(groupbox)

        self.pr_input.move(85, 145)
        self.pr_input.setFixedWidth(60)

        self.pr_input.addItem('None')
        self.pr_input.addItem('Odd')
        self.pr_input.addItem('Even')
        self.pr_input.setPlaceholderText("None")

        self.fc_input = QComboBox(groupbox)

        self.fc_input.addItem('[0x01] Read Coils')
        self.fc_input.addItem('[0x02] Read Discrete Inputs')
        self.fc_input.addItem('[0x03] Read Holding Registers')
        self.fc_input.addItem('[0x04] Read Input Registers')
        self.fc_input.addItem('[0x05] Write Single Coil')
        self.fc_input.addItem('[0x06] Write Single Register')
        self.fc_input.addItem('[0x0f] Write Multiple Coils')
        self.fc_input.addItem('[0x10] Write Multiple Registers')
        self.fc_input.move(215, 85)
        self.fc_input.setFixedWidth(120)  # 가로 크기 지정
        self.fc_input.setPlaceholderText("8")

        self.si_input = QLineEdit(groupbox)

        self.si_input.move(215, 105)
        self.si_input.setFixedWidth(60)  # 가로 크기 지정
        self.si_input.setPlaceholderText("1")

        self.ad_input = QLineEdit(groupbox)

        self.ad_input.move(215, 125)
        self.ad_input.setFixedWidth(60)  # 가로 크기 지정
        self.ad_input.setPlaceholderText("1")

        self.qu_input = QLineEdit(groupbox)

        self.qu_input.move(215, 145)
        self.qu_input.setFixedWidth(60)  # 가로 크기 지정
        self.qu_input.setPlaceholderText("1")

        tcp_ok = QPushButton('OK', groupbox)
        tcp_ok.move(80, 170)
        tcp_ok.clicked.connect(self.connect_to_modbus)  ## OK버튼을 눌렀을때 버튼에 비어있는 내용이 있다면 MESSAGE BOX(INPUT ALL BLANK!) 출력

        tcp_reset = QPushButton('RESET', groupbox)
        tcp_reset.move(160, 170)
        tcp_reset.clicked.connect(self.reset_first_exclusive_group)

        return groupbox

    def reset_first_exclusive_group(self):
        # IP와 Port 입력 필드 초기화
        self.ip_input.clear()
        self.port_input.clear()

        # RadioButton 초기 설정 (Master1 선택)
        self.mbtn1.setChecked(True)
        self.mbtn2.setChecked(False)

        # # Serial 정보 입력 필드 초기화

        self.br_input.clear()
        self.db_input.clear()
        self.sb_input.clear()
        self.pr_input.setCurrentIndex(0)
        self.fc_input.setCurrentIndex(0)
        self.si_input.clear()
        self.ad_input.clear()
        self.qu_input.clear()
        self.timer.stop()

    def populate_serial_ports(self):
        port_info = QSerialPortInfo()
        port_list = port_info.availablePorts()
        for port in port_list:
            self.sr_input.addItem(port.portName())

    def populate_serial_ports1(self):
        port_info2 = QSerialPortInfo()
        port_list2 = port_info2.availablePorts()
        for port in port_list2:
            self.slpr_input.addItem(port.portName())

    def connect_to_modbus(self):



        try:
            ip_address = self.ip_input.text()
            port = int(self.port_input.text())

            self.modbus_client = ModbusTcpClient(ip_address, port=port)
            self.modbus_client.connect()



            function_code = self.fc_input.currentText()
            start_address = int(self.ad_input.text())
            quantity = int(self.qu_input.text())
            slave = int(self.si_input.text())

            if function_code == '[0x01] Read Coils':    # bool 타입으로 바꿔야함.
                result = self.modbus_client.read_coils(start_address, quantity, slave)  # quantity 20으로 고정하자.
                self.log_text.append(f"Read Coils result: {result}")

            elif function_code == '[0x02] Read Discrete Inputs':    # bool 타입으로 바꿔야함.
                result = self.modbus_client.read_discrete_inputs(start_address, quantity, slave)
                self.log_text.append(f"Read Discrete Inputs result: {result}")

            elif function_code == '[0x03] Read Holding Registers':
                result = self.modbus_client.read_holding_registers(start_address, quantity, slave)
                self.log_text.append(f"Read Holding Registers result: {result}")
                print("result", result.registers)
            elif function_code == '[0x04] Read Input Registers':
                self.result = self.modbus_client.read_input_registers(start_address, quantity, slave)

                # time.sleep(0.5)
                self.log_text.append(f"Read Input Registers result: {self.result}")
                # print("TIck\n")
                print("result", self.result.registers)


            elif function_code == '[0x05] Write Single Coil':
                value = int(self.qu_input.text())  # bool 타입으로 바꿔야함.
                result = self.modbus_client.write_coil(start_address, value)
                self.log_text.append(f"Write Single Coil result: {result}")

            elif function_code == '[0x06] Write Single Register':
                value = int(self.qu_input.text())
                result = self.modbus_client.write_register(start_address, value, slave)
                self.log_text.append(f"Write Single Register result: {result}")

            elif function_code == '[0x0f] Write Multiple Coils':    # bool 타입으로 바꿔야함.
                values = [int(value) for value in self.qu_input.text().split(',')]
                result = self.modbus_client.write_coils(start_address, values)
                self.log_text.append(f"Write Multiple Coils result: {result}")

            elif function_code == '[0x10] Write Multiple Registers':
                values = [int(value) for value in self.qu_input.text().split(',')]
                result = self.modbus_client.write_registers(start_address, values, slave)  # quantity의 값들을 넣는방법 생각해보기
                self.log_text.append(f"Write Multiple Registers result: {result}")




            self.timer.start(3000)
            self.plsa_input0.setText(str(self.result.registers[0]))
            self.plsa_input1.setText(str(self.result.registers[1]))
            self.plsa_input2.setText(str(self.result.registers[2]))
            self.plsa_input3.setText(str(self.result.registers[3]))
            self.plsa_input4.setText(str(self.result.registers[4]))
            self.plsa_input5.setText(str(self.result.registers[5]))
            self.plsa_input6.setText(str(self.result.registers[6]))
            self.plsa_input7.setText(str(self.result.registers[7]))
            self.plsa_input8.setText(str(self.result.registers[8]))
            self.plsa_input9.setText(str(self.result.registers[9]))
            self.plsa_input10.setText(str(self.result.registers[10]))
            self.plsa_input11.setText(str(self.result.registers[11]))
            self.plsa_input12.setText(str(self.result.registers[12]))
            self.plsa_input13.setText(str(self.result.registers[13]))
            self.plsa_input14.setText(str(self.result.registers[14]))
            self.plsa_input15.setText(str(self.result.registers[15]))
            self.plsa_input16.setText(str(self.result.registers[16]))
            self.plsa_input17.setText(str(self.result.registers[17]))
            self.plsa_input18.setText(str(self.result.registers[18]))
            self.plsa_input19.setText(str(self.result.registers[19]))

        except Exception as e:

            self.log_text_tcp.append(f"Connection error: {str(e)}")

            self.log_text_tcp.setPlainText("Connection FAIL!")

        try:
            start_address1 = int(self.ad_input.text())

            for i1 in range(0, 20):
                plsl_label = getattr(self, f'plsl_label{i1}')
                new_address1 = start_address1 + i1

                plsl_label.setText(f'Address{new_address1}')


        except ValueError:
            self.log_text_m1.setPlainText("Please enter a valid starting address.")
            # QMessageBox.warning(self, "Invalid Input", "Please enter a valid starting address.")
            ## 이거를 message가 다 입력안되어있을때로 수정하기

    def createMasterGroup(self):
        groupbox = QGroupBox('Master1')

        self.log_text_m1 = QTextEdit()
        self.log_text_m1.setReadOnly(True)
        self.log_text_m1.setPlainText("Connection OK! or Connection FAIL!")

        clear_button = QPushButton('Clear Log')
        clear_button.clicked.connect(lambda: self.log_text_m1.clear())

        vbox = QVBoxLayout()
        vbox.addWidget(self.log_text_m1)
        vbox.addWidget(clear_button)
        groupbox.setLayout(vbox)

        groupbox.setFixedSize(350, 200)

        return groupbox

    def createMaster2Group(self):
        groupbox = QGroupBox('Master2')

        self.log_text_m2 = QTextEdit()
        self.log_text_m2.setReadOnly(True)
        self.log_text_m2.setPlainText("Connection OK! or Connection FAIL!")

        clear_button = QPushButton('Clear Log')
        clear_button.clicked.connect(lambda: self.log_text_m2.clear())

        vbox = QVBoxLayout()
        vbox.addWidget(self.log_text_m2)
        vbox.addWidget(clear_button)
        groupbox.setLayout(vbox)

        groupbox.setFixedSize(350, 200)

        return groupbox

    def createTcpGroup(self):
        groupbox = QGroupBox('TCP MODE')

        groupbox.setFixedSize(350, 200)
        self.log_text_tcp = QTextEdit()
        self.log_text_tcp.setReadOnly(True)
        self.log_text_tcp.setPlainText("Connection OK! or Connection FAIL!")

        clear_button = QPushButton('Clear Log')
        clear_button.clicked.connect(lambda: self.log_text_tcp.clear())

        vbox = QVBoxLayout()
        vbox.addWidget(self.log_text_tcp)
        vbox.addWidget(clear_button)
        groupbox.setLayout(vbox)

        return groupbox

    def createModBusPollGroup(self):
        groupbox = QGroupBox('ModBus Poll Group')

        groupbox.setFixedSize(700, 200)

        self.plsl_label0 = QLabel('Address10000', groupbox)
        self.plsl_label0.move(15, 25)

        self.plsa_input0 = QLineEdit(groupbox)  # register값이되야한다? 0~65535값

        self.plsa_input0.move(105, 20)
        self.plsa_input0.setFixedWidth(60)

        self.plsl_label1 = QLabel('Address10001', groupbox)
        self.plsl_label1.move(15, 45)

        self.plsa_input1 = QLineEdit(groupbox)

        self.plsa_input1.move(105, 40)
        self.plsa_input1.setFixedWidth(60)

        self.plsl_label2 = QLabel('Address10002', groupbox)
        self.plsl_label2.move(15, 65)

        self.plsa_input2 = QLineEdit(groupbox)

        self.plsa_input2.move(105, 60)
        self.plsa_input2.setFixedWidth(60)

        self.plsl_label3 = QLabel('Address10003', groupbox)
        self.plsl_label3.move(15, 85)

        self.plsa_input3 = QLineEdit(groupbox)

        self.plsa_input3.move(105, 80)
        self.plsa_input3.setFixedWidth(60)

        self.plsl_label4 = QLabel('Address10004', groupbox)
        self.plsl_label4.move(15, 105)

        self.plsa_input4 = QLineEdit(groupbox)

        self.plsa_input4.move(105, 100)
        self.plsa_input4.setFixedWidth(60)

        self.plsl_label5 = QLabel('Address10005', groupbox)
        self.plsl_label5.move(185, 25)

        self.plsa_input5 = QLineEdit(groupbox)

        self.plsa_input5.move(275, 20)
        self.plsa_input5.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label6 = QLabel('Address10006', groupbox)
        self.plsl_label6.move(185, 45)

        self.plsa_input6 = QLineEdit(groupbox)

        self.plsa_input6.move(275, 40)
        self.plsa_input6.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label7 = QLabel('Address10007', groupbox)
        self.plsl_label7.move(185, 65)

        self.plsa_input7 = QLineEdit(groupbox)

        self.plsa_input7.move(275, 60)
        self.plsa_input7.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label8 = QLabel('Address10008', groupbox)
        self.plsl_label8.move(185, 85)

        self.plsa_input8 = QLineEdit(groupbox)

        self.plsa_input8.move(275, 80)
        self.plsa_input8.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label9 = QLabel('Address10009', groupbox)
        self.plsl_label9.move(185, 105)

        self.plsa_input9 = QLineEdit(groupbox)

        self.plsa_input9.move(275, 100)
        self.plsa_input9.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label10 = QLabel('Address10010', groupbox)
        self.plsl_label10.move(355, 25)

        self.plsa_input10 = QLineEdit(groupbox)

        self.plsa_input10.move(445, 20)
        self.plsa_input10.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label11 = QLabel('Address10011', groupbox)
        self.plsl_label11.move(355, 45)

        self.plsa_input11 = QLineEdit(groupbox)

        self.plsa_input11.move(445, 40)
        self.plsa_input11.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label12 = QLabel('Address10012', groupbox)
        self.plsl_label12.move(355, 65)

        self.plsa_input12 = QLineEdit(groupbox)

        self.plsa_input12.move(445, 60)
        self.plsa_input12.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label13 = QLabel('Address10013', groupbox)
        self.plsl_label13.move(355, 85)

        self.plsa_input13 = QLineEdit(groupbox)

        self.plsa_input13.move(445, 80)
        self.plsa_input13.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label14 = QLabel('Address10014', groupbox)
        self.plsl_label14.move(355, 105)

        self.plsa_input14 = QLineEdit(groupbox)

        self.plsa_input14.move(445, 100)
        self.plsa_input14.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label15 = QLabel('Address10015', groupbox)
        self.plsl_label15.move(525, 25)

        self.plsa_input15 = QLineEdit(groupbox)

        self.plsa_input15.move(615, 20)
        self.plsa_input15.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label16 = QLabel('Address10016', groupbox)
        self.plsl_label16.move(525, 45)

        self.plsa_input16 = QLineEdit(groupbox)

        self.plsa_input16.move(615, 40)
        self.plsa_input16.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label17 = QLabel('Address10017', groupbox)
        self.plsl_label17.move(525, 65)

        self.plsa_input17 = QLineEdit(groupbox)

        self.plsa_input17.move(615, 60)
        self.plsa_input17.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label18 = QLabel('Address10018', groupbox)
        self.plsl_label18.move(525, 85)

        self.plsa_input18 = QLineEdit(groupbox)

        self.plsa_input18.move(615, 80)
        self.plsa_input18.setFixedWidth(60)  # 가로 크기 지정

        self.plsl_label19 = QLabel('Address10019', groupbox)
        self.plsl_label19.move(525, 105)

        self.plsa_input19 = QLineEdit(groupbox)

        self.plsa_input19.move(615, 100)
        self.plsa_input19.setFixedWidth(60)  # 가로 크기 지정

        for i in range(20):
            plsa_input = getattr(self, f'plsa_input{i}')
            plsa_input.installEventFilter(self)

        return groupbox

    # def eventFilter(self, obj, event):
    #     if event.type() == QEvent.FocusOut and isinstance(obj, QLineEdit):
    #         self.validateAndUpdateLineEdit(obj)
    #     return super().eventFilter(obj, event)
    #
    # def validateAndUpdateLineEdit(self, line_edit):
    #     try:
    #         value = int(line_edit.text())
    #         if 0 <= value <= 65535:
    #             # Valid value, do nothing
    #             pass
    #         else:
    #             # Invalid value, set to 0
    #             line_edit.setText("0")
    #     except ValueError:
    #         # Non-integer value, set to 0
    #         line_edit.setText("0")

    def createModBusSlaveGroup(self):
        groupbox = QGroupBox('ModBus Slave Group')
        groupbox.setFixedSize(700, 200)

        self.slsl_label = QLabel('SlaveID', groupbox)
        self.slsl_label.move(15, 25)

        self.slsl_input = QLineEdit(groupbox)

        self.slsl_input.move(65, 20)
        self.slsl_input.setFixedWidth(60)  # 가로 크기 지정
        self.slsl_input.setPlaceholderText("1")

        self.slad_label = QLabel('address', groupbox)
        self.slad_label.move(135, 25)

        self.slad_input = QLineEdit(groupbox)

        self.slad_input.move(185, 20)
        self.slad_input.setFixedWidth(60)  # 가로 크기 지정
        self.slad_input.setPlaceholderText("1")

        self.slpr_label = QLabel('PORT', groupbox)
        self.slpr_label.move(255, 25)

        self.slpr_input = QComboBox(groupbox)
        self.slpr_input.move(295, 20)
        self.slpr_input.setFixedWidth(70)  # 가로 크기 지정
        self.slpr_input.setPlaceholderText("COM_")

        self.populate_serial_ports1()

        self.slbr_label = QLabel('BAUD', groupbox)
        self.slbr_label.move(370, 25)

        self.slbr_input = QLineEdit(groupbox)

        self.slbr_input.move(405, 20)
        self.slbr_input.setFixedWidth(60)
        self.slbr_input.setPlaceholderText("115200")

        self.sldt_label = QLabel('DATA', groupbox)
        self.sldt_label.move(475, 25)

        self.sldt_input = QLineEdit(groupbox)

        self.sldt_input.move(515, 20)
        self.sldt_input.setFixedWidth(60)
        self.sldt_input.setPlaceholderText("1")

        self.slst_label = QLabel('STOP', groupbox)
        self.slst_label.move(15, 45)

        self.slst_input = QLineEdit(groupbox)

        self.slst_input.move(65, 40)
        self.slst_input.setFixedWidth(60)
        self.slst_input.setPlaceholderText("1")

        self.slpr_label = QLabel('PARITY', groupbox)
        self.slpr_label.move(135, 45)

        self.slpr_input = QComboBox(groupbox)

        self.slpr_input.move(185, 40)
        self.slpr_input.setFixedWidth(60)

        self.slpr_input.addItem('None')
        self.slpr_input.addItem('Odd')
        self.slpr_input.addItem('Even')
        self.slpr_input.setPlaceholderText("None")

        sbtn1 = QRadioButton('Integer', groupbox)
        sbtn1.move(265, 45)
        sbtn1.setChecked(True)

        sbtn2 = QRadioButton('Binary', groupbox)
        sbtn2.move(330, 45)

        slapl_bt = QPushButton('APPLY', groupbox)
        slapl_bt.move(430, 40)
        slapl_bt.clicked.connect(self.update_addresses)

        # reset버튼이 눌리면 모든값들 초기화하기
        slrs_bt = QPushButton('RESET', groupbox)
        slrs_bt.move(510, 40)
        slrs_bt.clicked.connect(self.reset_createModBusSlaveGroup)

        self.slad_label0 = QLabel('Address10000', groupbox)
        self.slad_label0.move(15, 75)

        self.slad_input0 = QLineEdit(groupbox)

        self.slad_input0.move(105, 70)
        self.slad_input0.setFixedWidth(60)

        self.slad_label1 = QLabel('Address10001', groupbox)
        self.slad_label1.move(15, 95)

        self.slad_input1 = QLineEdit(groupbox)

        self.slad_input1.move(105, 90)
        self.slad_input1.setFixedWidth(60)

        self.slad_label2 = QLabel('Address10002', groupbox)
        self.slad_label2.move(15, 115)

        self.slad_input2 = QLineEdit(groupbox)

        self.slad_input2.move(105, 110)
        self.slad_input2.setFixedWidth(60)

        self.slad_label3 = QLabel('Address10003', groupbox)
        self.slad_label3.move(15, 135)

        self.slad_input3 = QLineEdit(groupbox)

        self.slad_input3.move(105, 130)
        self.slad_input3.setFixedWidth(60)

        self.slad_label4 = QLabel('Address10004', groupbox)
        self.slad_label4.move(15, 155)

        self.slad_input4 = QLineEdit(groupbox)

        self.slad_input4.move(105, 150)
        self.slad_input4.setFixedWidth(60)

        self.slad_label5 = QLabel('Address10005', groupbox)
        self.slad_label5.move(185, 75)

        self.slad_input5 = QLineEdit(groupbox)

        self.slad_input5.move(275, 70)
        self.slad_input5.setFixedWidth(60)

        self.slad_label6 = QLabel('Address10006', groupbox)
        self.slad_label6.move(185, 95)

        self.slad_input6 = QLineEdit(groupbox)

        self.slad_input6.move(275, 90)
        self.slad_input6.setFixedWidth(60)

        self.slad_label7 = QLabel('Address10007', groupbox)
        self.slad_label7.move(185, 115)

        self.slad_input7 = QLineEdit(groupbox)

        self.slad_input7.move(275, 110)
        self.slad_input7.setFixedWidth(60)

        self.slad_label8 = QLabel('Address10008', groupbox)
        self.slad_label8.move(185, 135)

        self.slad_input8 = QLineEdit(groupbox)

        self.slad_input8.move(275, 130)
        self.slad_input8.setFixedWidth(60)

        self.slad_label9 = QLabel('Address10009', groupbox)
        self.slad_label9.move(185, 155)

        self.slad_input9 = QLineEdit(groupbox)

        self.slad_input9.move(275, 150)
        self.slad_input9.setFixedWidth(60)

        self.slad_label10 = QLabel('Address10010', groupbox)
        self.slad_label10.move(355, 75)

        self.slad_input10 = QLineEdit(groupbox)

        self.slad_input10.move(445, 70)
        self.slad_input10.setFixedWidth(60)

        self.slad_label11 = QLabel('Address10011', groupbox)
        self.slad_label11.move(355, 95)

        self.slad_input11 = QLineEdit(groupbox)

        self.slad_input11.move(445, 90)
        self.slad_input11.setFixedWidth(60)

        self.slad_label12 = QLabel('Address10012', groupbox)
        self.slad_label12.move(355, 115)

        self.slad_input12 = QLineEdit(groupbox)

        self.slad_input12.move(445, 110)
        self.slad_input12.setFixedWidth(60)

        self.slad_label13 = QLabel('Address10013', groupbox)
        self.slad_label13.move(355, 135)

        self.slad_input13 = QLineEdit(groupbox)

        self.slad_input13.move(445, 130)
        self.slad_input13.setFixedWidth(60)

        self.slad_label14 = QLabel('Address10014', groupbox)
        self.slad_label14.move(355, 155)

        self.slad_input14 = QLineEdit(groupbox)

        self.slad_input14.move(445, 150)
        self.slad_input14.setFixedWidth(60)

        self.slad_label15 = QLabel('Address10015', groupbox)
        self.slad_label15.move(525, 75)

        self.slad_input15 = QLineEdit(groupbox)

        self.slad_input15.move(615, 70)
        self.slad_input15.setFixedWidth(60)

        self.slad_label16 = QLabel('Address10016', groupbox)
        self.slad_label16.move(525, 95)

        self.slad_input16 = QLineEdit(groupbox)

        self.slad_input16.move(615, 90)
        self.slad_input16.setFixedWidth(60)

        self.slad_label17 = QLabel('Address10017', groupbox)
        self.slad_label17.move(525, 115)

        self.slad_input17 = QLineEdit(groupbox)

        self.slad_input17.move(615, 110)
        self.slad_input17.setFixedWidth(60)

        self.slad_label18 = QLabel('Address10018', groupbox)
        self.slad_label18.move(525, 135)

        self.slad_input18 = QLineEdit(groupbox)

        self.slad_input18.move(615, 130)
        self.slad_input18.setFixedWidth(60)

        self.slad_label19 = QLabel('Address10019', groupbox)
        self.slad_label19.move(525, 155)

        self.slad_input19 = QLineEdit(groupbox)

        self.slad_input19.move(615, 150)
        self.slad_input19.setFixedWidth(60)

        return groupbox

    def update_addresses(self):
        context = 
        ip_address = self.ip_input.text()
        port = int(self.port_input.text())

        self.modbus_server = ModbusTcpServer(address=("127.0.0.1", 502))
        # ModBus Serial 통신부분.
        self.modbus_server_RTU = ModbusSerialClient(ip_address, port= port)
        self.modbus_server_RTU.connect()


        start_address = int(self.slad_input.text())
        print("start_address", start_address)
        print("")
        for i in range(0, 20):
            slad_label = getattr(self, f'slad_label{i}')
            new_address = start_address + i
            print("new_address", new_address)
            slad_label.setText(f'Address{new_address}')

    def reset_createModBusSlaveGroup(self):
        # Clear all the input fields
        for i in range(0, 20):
            slad_input = getattr(self, f'slad_input{i}')
            slad_input.clear()
            slad_label = getattr(self, f'slad_label{i}')
            slad_label.setText('Address')

    def createLogGroup(self):
        groupbox = QGroupBox('Log')
        groupbox.setFixedSize(1400, 200)

        self.log_text = QTextEdit()  # log_text를 클래스의 멤버 변수로 만듭니다.
        self.log_text.setReadOnly(True)
        self.log_text.setPlainText("This is a log text...")

        clear_button = QPushButton('Clear Log')
        clear_button.clicked.connect(lambda: self.log_text.clear())  # 클릭 시 log_text를 지우는 동작 연결

        vbox = QVBoxLayout()
        vbox.addWidget(self.log_text)
        vbox.addWidget(clear_button)  # "Clear Log" 버튼 추가
        groupbox.setLayout(vbox)

        return groupbox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())  # GUI 메인 루프 시작 및 종료되지 않음