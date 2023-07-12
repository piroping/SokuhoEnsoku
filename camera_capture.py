import cv2
import tkinter as tk
from tkinter.simpledialog import askinteger
import atexit
import json
import os

class Application(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        self.name_dict = self.read_json()
        print(self.name_dict)
        
        self.cap = cv2.VideoCapture(0)
        self.qcd = cv2.QRCodeDetector()
        
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
        
        self.check_button = tk.Button(text='確認', font=self.spinbox_font)
        self.passage_button = tk.Button(text='通過', font=self.spinbox_font)
        
        self.label.grid(column=0, row=0, columnspan=3)
        self.year_spinbox.grid(column=0, row=1, sticky=tk.EW)
        self.class_spinbox.grid(column=1, row=1, sticky=tk.EW)
        self.number_spinbox.grid(column=2, row=1, sticky=tk.EW)
        
        self.check_button.grid(column=0, row=2, sticky=tk.EW)
        self.passage_button.grid(column=2, row=2, sticky=tk.EW)
        
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
    
    def read_json(self):
        c = True
        target = '0'
        for i in os.listdir():
            if i[-4:] == 'json':
                c = False
                target = i[0]
                break
        if c:
            target = str(askinteger('速歩遠足', 'ここは何関門ですか？', initialvalue=1))
            with open(target + '.json', 'w') as f:
                json.dump({'barrier':target}, f)
        
        with open(target + '.json', 'r') as f:
            return json.load(f)
    
    def exit(self):
        self.cap.release()
        cv2.destroyAllWindows()
    
    def camera(self):
        _, frame = self.cap.read()
        r, *_,= self.qcd.detectAndDecode(frame)
        if r:
            self.label['text'] = r
        frame = cv2.resize(frame, (1000, 500))
        cv2.imshow('test', frame)
        self.after(100, self.camera)
        

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('200x95')
    root.title('速歩遠足  受付機')
    root.resizable(width=True, height=False)
    application = Application(root)
    application.mainloop()

# pip install -r requirements.txt