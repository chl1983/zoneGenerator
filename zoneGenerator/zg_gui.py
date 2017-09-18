#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from zoneGenerator import zoneGenerator
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,QGridLayout, QApplication,QPushButton,
                             QInputDialog,QFileDialog,QFrame)

class GZQT(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.conf_file_pathLabel = QLabel('Please input the configuration file name or path:', self)
        self.command_file_pathLabel = QLabel('Please input the command file name or path:', self)
        self.switch_typeLabel = QLabel("Please select the switch type:", self)
        self.VsanIDLabel = QLabel("If it is a Cisco switch,please input the VSAN ID:")
        self.cfgnameLabel = QLabel("Please input the cfg or zoneset name:")

        self.conf_file_pathEdit = QLineEdit()
        self.command_file_pathEdit = QLineEdit()
        self.switch_type_defaultLabel = QLabel("...")
        self.switch_type_defaultLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.VsanIDEdit = QLineEdit()
        self.cfgnameEdit = QLineEdit()

        self.conf_file_pathbtn = QPushButton("...")
        self.conf_file_pathbtn.clicked.connect(lambda: self.select_conf_file_path(self.conf_file_pathEdit.text()))
        self.switch_typebtn = QPushButton("...")
        self.switch_typebtn.clicked.connect(self.get_switch_str)

        self.Generatebtn = QPushButton("Generate", self)
        self.Generatebtn.clicked.connect(self.generate)
        self.Cancelbtn = QPushButton("Cancel", self)
        self.Cancelbtn.clicked.connect(QCoreApplication.instance().quit)

        grid = QGridLayout()

        grid.addWidget(self.conf_file_pathLabel, 1, 1)
        grid.addWidget(self.command_file_pathLabel, 2, 1)
        grid.addWidget(self.switch_typeLabel, 3, 1)
        grid.addWidget(self.VsanIDLabel, 4 ,1)
        grid.addWidget(self.cfgnameLabel, 5, 1)



        grid.addWidget(self.conf_file_pathEdit, 1, 2)
        grid.addWidget(self.command_file_pathEdit, 2, 2)
        grid.addWidget(self.switch_type_defaultLabel, 3, 2)
        grid.addWidget(self.conf_file_pathbtn, 1, 3)
        grid.addWidget(self.switch_typebtn, 3, 3)
        grid.addWidget(self.VsanIDEdit, 4, 2)
        grid.addWidget(self.cfgnameEdit, 5, 2)

        grid.addWidget(self.Cancelbtn, 6, 3)
        grid.addWidget(self.Generatebtn, 6, 1)

        self.setLayout(grid)

        self.setWindowTitle('zoneGenerator@Kevin.Chen')
        self.show()


    def select_conf_file_path(self,conf_file_path):
        if os.path.exists(conf_file_path):
            path = QFileDialog.getOpenFileName(self, "Please select the configuration file:", conf_file_path, "Text file(*.txt)")

        else:
            path = QFileDialog.getOpenFileName(self, "Please select the configuration file:", sys.argv[0], "Text file(*.txt)")

        self.conf_file_pathEdit.setText(str(path[0]))


    def select_command_path(self):
         command_file_path, ok = QInputDialog.getText(self, "Command File", "Please input the command file:", QLineEdit.Normal, self.command_file_pathEdit.text())
         if ok and (len(command_file_path)!=0):
             self.command_file_pathEdit.setText(command_file_path)

    def get_switch_str(self):
        switch_type_list = ["1:Brocade", "2:Cisco"]
        switch_type_str, ok = QInputDialog.getItem(self, "switch type", "Please select switch type:", switch_type_list)
        if ok:
            self.switch_type_defaultLabel.setText(switch_type_str)

    def generate(self):
        conf_file = str(self.conf_file_pathEdit.text())
        command_file = str(self.command_file_pathEdit.text())
        switch_type = str(self.switch_type_defaultLabel.text()[0])
        VsanID = str(self.VsanIDEdit.text())
        cfgname = str(self.cfgnameEdit.text())
        zg = zoneGenerator(switch_type, conf_file, command_file, VsanID, cfgname)
        zg.generate_cmd()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GZ = GZQT()
    sys.exit(app.exec_())