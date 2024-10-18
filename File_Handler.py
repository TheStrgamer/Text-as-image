from tkinter import filedialog
from PIL import Image

def save_image_file(image, path = None):
    """
    Saves the given image to the given path
    Opens a file dialog if no path is given
    """
    if path is None:
        path = filedialog.asksaveasfilename(defaultextension=".png")
    if image is None or type(image) is not Image.Image:
        raise ValueError('Invalid image')
    image.save(path)

def upload_image_file(filename = None):
    """
    Opens the given file and returns the image
    Opens a file dialog if no filename is given
    """
    if filename is None:
        f_types = [('PNG Files', '*.png')]
        filename = filedialog.askopenfilename(filetypes=f_types)
    return Image.open(filename)

def save_file(data, path = None, extension = None): 
    """
    Saves the given data to the given path
    Opens a file dialog if no path is given
    """
    if path is None:
        if extension is not None:
            path = filedialog.asksaveasfilename(defaultextension=extension)
        else:
            path = filedialog.asksaveasfilename()
    with open(path, 'wb') as file:
        file.write(data)
def upload_file(filename = None):
    """
    Opens the given file and returns the data
    Opens a file dialog if no filename is given
    """
    if filename is None:
        filename = filedialog.askopenfilename()
    filename_trimmed = filename.split('/')[-1]
    with open(filename, 'rb') as file:
        return file.read(), filename_trimmed
