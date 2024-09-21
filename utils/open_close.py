import cv2
class operate_image:
    def __init__(self) -> None:
        pass
    
def open_calcu(image_path,length=5): #消除背景噪声，不改变前景图像的细节
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    kernel = np.ones((5, 5), np.uint8) # 创建结构元素5x5的矩形
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return opening

def close_calcu(image_path,length=5): #消除前景图像中的噪点，不影响背景的细节
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    kernel = np.ones((5, 5), np.uint8) # 创建结构元素5x5的矩形
    closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return closing