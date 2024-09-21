import sys
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QUrl, QThread, QEvent, QProcess, pyqtSlot, QSize, QPoint
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QOpenGLWidget, QLabel, QProgressDialog, QTabBar, \
    QListWidget, QMenu
from PyQt5.QtGui import QIcon, QTextCursor, QPixmap, QImage, QFont, QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5 import uic
import os,re,shutil
from pyqt5_plugins.examplebutton import QtWidgets
import numpy as np
import tifffile as tiff
import configparser
import cc3d
from scipy import ndimage

from utils import SocketClient,ImageShow,ImageLabel #导入客户端代码
from sam import Ui_Form

class page(QWidget,Ui_Form):

    def __init__(self):
        # 初始化
        super(page, self).__init__()  # 这个是必须调用的，否则会运行不成功
        # self.ui = uic.loadUi('sam.ui')  # 加载designer设计的ui程序
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # self.ui.setWindowTitle('segment') #设置窗口标题
        # self.ui.setWindowIcon(QIcon('./image/seu-logo.png')) #设置窗口图标
        # self.ui.showMaximized()
        self.setWindowTitle('segment') #设置窗口标题
        self.setWindowIcon(QIcon('./image/seu-logo.png')) #设置窗口图标
        self.showMaximized()
        self.global_connected = False #标记是否完成连接

        self.set_font()
        self.signal_bind()
        self.setup()

    def setup(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        if not config.sections():
            return
        ip = config['Server']['ip_address']
        port = config['Server']['port']
        self.ui.ip_LineEdit.setText(ip)
        self.ui.port_LineEdit.setText(port)
        self.ui.input_change_btn.setEnabled(False)
        self.voxel_num_thre2d = 20 #总像素数小于这个参数的部分会被删除
        # self.has_send = False #标记是否按下了`yes`按钮
        self.ui.confirm_btn.setEnabled(False)
        self.ui.detect_btn.setEnabled(False)
        self.ui.remask_btn.setEnabled(False)
        self.ui.reset_btn.setEnabled(False)
        self.ui.undo_btn.setEnabled(False)
        self.ui.nextImage_btn.setEnabled(False)
        self.ui.previousImage_btn.setEnabled(False)

        self.kernal = np.ones((5, 5)) #这个视情况而定，一般不要设置的太大

    def init(self): #一些初始化设置
        self.client.server_send_text_finished_signal.connect(self.update_file_listWidget)
        self.client.server_send_mask_finished_signal.connect(self.set_image_mask)
        self.client.connection_close_signal.connect(self.on_connection_close_signal)
        
        self.image_player = ImageShow()
        self.ui.image_show_label.setAlignment(Qt.AlignCenter)

    def signal_bind(self): #绑定按钮信号
        self.ui.link_btn.clicked.connect(self.link_btn_clicked)
        self.ui.input_yes_btn.clicked.connect(self.input_yes_btn_clicked)
        self.ui.previousImage_btn.clicked.connect(self.previousImage_btn_clicked)
        self.ui.nextImage_btn.clicked.connect(self.nextImage_btn_clicked)
        self.ui.slice_ListW.doubleClicked.connect(self.slice_ListW_double_clicked)
        self.ui.detect_btn.clicked.connect(self.detect_btn_clicked)
        self.ui.reset_btn.clicked.connect(self.reset_btn_clicked)
        self.ui.undo_btn.clicked.connect(self.undo_btn_clicked)
        self.ui.input_change_btn.clicked.connect(self.input_change_btn_clicked)
        self.ui.save_config_btn.clicked.connect(self.save_config_btn_clicked)
        self.ui.remask_btn.clicked.connect(self.remask_btn_clicked)
        self.ui.select_mask_store_path_btn.clicked.connect(self.select_mask_store_path_btn_clicked)
        self.ui.confirm_btn.clicked.connect(self.confirm_btn_clicked)

    def set_font(self):
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(18)  # 设置初始字体大小

        # 输入ip和端口区
        self.ui.ip_LineEdit.setFont(font)
        self.ui.port_LineEdit.setFont(font)
        self.ui.link_btn.setFont(font)
        self.ui.save_config_btn.setFont(font)

        # server的按钮功能区
        self.ui.nextImage_btn.setFont(font)
        self.ui.previousImage_btn.setFont(font)
        self.ui.reset_btn.setFont(font)
        self.ui.confirm_btn.setFont(font)
        self.ui.detect_btn.setFont(font)
        self.ui.undo_btn.setFont(font)
        self.ui.remask_btn.setFont(font)

        # local的按钮功能区
        self.ui.local_reset_btn.setFont(font)
        self.ui.local_confirm_btn.setFont(font)
        self.ui.local_detect_btn.setFont(font)
        self.ui.local_undo_btn.setFont(font)
        self.ui.choose_file_btn.setFont(font)

        # server输入文件地址功能区
        self.ui.vol_label.setFont(font)
        self.ui.mask_label.setFont(font)
        self.ui.vol_LEdit.setFont(font)
        self.ui.maskPath_LEdit.setFont(font)
        self.ui.input_yes_btn.setFont(font)
        self.ui.input_change_btn.setFont(font)
        self.ui.select_mask_store_path_btn.setFont(font)

    def link_btn_clicked(self):
        if(self.global_connected):
            QMessageBox.warning(self, '提示', '已经连接到服务器', QMessageBox.Yes | QMessageBox.No)
            return
        self.ip = self.ui.ip_LineEdit.text()
        self.port = self.ui.port_LineEdit.text()
        if(not(self.ip and self.port)):
            QMessageBox.critical(self, '错误', '请输入IP地址和端口号', QMessageBox.Yes | QMessageBox.No)
            return
        ipv4_pattern = re.compile(r'^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$')
        if(not ipv4_pattern.match(self.ip)):
            QMessageBox.critical(self, '错误', 'IP地址输入格式错误！', QMessageBox.Yes | QMessageBox.No)
            return
        port_pattern = re.compile(r'^([0-9]{1,5})$')
        if(not port_pattern.match(self.port)):
            QMessageBox.critical(self, '错误', '端口号输入格式错误！', QMessageBox.Yes | QMessageBox.No)
            return
        reply = QMessageBox.question(self, 'Message', '确定连接到服务器吗?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return
        ## 进行连接
        url = f'http://{self.ip}:{self.port}'
        self.client = SocketClient(url)
        try:
            self.client.connect()
        except:
            QMessageBox.information(self, '提示', '连接失败！或者检查服务器是否开启或者关掉VPN！', QMessageBox.Yes | QMessageBox.No)
            return
        QMessageBox.information(self, '提示', '连接成功！',  QMessageBox.Yes | QMessageBox.No)
        self.init() #当连接成功后，才可以开始绑定信号
        self.global_connected = True #全局标记是否连接成功的选项
        
    def input_yes_btn_clicked(self):
        if(not self.global_connected):
            QMessageBox.critical(self, '错误', '先连接服务器!', QMessageBox.Yes | QMessageBox.No)
            return
        mask_path = self.ui.maskPath_LEdit.text()
        label_file_path = self.ui.vol_LEdit.text()
        if(not(mask_path and label_file_path)):
            QMessageBox.critical(self, '错误', '先输入相关文件路径', QMessageBox.Yes | QMessageBox.No)
            return
        if(not os.path.exists(mask_path)):
            QMessageBox.critical(self, '错误', '输入的mask存储路径不存在！', QMessageBox.Yes | QMessageBox.No)
            return
        reply = QMessageBox.question(self, 'Message', '确定开始转换吗?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        self.ui.image_show_label.delete_all() #重新加载了，因此要全部删除

        self.ui.maskPath_LEdit.setEnabled(False)
        self.ui.vol_LEdit.setEnabled(False)
        self.ui.input_yes_btn.setEnabled(False)
        self.ui.select_mask_store_path_btn.setEnabled(False)
        self.ui.input_change_btn.setEnabled(True)

        self.showProgressDialog('正在进行转换，请稍后...\n注意：此项可能需要较长时间\n  您可以选择关闭此窗口')
        self.ui.input_yes_btn.setEnabled(False)

        # self.client.sio.send_text(label_file_path)
        self.client.send_text(label_file_path) #发送，并开始转换
        self.ui.confirm_btn.setEnabled(True)
        self.ui.detect_btn.setEnabled(True)
        self.ui.remask_btn.setEnabled(True)
        self.ui.reset_btn.setEnabled(True)
        self.ui.undo_btn.setEnabled(True)
        self.ui.nextImage_btn.setEnabled(True)
        self.ui.previousImage_btn.setEnabled(True)

    def nextImage_btn_clicked(self):
        self.image_player.get_next()
        self.ui.image_show_label.loadImage(self.image_player.get_current())
        # self.img_show(self.image_player.get_current())

    def previousImage_btn_clicked(self):
        self.image_player.get_prev()
        self.ui.image_show_label.loadImage(self.image_player.get_current())
        # self.img_show(self.image_player.get_current())

    def slice_ListW_double_clicked(self):
        self.image_player.set_location(self.ui.slice_ListW.currentRow())
        self.ui.image_show_label.loadImage(self.image_player.get_current())
        # self.img_show(self.image_player.get_current())

    def update_file_listWidget(self,data): #更新list_widget中的所有内容
        # data存储所有转换后的二维图像的完整文件路径, store_path表示存储文件的文件夹名称
        # self.update_image_signal.emit() #发送这个信号
        if(data['code']!=100):
            QMessageBox.warning(self, '提示', data['info'], QMessageBox.Yes | QMessageBox.No)
            return
        self.ui.image_show_label.image_update() #更新

        self.progress_dialog.close()
        self.ui.slice_ListW.clear()

        self.vol_trance_to_slice_data = data['file_list'] #要依靠这个去将标注的文件、和输入的prompts发送给服务器
        print(data['file_list'])
        # print(i.split('/')[0] for i in data['file_list'])
        self.ui.slice_ListW.addItems([os.path.basename(i).split('.')[0] for i in data['file_list']])
        self.image_player.change_path(os.path.join('client_file',data['file_store_path']))
        self.image_player.ite()
        if(self.image_player.get_first()): #如果不为空
            self.ui.image_show_label.loadImage(self.image_player.get_first())
            self.ui.image_show_label.setAttribute(Qt.WA_TransparentForMouseEvents, False) #有了图片之后，就可以设置对鼠标点击有效了
            # self.img_show(self.image_player.get_first())

    def set_image_mask(self,data):
        print('接收到mask结束的信号')
        self.progress_dialog.close() #关闭进度窗口
        code = data['code']
        if(code==100):
            file_name = data['file_name'] #就是这个Mask对应的图片在服务器中的存储位置
            mask = np.load(data['mask'])
            file_parent_path = os.path.dirname(file_name).replace('/','-')
            file_prefix = os.path.basename(file_name).split('.')[0]
            # 在这里就要把Mask存储起来
            mask_numpy = mask['array'] # np.ndarray形式存储起来的mask
            mask_numpy = cc3d.dust(
                mask_numpy, threshold=self.voxel_num_thre2d, connectivity=8, in_place=True
            )
            file_store_path = os.path.join('.\client_file\mask',file_parent_path)
            os.makedirs(file_store_path,exist_ok=True) #创建文件夹
            file_final_path = os.path.join(file_store_path,file_prefix+'.tif')
            # tiff.imwrite(file_final_path,mask_numpy)

            ## 尝试进行开闭运算
            # image = tiff.imread('frontpage\mask_store_path\sample8_proj_000.tif')
            opened_image = ndimage.binary_opening(mask_numpy, structure=self.kernal)
            closed_image = ndimage.binary_closing(opened_image, structure=self.kernal)
            tiff.imwrite(file_final_path,closed_image)

            res = self.ui.image_show_label.loadMask(file_final_path)
            if(res==-1):
                QMessageBox.critical(self, '错误', '出现了不可预料的错误！请重试！', QMessageBox.Yes | QMessageBox.No)
                return
            # print('成功收到')
        else:
            QMessageBox.critical(self, '错误', data['info'], QMessageBox.Yes | QMessageBox.No)
            return


    def on_connection_close_signal(self):
        self.global_connected = False
        QMessageBox.information(self, '提示', '与服务器的连接已断开', QMessageBox.Yes | QMessageBox.No)
        return

    def detect_btn_clicked(self):
        # if(not self.has_send):
        #     QMessageBox.warning(self, '提示', '请先输入文件路径!', QMessageBox.Yes | QMessageBox.No)
        #     return

        reply = QMessageBox.question(self, 'Message', '确定开始检测mask吗? ', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return
        data = self.ui.image_show_label.current()
        path = data['path']
        points = data['points']
        print('最开始的points: ',points)
        if(len(points)==0):
            QMessageBox.warning(self, '提示', '请先输入点作为prompt!', QMessageBox.Yes | QMessageBox.No)
            return
        
        self.showProgressDialog('正在检测mask与网络传输！\n注意：此项可能需要较长时间\n  您可以选择关闭此窗口')
        send_points = []
        for point in points:
            send_points.append([round(point.x(),2),round(point.y(),2)]) #将点保留两位小数，以列表的方式发送出去
        print(send_points)
        # path_list = path.replace('-', '/').split('\\')
        # server_path = ''
        # for i in range(1,len(path_list)-1):
        #     server_path = server_path+i+'/'
        # print(path_list) #类似于这种：['client_file', '/mnt/no1/liu_yang/use_sam_to_segment/file_to_test/dir', 'metal_trace_000.jpg']
        server_file_path = path.replace('-', '/').replace('\\', '/')[12:]
        print(send_points)
        send_data = {'file_path': server_file_path,
                     'points':send_points}
        self.client.on_segment_request(send_data)
        # print(server_file_path)

    def reset_btn_clicked(self):
        reply = QMessageBox.question(self, 'Message', '确定将prompt和mask都删除吗? ', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        else:
            self.ui.image_show_label.reset()
            QMessageBox.information(self, '提示', '成功reset', QMessageBox.Yes | QMessageBox.No)


    def undo_btn_clicked(self):
        self.ui.image_show_label.undoLastPoint() #撤销上一个点

    def confirm_btn_clicked(self):
        result = self.ui.image_show_label.confirm()
        if(result['code']==101):
            QMessageBox.warning(self, '提示', '请先检测得到mask', QMessageBox.Yes | QMessageBox.No)
            return
        reply = QMessageBox.question(self, 'Message', '确定保存这个mask吗？', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return
        mask_path = result['path']
        mask_store_path = self.ui.maskPath_LEdit.text() #必须要随时获得
        if(not os.path.exists(mask_store_path)):
            QMessageBox.critical(self, '错误', '出错了！mask存储路径不存在！', QMessageBox.Yes | QMessageBox.No)
            return #以防万一
        target_path = os.path.join(mask_store_path,os.path.basename(mask_path))
        print('target_path: ',target_path)
        shutil.copy(mask_path,target_path)
        QMessageBox.information(self, '提示', 'mask已经被保存!', QMessageBox.Yes | QMessageBox.No)

    def input_change_btn_clicked(self):
        reply = QMessageBox.question(self, 'Message', '确定更改相关路径吗？', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return
        # self.ui.maskPath_LEdit.clear()
        # self.ui.vol_LEdit.clear()
        self.ui.maskPath_LEdit.setEnabled(True)
        self.ui.vol_LEdit.setEnabled(True)
        self.ui.input_yes_btn.setEnabled(True)
        self.ui.select_mask_store_path_btn.setEnabled(True)
        self.ui.input_change_btn.setEnabled(False)

    def save_config_btn_clicked(self):
        reply = QMessageBox.question(self, 'Message', '确定保存配置吗？', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return
        if(not self.global_connected):
            QMessageBox.critical(self, '错误', '请先连接成功！', QMessageBox.Yes | QMessageBox.No)
            return
        config = configparser.ConfigParser()

        config['Server'] = {
            'ip_address': self.ip,
            'port': self.port
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def remask_btn_clicked(self):
        reply = QMessageBox.question(self, 'Message', '确定删除这个mask吗', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return
        res = self.ui.image_show_label.dropMask() #去除此时的mask
        if(res==101):
            QMessageBox.warning(self, '提示', '先检测得到mask', QMessageBox.Yes | QMessageBox.No)
            return
    
    def select_mask_store_path_btn_clicked(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        if(not os.path.exists(folder_path)):
            QMessageBox.critical(self, '错误', '文件路径不存在', QMessageBox.Yes | QMessageBox.No)
            return
        self.mask_store_path = folder_path
        self.ui.maskPath_LEdit.setText(folder_path)

    def showProgressDialog(self,text):
        self.progress_dialog = QProgressDialog('Task in progress.', 'Cancel', 0, 0)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setWindowTitle('Processing')
        self.progress_dialog.setLabelText(f"{text}")
        self.progress_dialog.setCancelButton(None)

        self.progress_dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)#禁用帮助按钮
        self.progress_dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, False) #启用隐藏按钮

        # self.progress_dialog.setWindowIcon(QIcon("./FrontPage/images/process.png"))
        self.progress_dialog.setFont(QFont('Arial',15))
        self.progress_dialog.setRange(0, 0)
        self.progress_dialog.setFixedSize(500,200)
        self.progress_dialog.show()

#图片播放类
class SN:
    def __init__(self):
        self.img_media_list = []
        self.location = 0

#加载qss文件
class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()

if __name__ == '__main__':
    app = QApplication([])
    demo = page()

    #加载QSS文档
    styleFile = 'style.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    # demo.ui.setStyleSheet(qssStyle)
    demo.setStyleSheet(qssStyle)

    # demo.ui.show()
    demo.show()
    app.exec()
