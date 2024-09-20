from PIL import Image
import random
from File_Handler import save_file, upload_file
import time as Time


class Text_Image_Translator:
    def __init__(self, seed = 0, DEBUG = False):
        self.chars = []

        self.DEBUG = DEBUG
        if DEBUG:
            startTime = Time.time()

        for i in range(255**3-2):
            if i < 1114112:
                self.chars.append(chr(i))
            else:
                self.chars.append(' ')

        self.chars.append(' ')
        self.chars.append('\n')
        if DEBUG:
            print('Time to add chars:', Time.time()-startTime)

        self.seed = seed
        if DEBUG:
            startTime = Time.time()
        self.randomize(seed)
        if DEBUG:
            print('Time to randomize:', Time.time()-startTime)

    def set_seed(self, seed):
        self.seed = seed
        self.randomize(seed)

    def randomize(self, seed):
        random.seed(seed)
        random.shuffle(self.chars)

    def get_dimensions(self, length):
        sqrt = length**0.5
        if sqrt%1 != 0:
            width = int(sqrt)+1
            height = int(sqrt)
        else:
            width = int(sqrt)
            height = int(sqrt)
        return width, height
    
    def get_rgb(self, char):
        index = self.chars.index(char)
        r = index // 255 // 255
        g = index // 255 % 255
        b = index % 255
        return r, g, b
    
    def get_char(self, r, g, b):
        index = r*255*255 + g*255 + b
        return self.chars[index]
    
    def encrypt(self, text):
        if self.DEBUG:
            startTime = Time.time() 

        length = len(text)
        width, height = self.get_dimensions(length)
        img = Image.new('RGB', (width, height))
        pixels = img.load()
        for i in range(width):
            for j in range(height):
                index = (i*height+j)
                if index < length:
                    r, g, b = self.get_rgb(text[index])
                else:
                    r, g, b = self.get_rgb(' ')
                pixels[i, j] = (r, g, b)
        if self.DEBUG:
            print('Time to encrypt:', Time.time()-startTime)
        return img
    
    def decrypt(self, img):
        if self.DEBUG:
            startTime = Time.time()
        width, height = img.size
        pixels = img.load()
        text = ''
        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]
                text += self.get_char(r, g, b)
        if self.DEBUG:
            print('Time to decrypt:', Time.time()-startTime)
        return text
    
    def save_file(self, image):
        save_file(image)
    def upload_file(self, filename):
        return upload_file(filename)
    

if __name__ == '__main__':
    import sys
    translator = Text_Image_Translator(DEBUG=True)

    if len(sys.argv) < 2:
        print('Usage: python Text_Image_Translator.py <command> <args>')
        sys.exit(1)
    else:
        command = sys.argv[1]
        if command == 'encrypt':
            if len(sys.argv) < 4:
                print('Usage: python Text_Image_Translator.py encrypt <text> <filename>')
                sys.exit(1)
            text = sys.argv[2]
            filename = sys.argv[3]
            if len(sys.argv) == 5:
                seed = int(sys.argv[4])
                translator.set_seed(seed)
            image = translator.encrypt(text)
            save_file(image, filename)

        elif command == 'decrypt':
            if len(sys.argv) < 3:
                print('Usage: python Text_Image_Translator.py decrypt <filename>')
                sys.exit(1)
            filename = sys.argv[2]
            if len(sys.argv) == 4:
                seed = int(sys.argv[3])
                translator.set_seed(seed)
            image = translator.upload_file(filename)
            text = translator.decrypt(image)
            print(text)
        else:
            print('Invalid command')
            sys.exit(1)


    





        

        




    




