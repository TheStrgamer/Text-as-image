from PIL import Image
import random
from File_Handler import save_file, upload_file, save_image_file, upload_image_file
import time as Time
import numpy as np



class File_Image_Translator:
    """
    A class that encrypts and decrypts text into images and vice versa
    The class can use a seed to randomize characters, to make the encryption more secure

    """
    def __init__(self, seed = 0, DEBUG = False):
        self.chars = np.zeros(256, dtype='U1')
        valid_extencion_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_"
        i = 0
        for char in valid_extencion_characters:
            self.chars[i] = char
            i += 1
        for i in range(len(valid_extencion_characters),256-len(valid_extencion_characters)):
            self.chars[i] = ' '
        self.char_index = {}
        self.chars_original = self.chars.copy()

        self.seed = seed
        self.last_seed = seed
        self.randomized = False
        self.DEBUG = DEBUG
        if DEBUG:
            startTime = Time.time()

        self.mapped_ints = {}
        for i in range(256):
            self.mapped_ints[i] = i
        self.numbers = []
        
        if DEBUG:
            print('Time to add integers:', Time.time()-startTime)


            
    def set_seed(self, seed):
        """
        Used to set the seed of the randomizer
        """
        self.seed = int(seed)
        if self.seed != self.last_seed:
            self.last_seed = self.seed
            self.randomize(self.seed)
            if self.DEBUG:
                print('Seed set to:', int(seed))
        self.randomized = True

    def randomize(self, seed):
        """
        Randomizes the order of the characters
        """
        if self.DEBUG:
            time = Time.time()
        np.random.seed(seed)
        self.numbers = [i for i in range(256)]
        np.random.shuffle(self.numbers)
        for i in range(len(self.numbers)):
            self.mapped_ints[self.numbers[i]] = i

        np.random.seed(seed)
        self.chars = self.chars_original.copy()
        np.random.shuffle(self.chars)
        for i in range(len(self.chars)):
            self.char_index[self.chars[i]] = i 
        
        if self.DEBUG:
            print('Time to randomize:', Time.time()-time)


    def get_dimensions(self, length):
        """
        Calculates the dimensions of the image based on the length of the text
        """
        sqrt = length**0.5
        if round(sqrt)**2 < length:
            width = round(sqrt)+1
            height = round(sqrt)
        else:
            width = round(sqrt)
            height = round(sqrt)
        return width, height
    
    def get_rgb(self, int1, int2, int3):
        """
        Returns the RGB values based on the mapped integers
        """
        
        r = self.numbers[int1]
        g = self.numbers[int2]
        b = self.numbers[int3]
        return r, g, b
    def get_char_rgb(self, a, b, c):
        """
        Returns the RGB values based on the mapped integers
        """
        r = self.char_index[a]
        g = self.char_index[b]
        b = self.char_index[c]
        
        return self.get_rgb(r, g, b)
    
    def get_char(self, r, g, b):
        """
        Returns the character based on the RGB values
        """
        int1, int2, int3 = self.get_ints(r, g, b)
        return self.chars[int1] + self.chars[int2] + self.chars[int3]


    def get_ints(self, r, g, b):
        """
        Returns the mapped integers based on the RGB values
        """
        int1 = self.mapped_ints[r]
        int2 = self.mapped_ints[g]
        int3 = self.mapped_ints[b]
        return int1, int2, int3
    
    def encrypt(self, file_path = None, data = None):
        if self.randomized == False:
            self.randomize(self.seed)
        if data is None and file_path is None:
            print('No data given')
            return
        if data is None:
            data, file_path = upload_file(file_path)
        
        filetype = file_path.split('.')[-1]
        extencion_pixel_count = len(filetype) // 3
        if len(filetype) % 3 != 0:
            extencion_pixel_count += 1

        length = len(data)//3 + 1 + extencion_pixel_count
        if len(data) % 3 != 0:
            length += 1
        width, height = self.get_dimensions(length)
        print('length:', length, end=' ')
        print('width:', width, end=' ')
        print('height:', height)

        bytes = []
        for byte in data:
            bytes.append(byte)
        
        image = Image.new('RGB', (width, height))
        pixels = image.load()

        w_index = 0
        for h_index in range(extencion_pixel_count+1):
            if h_index == 0:
                r, g, b = extencion_pixel_count, 0, 0
            else:
                r_char, g_char, b_char = ' ', ' ', ' '
                if h_index*3-3 < len(filetype):
                    r_char = filetype[h_index*3-3]
                if h_index*3-2 < len(filetype):
                    g_char = filetype[h_index*3-2]
                if h_index*3-1 < len(filetype):
                    b_char = filetype[h_index*3-1]
                r, g, b = self.get_char_rgb(r_char, g_char, b_char)
            if h_index >= height:
                h_index = 0
                w_index += 1
            pixels[w_index, h_index] = (r, g, b)
        index = 0
        for i in range(width):
            for j in range(height):
                if (i < w_index or (i==w_index and j <= h_index)):
                    print('continue')
                    continue
                if index < len(bytes):  
                    r = bytes[index]
                    g, b = 0, 0
                    if index +1 < len(bytes):
                        g = bytes[index+1]
                    if index + 2 < len(bytes):
                        b = bytes[index+2]

                    r, g, b = self.get_rgb(r,g,b)
                    index += 3
                else:
                    r, g, b = self.get_rgb(0, 0, 0)
                pixels[i, j] = (r, g, b)
        return image

            
    def decrypt(self, img):
        if self.randomized == False:
            self.randomize(self.seed)

        pixels = img.load()
        width, height = img.size
        extencion_pixel_count = pixels[0, 0][0]
        extencion = ''

        w_index = 0
        for h_index in range(1, extencion_pixel_count+1):
            if h_index >= height:
                h_index = 0
                w_index += 1
            r, g, b = pixels[w_index, h_index]
            extencion += self.get_char(r, g, b)
        data = []
        for i in range(width):
            for j in range(height):
                if (i < w_index or (i==w_index and j <= h_index)):
                    continue
                r, g, b = pixels[i, j]
                r, g, b = self.get_ints(r, g, b)
                data.append(r)
                data.append(g)
                data.append(b)
        return bytes(data), extencion

    
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
                    print('Usage: python File_Image_Translator.py encrypt <in_filename> <out_filename> [seed](optional)')
                    print('Encrypts a file into an image, and saves it as a file with the given image filename')
                    print('If seed is not given, a default seed will be used')
                elif help_command == 'decrypt':
                    print('Usage: python File_Image_Translator.py decrypt <in_filename> <out_filename> [seed](optional)')
                    print('Decrypts an image into a file, and saves the file')
                    print('If seed is not given, a default seed will be used')
                else:
                    print('Invalid command')
                    sys.exit(1)
            else:
                print('Commands:')
                print('encrypt <in_filename> <out_filename> [seed](optional)')
                print('decrypt <in_filename> <out_filename> [seed](optional)\n')
                print('type "python File_Image_Translator.py help <command>" for more info on a specific command')
    def encrypt(*args):
        print(args)
        translator = File_Image_Translator(DEBUG=True)
        
        if len(args) < 4:
            print('Usage: python File_Image_Translator.py encrypt <in_filename> <out_filename> [seed](optional)')
            sys.exit(1)
        in_path = args[2]
        out_path = args[3]
        if len(args) == 5:
            seed = int(args[4])
            translator.set_seed(seed)
        image = translator.encrypt(in_path)
        save_image_file(image, out_path)
    def decrypt(*args):
        translator = File_Image_Translator(DEBUG=True)

        if len(sys.argv) < 4:
            print('Usage: python Text_Image_Translator.py decrypt <filename> [seed](optional)')
            sys.exit(1)
        in_path = sys.argv[2]
        out_path = sys.argv[3]
        if len(sys.argv) == 5:
            seed = int(sys.argv[4])
            translator.set_seed(seed)
        image = upload_image_file(in_path)
        data, extencion = translator.decrypt(image)
        if '.' in out_path:
            out_path = out_path.split('.')
            out_path.remove(out_path[-1])
            out_path = '.'.join(out_path)
        out_path += '.' + extencion
        with open(out_path, 'wb') as file:
            file.write(data)
    
    import sys

    if len(sys.argv) < 2:
        print('Usage: python File_Image_Translator.py <command> <args>')
        print('Type "python File_Image_Translator.py help" for more info')
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

