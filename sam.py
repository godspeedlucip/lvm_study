# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sam.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from utils import ImageLabel
import os

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1018, 717)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.ip_LineEdit = QtWidgets.QLineEdit(Form)
        self.ip_LineEdit.setText("")
        self.ip_LineEdit.setObjectName("ip_LineEdit")
        self.horizontalLayout_3.addWidget(self.ip_LineEdit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.port_LineEdit = QtWidgets.QLineEdit(Form)
        self.port_LineEdit.setText("")
        self.port_LineEdit.setObjectName("port_LineEdit")
        self.horizontalLayout_3.addWidget(self.port_LineEdit)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.link_btn = QtWidgets.QPushButton(Form)
        self.link_btn.setObjectName("link_btn")
        self.horizontalLayout_3.addWidget(self.link_btn)
        self.save_config_btn = QtWidgets.QPushButton(Form)
        self.save_config_btn.setObjectName("save_config_btn")
        self.horizontalLayout_3.addWidget(self.save_config_btn)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.horizontalLayout_3.setStretch(2, 1)
        self.horizontalLayout_3.setStretch(3, 3)
        self.horizontalLayout_3.setStretch(4, 1)
        self.horizontalLayout_3.setStretch(5, 1)
        self.horizontalLayout_3.setStretch(6, 1)
        self.horizontalLayout_3.setStretch(7, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.server = QtWidgets.QWidget()
        self.server.setObjectName("server")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.server)
        self.verticalLayout.setObjectName("verticalLayout")
        self.path_hori_layout = QtWidgets.QHBoxLayout()
        self.path_hori_layout.setObjectName("path_hori_layout")
        self.vol_label = QtWidgets.QLabel(self.server)
        self.vol_label.setObjectName("vol_label")
        self.path_hori_layout.addWidget(self.vol_label)
        self.vol_LEdit = QtWidgets.QLineEdit(self.server)
        self.vol_LEdit.setObjectName("vol_LEdit")
        self.path_hori_layout.addWidget(self.vol_LEdit)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.path_hori_layout.addItem(spacerItem4)
        self.mask_label = QtWidgets.QLabel(self.server)
        self.mask_label.setObjectName("mask_label")
        self.path_hori_layout.addWidget(self.mask_label)
        self.maskPath_LEdit = QtWidgets.QLineEdit(self.server)
        self.maskPath_LEdit.setObjectName("maskPath_LEdit")
        self.path_hori_layout.addWidget(self.maskPath_LEdit)
        self.select_mask_store_path_btn = QtWidgets.QPushButton(self.server)
        self.select_mask_store_path_btn.setObjectName("select_mask_store_path_btn")
        self.path_hori_layout.addWidget(self.select_mask_store_path_btn)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.path_hori_layout.addItem(spacerItem5)
        self.input_yes_btn = QtWidgets.QPushButton(self.server)
        self.input_yes_btn.setObjectName("input_yes_btn")
        self.path_hori_layout.addWidget(self.input_yes_btn)
        self.input_change_btn = QtWidgets.QPushButton(self.server)
        self.input_change_btn.setObjectName("input_change_btn")
        self.path_hori_layout.addWidget(self.input_change_btn)
        self.path_hori_layout.setStretch(0, 1)
        self.path_hori_layout.setStretch(1, 3)
        self.path_hori_layout.setStretch(2, 1)
        self.path_hori_layout.setStretch(3, 1)
        self.path_hori_layout.setStretch(4, 3)
        self.path_hori_layout.setStretch(5, 1)
        self.path_hori_layout.setStretch(6, 1)
        self.path_hori_layout.setStretch(7, 1)
        self.path_hori_layout.setStretch(8, 1)
        self.verticalLayout.addLayout(self.path_hori_layout)
        self.main_hori_layout = QtWidgets.QHBoxLayout()
        self.main_hori_layout.setObjectName("main_hori_layout")
        self.slice_ListW = QtWidgets.QListWidget(self.server)
        self.slice_ListW.setObjectName("slice_ListW")
        self.main_hori_layout.addWidget(self.slice_ListW)
        self.image_show_label = ImageLabel(self.server) #zheli
        self.image_show_label.setMinimumSize(QtCore.QSize(100, 100))
        self.image_show_label.setObjectName("image_show_label")
        # self.image_show_label = QtWidgets.QLabel(self.server)
        # self.image_show_label.setMinimumSize(QtCore.QSize(100, 100))
        # self.image_show_label.setText("")
        # self.image_show_label.setObjectName("image_show_label")
        self.main_hori_layout.addWidget(self.image_show_label)
        self.btn_verti_layout = QtWidgets.QVBoxLayout()
        self.btn_verti_layout.setObjectName("btn_verti_layout")
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.btn_verti_layout.addItem(spacerItem6)
        self.detect_btn = QtWidgets.QPushButton(self.server)
        self.detect_btn.setObjectName("detect_btn")
        self.btn_verti_layout.addWidget(self.detect_btn)
        self.reset_btn = QtWidgets.QPushButton(self.server)
        self.reset_btn.setObjectName("reset_btn")
        self.btn_verti_layout.addWidget(self.reset_btn)
        self.undo_btn = QtWidgets.QPushButton(self.server)
        self.undo_btn.setObjectName("undo_btn")
        self.btn_verti_layout.addWidget(self.undo_btn)
        self.remask_btn = QtWidgets.QPushButton(self.server)
        self.remask_btn.setObjectName("remask_btn")
        self.btn_verti_layout.addWidget(self.remask_btn)
        self.confirm_btn = QtWidgets.QPushButton(self.server)
        self.confirm_btn.setObjectName("confirm_btn")
        self.btn_verti_layout.addWidget(self.confirm_btn)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.previousImage_btn = QtWidgets.QPushButton(self.server)
        self.previousImage_btn.setObjectName("previousImage_btn")
        self.horizontalLayout_2.addWidget(self.previousImage_btn)
        self.nextImage_btn = QtWidgets.QPushButton(self.server)
        self.nextImage_btn.setObjectName("nextImage_btn")
        self.horizontalLayout_2.addWidget(self.nextImage_btn)
        self.btn_verti_layout.addLayout(self.horizontalLayout_2)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.btn_verti_layout.addItem(spacerItem7)
        self.main_hori_layout.addLayout(self.btn_verti_layout)
        self.main_hori_layout.setStretch(1, 8)
        self.main_hori_layout.setStretch(2, 1)
        self.verticalLayout.addLayout(self.main_hori_layout)
        self.tabWidget.addTab(self.server, "")
        self.local = QtWidgets.QWidget()
        self.local.setObjectName("local")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.local)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.local_img_show_label = QtWidgets.QLabel(self.local)
        self.local_img_show_label.setObjectName("local_img_show_label")
        self.horizontalLayout.addWidget(self.local_img_show_label)
        self.btn_verti_layout_2 = QtWidgets.QVBoxLayout()
        self.btn_verti_layout_2.setObjectName("btn_verti_layout_2")
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.btn_verti_layout_2.addItem(spacerItem8)
        self.choose_file_btn = QtWidgets.QPushButton(self.local)
        self.choose_file_btn.setObjectName("choose_file_btn")
        self.btn_verti_layout_2.addWidget(self.choose_file_btn)
        self.local_detect_btn = QtWidgets.QPushButton(self.local)
        self.local_detect_btn.setObjectName("local_detect_btn")
        self.btn_verti_layout_2.addWidget(self.local_detect_btn)
        self.local_reset_btn = QtWidgets.QPushButton(self.local)
        self.local_reset_btn.setObjectName("local_reset_btn")
        self.btn_verti_layout_2.addWidget(self.local_reset_btn)
        self.local_undo_btn = QtWidgets.QPushButton(self.local)
        self.local_undo_btn.setObjectName("local_undo_btn")
        self.btn_verti_layout_2.addWidget(self.local_undo_btn)
        self.local_confirm_btn = QtWidgets.QPushButton(self.local)
        self.local_confirm_btn.setObjectName("local_confirm_btn")
        self.btn_verti_layout_2.addWidget(self.local_confirm_btn)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_verti_layout_2.addLayout(self.horizontalLayout_4)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.btn_verti_layout_2.addItem(spacerItem9)
        self.horizontalLayout.addLayout(self.btn_verti_layout_2)
        self.horizontalLayout.setStretch(0, 8)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout_5.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.local, "")
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ip_LineEdit.setPlaceholderText(_translate("Form", "输入IP地址"))
        self.port_LineEdit.setPlaceholderText(_translate("Form", "输入端口号"))
        self.link_btn.setToolTip(_translate("Form", "<html><head/><body><p>输入IP和端口连接服务器</p></body></html>"))
        self.link_btn.setText(_translate("Form", "connect"))
        self.save_config_btn.setToolTip(_translate("Form", "<html><head/><body><p>将当前输入的IP和端口保存，下一次无需继续输入</p></body></html>"))
        self.save_config_btn.setText(_translate("Form", "save"))
        self.vol_label.setText(_translate("Form", "文件路径"))
        self.vol_LEdit.setToolTip(_translate("Form", "<html><head/><body><p>想检测mask的文件夹或文件的路径</p></body></html>"))
        self.vol_LEdit.setText(_translate("Form", ""))
        self.mask_label.setText(_translate("Form", "mask存储路径"))
        self.maskPath_LEdit.setToolTip(_translate("Form", "<html><head/><body><p>存放检测得到的mask的路径</p></body></html>"))
        self.maskPath_LEdit.setText(_translate("Form", os.path.dirname(os.path.abspath(__file__))))
        self.select_mask_store_path_btn.setToolTip(_translate("Form", "<html><head/><body><p>选择mask的存储路径</p></body></html>"))
        self.select_mask_store_path_btn.setText(_translate("Form", "select"))
        self.input_yes_btn.setToolTip(_translate("Form", "<html><head/><body><p>确认输入的路径，并获取服务器返回的图片</p></body></html>"))
        self.input_yes_btn.setText(_translate("Form", "yes"))
        self.input_change_btn.setToolTip(_translate("Form", "<html><head/><body><p>改变文件路径和mask存储路路径</p></body></html>"))
        self.input_change_btn.setText(_translate("Form", "change"))
        self.slice_ListW.setToolTip(_translate("Form", "<html><head/><body><p>列出二维切片</p></body></html>"))
        self.image_show_label.setToolTip(_translate("Form", "<html><head/><body><p>显示当前的图片</p></body></html>"))
        self.detect_btn.setToolTip(_translate("Form", "<html><head/><body><p>检测当前图片得到mask</p></body></html>"))
        self.detect_btn.setText(_translate("Form", "detect"))
        self.reset_btn.setToolTip(_translate("Form", "<html><head/><body><p>重置当前图像的prompt和mask</p></body></html>"))
        self.reset_btn.setText(_translate("Form", "reset"))
        self.undo_btn.setToolTip(_translate("Form", "<html><head/><body><p>撤销刚才打入的点</p></body></html>"))
        self.undo_btn.setText(_translate("Form", "undo"))
        self.remask_btn.setToolTip(_translate("Form", "<html><head/><body><p>删除这个mask</p></body></html>"))
        self.remask_btn.setText(_translate("Form", "remask"))
        self.confirm_btn.setToolTip(_translate("Form", "<html><head/><body><p>保存当前的mask</p></body></html>"))
        self.confirm_btn.setText(_translate("Form", "confirm"))
        self.previousImage_btn.setToolTip(_translate("Form", "<html><head/><body><p>切换到上一张图片</p></body></html>"))
        self.previousImage_btn.setText(_translate("Form", "prev"))
        self.nextImage_btn.setToolTip(_translate("Form", "<html><head/><body><p>切换到下一张图片</p></body></html>"))
        self.nextImage_btn.setText(_translate("Form", "next"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.server), _translate("Form", "服务器选择"))
        self.local_img_show_label.setToolTip(_translate("Form", "<html><head/><body><p>显示当前的图片</p></body></html>"))
        self.local_img_show_label.setText(_translate("Form", "显示图片的地方"))
        self.choose_file_btn.setToolTip(_translate("Form", "<html><head/><body><p>选择本地文件并上传到服务器</p></body></html>"))
        self.choose_file_btn.setText(_translate("Form", "choose_file"))
        self.local_detect_btn.setToolTip(_translate("Form", "<html><head/><body><p>检测当前图片得到mask</p></body></html>"))
        self.local_detect_btn.setText(_translate("Form", "detect"))
        self.local_reset_btn.setToolTip(_translate("Form", "<html><head/><body><p>重置当前图像的prompt和mask</p></body></html>"))
        self.local_reset_btn.setText(_translate("Form", "reset"))
        self.local_undo_btn.setToolTip(_translate("Form", "<html><head/><body><p>撤销刚才打入的点</p></body></html>"))
        self.local_undo_btn.setText(_translate("Form", "undo"))
        self.local_confirm_btn.setToolTip(_translate("Form", "<html><head/><body><p>保存当前的mask</p></body></html>"))
        self.local_confirm_btn.setText(_translate("Form", "confirm"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.local), _translate("Form", "本地上传"))