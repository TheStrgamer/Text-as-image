from tkinter import filedialog
from PIL import Image

def save_file(image, path = None):
    """
    Saves the given image to the given path
    Opens a file dialog if no path is given
    """
    if path is None:
        path = filedialog.asksaveasfilename(defaultextension=".png")
    if image is None or type(image) is not Image.Image:
        raise ValueError('Invalid image')
    image.save(path)

def upload_file(filename = None):
    """
    Opens the given file and returns the image
    Opens a file dialog if no filename is given
    """
    if filename is None:
        f_types = [('PNG Files', '*.png')]
        filename = filedialog.askopenfilename(filetypes=f_types)
    return Image.open(filename)
