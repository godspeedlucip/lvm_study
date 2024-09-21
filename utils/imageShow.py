import os
import copy

class myImage:
    def __init__(self,path,gap_width=0,gap_height=0,factor = 0,relevant_points = [],true_point=[],mask = None):
        self.path = path
        self.gap_width = gap_width
        self.gap_height = gap_height
        self.factor = factor
        self.relevant_points = relevant_points #打点处相对于label的坐标QPoint
        self.true_points = true_point #打点处相对于pixmap的坐标QPoint
        self.mask = mask

    def get_relevant_points(self):
        return self.relevant_points
    
    def append_relevant_point(self,point):
        self.relevant_points.append(point)

    def set_relevant_points(self, points):
        self.relevant_points = copy.deepcopy(points)

    def get_true_points(self):
        return self.true_points
    def append_true_point(self,point):
        self.true_points.append(point)
    def set_true_points(self, points):
        self.true_points = copy.deepcopy(points)

    def get_gap_width(self):
        return self.gap_width
    def get_gap_height(self):
        return self.gap_height
    def set_gap_width(self,gap_width):
        self.gap_width = gap_width
    def set_gap_height(self,gap_height):
        self.gap_height = gap_height
    def get_path(self):
        return self.path

    def set_factor(self,factor):
        self.factor = factor
    def get_factor(self):
        return self.factor

    def get_mask_path(self):
        return self.mask
    
    def set_mask_path(self,mask_path):
        if(mask_path):
            self.mask = copy.copy(mask_path)
    
    def delete_mask_path(self):
        self.mask = None
    
    def reset(self):
        self.true_points.clear()
        self.relevant_points.clear()
        self.mask = None





class ImageShow:
    def __init__(self, path=None):
        self.media_list = []
        if(path):
            for i in os.listdir(path):
                self.media_list.append(myImage(os.path.join(path,i)))
        self.location = 0

    def get_first(self):
        return self.media_list[0]

    def get_current(self):
        return self.media_list[self.location]

    def get_prev(self):
        if(self.media_list == []):
            return
        if(self.location==0): #如果已经是第一张图片
            self.location = len(self.media_list)-1
            return self.media_list[-1]
        else:
            self.location = self.location - 1
            return self.media_list[self.location]

    def get_next(self):
        if (self.media_list == []):
            return
        if(self.location==len(self.media_list)-1): #如果已经是最后一张图片
            self.location = 0
            return self.media_list[0]
        else:
            self.location = self.location + 1
            return self.media_list[self.location]

    def ite(self):
        for i in self.media_list:
            print(i)


    def set_location(self,location):
        self.location = location

    def change_path(self,path):
        if(path==None):
            return
        self.media_list = []
        if(path):
            for i in os.listdir(path):
                self.media_list.append(myImage(os.path.join(path,i)))
        self.location = 0
