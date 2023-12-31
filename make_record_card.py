from read_name_list import ReadNameList
from PIL import Image, ImageFont, ImageDraw
import qrcode
import os

class MakeRecord:
    def __init__(self):
        self.name = ReadNameList().open()
        self.make()
    
    def make(self):
        if not os.path.isdir('./records/'):
            os.mkdir('./records')
        l = len(self.name) // 8
        if len(self.name) % 8 != 0:
            l += 1
        for i in range(l):
            self.write(self.name[i * 8:i * 8 + 8], i)
    
    def write(self, li, ind):
        image = Image.new('L', (2894, 4093), 255)
        font = ImageFont.truetype('C:/Windows/Fonts/BIZ-UDGothicR.ttc', 72)
        draw = ImageDraw.Draw(image)
        for i, (x, y) in zip(li, [(i, j) for i in range(2) for j in range(4)]):
            draw.multiline_text((image.width // 2 * x + 180, image.height // 4 * y + 50), f'函館ラ・サール学園  速歩遠足\n{i[0]}年{i[1]}組{i[2]}番', fill=0, font=font)
            code = qrcode.make(f'{i[0]}{i[1]}{str(i[2]).zfill(2)}', error_correction = qrcode.constants.ERROR_CORRECT_H, box_size = 30) # type: ignore
            image.paste(code, (image.width // 2 * x - 100 + 180, image.height // 4 * y + 150 + 50))
        
        draw.line((image.width / 2, 0, image.width / 2, image.height), 0, width=8)
        for i in range(1, 4):
            draw.line((0, image.height / 4 * i, image.width, image.height / 4 * i), 0, width=8)
        
        image.save(f'records/{ind}.png')

if __name__ == '__main__':
    t = MakeRecord()
