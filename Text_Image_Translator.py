from PIL import Image
import random
from File_Handler import save_file, upload_file
import time as Time


class Text_Image_Translator:
    """
    A class that encrypts and decrypts text into images and vice versa
    The class can use a seed to randomize characters, to make the encryption more secure

    """
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
        """
        Used to set the seed of the randomizer
        """
        self.seed = seed
        self.randomize(seed)

    def randomize(self, seed):
        """
        Randomizes the order of the characters
        """
        random.seed(seed)
        random.shuffle(self.chars)

    def get_dimensions(self, length):
        """
        Calculates the dimensions of the image based on the length of the text
        """
        sqrt = length**0.5
        if sqrt%1 != 0:
            width = int(sqrt)+1
            height = int(sqrt)
        else:
            width = int(sqrt)
            height = int(sqrt)
        return width, height
    
    def get_rgb(self, char):
        """
        Returns the RGB values based on the index of the given character in the list
        """
        index = self.chars.index(char)
        r = index // 255 // 255
        g = index // 255 % 255
        b = index % 255
        return r, g, b
    
    def get_char(self, r, g, b):
        """
        Returns the character based on the RGB values
        """
        index = r*255*255 + g*255 + b
        return self.chars[index]
    
    def encrypt(self, text):
        """
        Encrypts the given text into an image
        Returns the image as a PIL Image object
        """
        if self.DEBUG:
            startTime = Time.time() 

        length = len(text)
        width, height = self.get_dimensions(length)
        img = Image.new('RGB', (width, height))
        pixels = img.load()
        for i in range(width):
            w_index = i*height
            for j in range(height):
                index = w_index + j
                if index < length:
                    r, g, b = self.get_rgb(text[index])
                else:
                    r, g, b = self.get_rgb(' ')
                pixels[i, j] = (r, g, b)
        if self.DEBUG:
            print('Time to encrypt:', Time.time()-startTime)
        return img
    
    def decrypt(self, img):
        """
        Decrypts the given image into a text string
        Returns the translated string
        """
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
        """
        Saves the given image as a file
        Uses the save_file function from File_Handler.py
        """
        save_file(image)
    def upload_file(self, filename):
        """
        Uploads an image file
        Uses the upload_file function from File_Handler.py"""
        return upload_file(filename)
    

if __name__ == '__main__':
    def help(*args):
        if command == 'help':
            if len(args) == 3:
                help_command = args[2]
                if help_command == 'encrypt':
                    print('Usage: python Text_Image_Translator.py encrypt <text> <filename> [seed](optional)')
                    print('Encrypts a text into an image, and saves it as a file with the given filename')
                    print('If seed is not given, a default seed will be used')
                elif help_command == 'decrypt':
                    print('Usage: python Text_Image_Translator.py decrypt <filename> [seed](optional)')
                    print('Decrypts an image into a text, and prints the text')
                    print('If seed is not given, a default seed will be used')
                else:
                    print('Invalid command')
                    sys.exit(1)
            else:
                print('Commands:')
                print('encrypt <text> <filename> [seed](optional)')
                print('decrypt <filename> [seed](optional)\n')
                print('type "python Text_Image_Translator.py help <command>" for more info on a specific command')
    def encrypt(*args):
        translator = Text_Image_Translator(DEBUG=True)
        if len(args) < 4:
            print('Usage: python Text_Image_Translator.py encrypt <text> <filename> [seed](optional)')
            sys.exit(1)
        text = args[2]
        filename = args[3]
        if len(args) == 5:
            seed = int(args[4])
            translator.set_seed(seed)
        image = translator.encrypt(text)
        save_file(image, filename)
    def decrypt(*args):
        translator = Text_Image_Translator(DEBUG=True)

        if len(sys.argv) < 3:
            print('Usage: python Text_Image_Translator.py decrypt <filename> [seed](optional)')
            sys.exit(1)
        filename = sys.argv[2]
        if len(sys.argv) == 4:
            seed = int(sys.argv[3])
            translator.set_seed(seed)
        image = translator.upload_file(filename)
        text = translator.decrypt(image)
        print(text)
    
    import sys

    if len(sys.argv) < 2:
        print('Usage: python Text_Image_Translator.py <command> <args>')
        print('Type "python Text_Image_Translator.py help" for more info')
        sys.exit(1)
    else:
        command = sys.argv[1]   
        if command == 'encrypt':
            encrypt(*sys.argv)
        elif command == 'decrypt':
            decrypt(*sys.argv)
        elif command == 'help':
            help(*sys.argv)
        else:
            print('Invalid command')
            sys.exit(1)         


    





        

        




    




