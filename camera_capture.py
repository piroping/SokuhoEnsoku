import cv2
import tkinter as tk
from tkinter.simpledialog import askinteger
import atexit
import json
import os
import time

class Application(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.name_dict = {}
        
        self.load_json()
        
        self.cap = cv2.VideoCapture(0)
        self.qcd = cv2.QRCodeDetector()
        
        self.counter = 0 # 画面出力の削除の制御用
        
        atexit.register(self.exit)
        self.write_tk()
        self.camera()
    
    def write_tk(self):
        self.spinbox_font = ('', 10)
        self.label_font = ('', 40)
        self.year_val = tk.IntVar()
        self.class_val = tk.StringVar()
        self.number_val = tk.IntVar()
        
        self.label = tk.Label(text='', font=self.label_font)
        self.year_spinbox = tk.Spinbox(textvariable=self.year_val, from_=1, to=3, increment=1, wrap=True, width=2, font=self.spinbox_font)
        self.class_spinbox = tk.Spinbox(textvariable=self.class_val, values=['A', 'B', 'C', 'D', 'E'],increment=1, wrap=True, width=2, font=self.spinbox_font)
        self.number_spinbox = tk.Spinbox(textvariable=self.number_val, from_=1, to=50, increment=1, wrap=True, width=2, font=self.spinbox_font)
        
        self.check_button = tk.Button(text='確認', font=self.spinbox_font, command=self.check_name)
        self.check_point = tk.Label(text=f'第{self.target}関門')
        self.passage_button = tk.Button(text='通過', font=self.spinbox_font, command=self.write_name)
        
        self.label.grid(column=0, row=0, columnspan=3)
        self.year_spinbox.grid(column=0, row=1, sticky=tk.EW)
        self.class_spinbox.grid(column=1, row=1, sticky=tk.EW)
        self.number_spinbox.grid(column=2, row=1, sticky=tk.EW)
        
        self.check_button.grid(column=0, row=2, sticky=tk.EW)
        self.check_point.grid(column=1, row=2, sticky=tk.EW)
        self.passage_button.grid(column=2, row=2, sticky=tk.EW)
        
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
    
    def load_json(self):
        self.file_name = self.find_json()
        self.target = askinteger('速歩遠足', 'ここは何関門ですか？', initialvalue=1)
        if self.target is None:
            exit()
        self.name_dict['checkpoint'] = self.target
        self.write_json()
    
    def exit(self):
        self.cap.release()
        cv2.destroyAllWindows()
    
    def camera(self):
        _, frame = self.cap.read()
        r, *_,= self.qcd.detectAndDecode(frame)
        if r:
            self.write_time(r)
            self.counter += 1
            self.after(1000, self.reduce_counter)
        frame = cv2.resize(frame, (1000, 500))
        cv2.imshow('reader', frame)
        self.after(50, self.camera)
    
    def reduce_counter(self):
        self.counter -= 1
        if self.counter == 0:
            self.label['text'] = ''
    
    def write_time(self, ip):
        if ip == None:
            return
        t = time.time()
        if ip not in self.name_dict:
            self.label['text'] = f'{len(self.name_dict)}位'
            self.name_dict[ip] = t
            self.write_json()
        
    def write_json(self):
        with open(self.file_name + '.json', 'w') as f:
            json.dump(self.name_dict, f)
    
    def find_json(self):
        file_name = 0
        while True:
            if os.path.isfile(f'{file_name}.json'):
                file_name += 1
            else:
                return str(file_name)

    def check_name(self):
        ip = str(self.year_val.get()) + self.class_val.get() + str(self.number_val.get()).zfill(2)
        if ip in self.name_dict:
            self.label['text'] = '通過しています'
        else:
            self.label['text'] = '通過していません'
    
    def write_name(self):
        ip = str(self.year_val.get()) + self.class_val.get() + str(self.number_val.get()).zfill(2)
        self.write_time(ip)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('400x95')
    root.title('速歩遠足  受付機')
    root.resizable(width=True, height=False)
    application = Application(root)
    application.mainloop()

# pip install -r requirements.txt