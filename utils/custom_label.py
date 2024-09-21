# 自定义label，实现在图上打点，并记录点的位置

from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QPixmap, QImage
from PyQt5.QtWidgets import  QLabel
from utils import myImage
import copy
import sys
import os
import tifffile as tiff
from PIL import Image
import numpy as np


'''注意: 赋值列表时要使用copy.deepcopy进行深拷贝!'''

class ImageLabel(QLabel):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True) #使其对鼠标的点击事件无效
        self.relevant_points = [] #相对于label左上角的坐标
        self.true_points = [] # 相对于图片左上角的坐标（图片是实际的尺寸）
        self.mask = None #初始化为None
        self.image = {} #存储所有的image对象，key就是这个image的path

    def loadImage(self, myImage): #加载图片时肯定会传入图片的路径，根据这个路径作为键，存储每张图片的点
        if self.pixmap(): #第一次加载时肯定是没有pixmap的
            # 如果已经显示了图片，那么可能已经打了点了，因此就要将它保存起来
            self.image[self.current_path].set_relevant_points(self.relevant_points)
            self.image[self.current_path].set_true_points(self.true_points)
            # self.image[self.current_path].set_mask(self.mask)
            self.relevant_points.clear()
            self.true_points.clear()
            self.mask = None

        # 得在if语句的后面
        self.current_path = myImage.get_path()
        self.image[self.current_path] = myImage # 后面会用到，因此第一步就要设置

        print('=======',self.current_path,'=======')

        # 加载新图片
        self.img_show(myImage)

        self.relevant_points = copy.deepcopy(self.image[self.current_path].get_relevant_points())
        self.true_points = copy.deepcopy(self.image[self.current_path].get_true_points())
        self.mask = None
        mask_path = self.image[self.current_path].get_mask_path()
        if(mask_path):
            self.loadMask(mask_path)
            # self.mask = self.image[self.current_path].get_mask().copy()
        self.update()

    def loadMask(self, mask_path): #将mask画在图上
        # 默认把mask保存在'client_file/mask/server_file_path/file_name'的文件夹中
        if(not os.path.exists(mask_path)):
            return -1
        self.image[self.current_path].set_mask_path(mask_path)
        print(mask_path)

        self.mask = tiff.imread(mask_path)
        # tiff_image = Image.open(mask_path)
        # image_array = np.array(tiff_image)
        # binary_array = np.where(image_array, 255, 0).astype(np.uint8)
        # height, width = binary_array.shape
        # bytes_per_line = width  # 每行字节数，1 个字节代表 1 个像素
        # qimage = QImage(binary_array.data, width, height, bytes_per_line, QImage.Format_Indexed8)
        # resized_mask, _ = self.m_resize(self.width(), self.height(), qimage)
        # self.mask = resized_mask

        self.update()

    def dropMask(self): #删除这个mask，并不显示当前的mask
        cur_mask_path = self.image[self.current_path].get_mask_path()
        if(cur_mask_path is None):#如果mask_path不存在
            return 101

        os.remove(cur_mask_path) #删除mask文件
        self.image[self.current_path].delete_mask_path() #把mask_path删除

        self.mask = None #置空就行
        self.update()
        return 100

    def reset(self):
        # 将打的点和获得的mask都清除
        # self.image[self.current_path].relevant_points.clear()
        # self.image[self.current_path].true_points.clear()
        # self.image[self.current_path].set_mask(None)
        self.relevant_points.clear()
        self.true_points.clear()
        self.mask = None
        cur_mask_path = self.image[self.current_path].get_mask_path()
        if(cur_mask_path and os.path.exists(cur_mask_path)):
            os.remove(cur_mask_path) #删除这个文件
        self.image[self.current_path].delete_mask_path() #也要把它里面的给删除
        self.update() #更新，重新绘制label

    def current(self): # 在detect按钮被按下后调用，返回当前显示图片的服务器路径和输入的point
        # 有可能是第一张，而没有切换就不会保存打的点。因此直接将其手动的保存
        self.image[self.current_path].set_relevant_points(self.relevant_points)
        self.image[self.current_path].set_true_points(self.true_points)

        # 获取当前图片的路径和点
        cur_img_path = self.image[self.current_path].get_path()
        data = {'path':cur_img_path,
                'points':self.image[self.current_path].get_true_points()}
        return data

    def confirm(self):
        # 返回数据
        mask_path = self.image[self.current_path].get_mask_path()
        if(mask_path): #如果path存在
            code = 100
        else: #如果path不存在
            code = 101
        data = {'code':code,
                'path':mask_path}
        return data

    def delete_all(self): #删除全部的东西
        # 首先把系统中暂存的给删除
        self.true_points.clear()
        self.relevant_points.clear()
        self.mask = None
        self.current_path = None
        # 再把所有的东西都给删除
        for value in self.image.values():
            value.reset()
        self.clear()
        # 释放字典的空间
        self.image.clear()

    def image_update(self): #当列表中的图片更新时，需要清空这些记录的信息
        self.image.clear()
        self.relevant_points.clear()
        self.true_points.clear()

    def img_show(self,image):
        # print(self.current_path)
        label_image=QImage(image.get_path()) #使用QImage打开图片
        pil_image,factor = self.m_resize(self.width(), self.height(), label_image)
        pixmap = QPixmap.fromImage(pil_image)
        label_size = self.size()
        pixmap_size = pixmap.size()

        label_to_pixmap_width_gap = label_size.width()-pixmap_size.width()
        label_to_pixmap_height_gap = label_size.height()-pixmap_size.height()
        # 更新image
        self.image[self.current_path].set_gap_width(label_to_pixmap_width_gap)
        self.image[self.current_path].set_gap_height(label_to_pixmap_height_gap)
        self.image[self.current_path].set_factor(factor)

        self.resize(pil_image.width(),pil_image.height())
        self.setPixmap(pixmap)

    def m_resize(self,w_box, h_box, pil_image):  # 参数是：要适应的窗口宽、高、Image.open后的图片
        #调整图片的大小
        w, h = pil_image.width(), pil_image.height() # 获取图像的原始大小
        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h
        factor = min([f1, f2])
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.scaled(width, height),factor

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: #确保是鼠标左键的点击事件
            # 获取鼠标点击的地方，相对于label的左上角的坐标
            relevant_x = event.pos().x()
            relevant_y = event.pos().y()
            # 获取鼠标点击的地方，相对于pixmap的左上角的坐标
            true_x = float(relevant_x-self.image[self.current_path].get_gap_width()/2)/self.image[self.current_path].get_factor()
            true_y = float(relevant_y-self.image[self.current_path].get_gap_height()/2)/self.image[self.current_path].get_factor()

            if(relevant_x > (self.width()-self.image[self.current_path].get_gap_width()/2)):
                return
            if(relevant_y > (self.height()-self.image[self.current_path].get_gap_height()/2)):
                return
            if(true_x<0 or true_y<0): #打的点必须在图片的有效范围内
                return
            # print(true_x,true_y)
            # 将打的点的全局坐标添加到列表中
            self.relevant_points.append(QPoint(relevant_x,relevant_y)) #在创建QPoint对象时，输入的坐标最终会被转换为整数
            self.true_points.append(QPoint(true_x,true_y))
            self.update() #这个方法会调用paintEvent方法
            print(f'relevant_x: {relevant_x}, relevant_y: {relevant_y}, true_x: {true_x}, true_y: {true_y}')

    def undoLastPoint(self):
        # 撤销上一个点
        if self.relevant_points:
            self.relevant_points.pop()
            self.true_points.pop()
            self.update()

    def paintEvent(self, event): #label被初始化的时候也会调用这个函数
        # print(self.current_path)
        # 先调用父类的paintEvent来绘制原始图片
        super().paintEvent(event)

        # 然后在图片上绘制点
        painter = QPainter(self)
        pen = QPen(Qt.red, 5)
        painter.setPen(pen)

        # 将点绘制在当前显示图片的相应位置上
        for point in self.relevant_points:
            painter.drawPoint(QPoint(point.x(), point.y()))

        # 将mask画在图上
        pen = QPen(Qt.green, 1)
        painter.setPen(pen)
        # if self.mask: #如果当前有mask
        #     # painter.setOpacity(0.2)  # 设置透明度
        #     painter.drawImage(self.image[self.current_path].get_gap_width()/2, self.image[self.current_path].get_gap_height()/2, self.mask)
        if(not self.mask is None):
            for i in range(self.mask.shape[0]): #height
                for j in range(self.mask.shape[1]):#width
                    if(self.mask[i][j]): #如果是有效区域
                        factor = self.image[self.current_path].get_factor()
                        x = j*factor
                        y = i*factor
                        x_inter = self.image[self.current_path].get_gap_width()/2
                        y_inter = self.image[self.current_path].get_gap_height()/2
                        painter.drawPoint(QPoint(x+x_inter, y+y_inter))

