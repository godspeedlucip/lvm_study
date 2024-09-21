import socketio
import os
import hashlib
from PyQt5.QtCore import QObject, pyqtSignal
import tifffile as tiff
import io

class SocketClient(QObject):
    CHUNK_SIZE = 1024 * 64  # 每次发送64kb的chunk
    server_send_text_finished_signal = pyqtSignal(dict)  # 服务器的图片已经完整发送过来
    server_send_mask_finished_signal = pyqtSignal(dict) # 这张图片的mask已经被检测完成
    connection_close_signal = pyqtSignal()

    def __init__(self, url):
        super().__init__()
        self.sio = socketio.Client()
        self.sio.eio.ping_timeout = 60
        self.sio.continue_receive = True
        self.sio.continue_sending = False
        self.url = url
        self.temp_mask_path = os.path.join('client_file','temp_mask.dat')
        
        # 注册事件
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('text_result', self.handle_text_result)
        self.sio.on('send_text_finish', self.on_send_text_finish)
        self.sio.on('chunk_confirmation', self.on_confirmation)
        self.sio.on('segment_result', self.on_segment_result)
        self.sio.on('segment_result_send_finish', self.on_segment_result_send_finish)
        
    
    def on_connect(self):
        pass
    
    def on_disconnect(self):
        print("Disconnected from the server")
    
    ## 以下是在客户端输入文件路径后的网络传输代码
    def handle_text_result(self, data):
        code = data['code']
        if code == 100:  # 成功
            file_name = data['file_name']
            slice_name = data['slice_name']
            file_path = os.path.join('client_file', file_name, slice_name)
            # file_name = file_name.replace('/', '-') #会将转换的文件存储在`client/输入的文件路径/`
            os.makedirs(os.path.join('client_file', file_name), exist_ok=True)
            with open(file_path, 'ab') as f:
                f.write(data['chunk'])
                print(f'receiving {file_name}')
                self.sio.emit('text_continue_send', {'status': 'received'})
        
        else:
            self.server_send_text_finished_signal.emit(data)
    
    def send_text(self, text):
        # self.slice_save_path = file_store_path
        self.sio.emit('text', {'file_path': text})
    
    def on_send_text_finish(self, data):
        if data['status'] == 'finish':
            self.sio.continue_receive = False
            self.server_send_text_finished_signal.emit(data)
            print('client send text to server finished')
    
    def on_confirmation(self, data):
        if data['status'] == 'received':
            self.sio.continue_sending = True  # 标记可以继续发送
    
    ## 以下是客户端向服务器发送要标注的图片路径和点prompt是的网络传输代码
    def on_segment_request(self,data):
        self.sio.emit('segment', {'file_path': data['file_path'],
                                  'points':data['points']})


    ## 当服务器向客户端发送mask时，该函数进行处理
    def on_segment_result(self,data):
        code = data['code']
        print('进入这个函数')
        print('code: ',code)
        if(code==100):
            print('come here')
            file_name = data['file_name']
            with open(self.temp_mask_path, 'ab') as f:
                f.write(data['chunk'])
                print(f'receiving mask {file_name}')
                self.sio.emit('mask_continue_send', {'status': 'received'})
        elif(code==101): #表示文件不存在
            self.server_send_mask_finished_signal.emit(data)
        elif(code==102): #颜色格式不是灰度图像的格式
            self.server_send_mask_finished_signal.emit(data)
        elif(code==103):
            self.server_send_mask_finished_signal.emit(data)
        else:
            result = {'code':104,
                      'info':'服务器出错！请检查后重试'}
            self.server_send_mask_finished_signal.emit(result)

    def on_segment_result_send_finish(self,data):
        if(data['status'] == 'finish'):
            file_name = data['file_name']
            with open(self.temp_mask_path,'rb') as f:
                mask_metadata = f.read() 
            buffer = io.BytesIO(mask_metadata)
            # npz_file = np.load(buffer)
            result = {'file_name':file_name, #这是发送成功之后的处理
                      'code':100,
                      'mask':buffer} #将字节流数据传送给主界面
            self.server_send_mask_finished_signal.emit(result)
            os.remove(self.temp_mask_path) #将临时文件删除
            
    def send_image(self, image_path):
        client_md5 = hashlib.md5()
        with open(image_path, 'rb') as f:
            while chunk := f.read(self.CHUNK_SIZE):
                client_md5.update(chunk)
        client_md5 = client_md5.hexdigest()
        
        base_name = os.path.basename(image_path)
        prefix = base_name.split('.')[0]
        suffix = base_name.split('.')[-1]

        chunk_size = 1024 * 32 * 8
        with open(image_path, "rb") as f:
            chunk = f.read(chunk_size)
            while chunk:
                print('=========')
                self.sio.emit('image', {'chunk': chunk})
                self.sio.continue_sending = False
                while not self.sio.continue_sending:
                    self.sio.sleep(0.1)
                chunk = f.read(chunk_size)
        
        self.sio.emit('image_complete', {'prefix': prefix, 'suffix': suffix, 'md5': client_md5})
    
    def connect(self):
        self.sio.connect(self.url)
        return self.sio.connected
    
    def start_receiving(self):
        while self.sio.continue_receive:
            self.sio.sleep(0.5)
    
    def disconnect(self):
        self.sio.disconnect()
        self.connection_close_signal.emit()


# # Example usage in another file
# if __name__ == "__main__":
#     url = 'http://ip:port'
#     client = SocketClient(url)
    
#     client.connect()
#     dir_path = '/mnt/no1/liu_yang/Data_MAR/ProjData/sample5_metal.tif'
#     client.send_text(dir_path)
    
#     client.start_receiving()
#     client.disconnect()
