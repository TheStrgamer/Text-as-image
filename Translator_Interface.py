import tkinter as tk
from Text_Image_Translator import Text_Image_Translator
from File_Handler import save_file, upload_file
from PIL import Image, ImageTk
import customtkinter

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue") 

class TranslatorInterface(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('Text Image Translator')

        self.width = 650
        self.height = 500
        self.geometry(f"{self.width}x{self.height}")

        self.translator = Text_Image_Translator(DEBUG=False)
        
        self.pages = {}
        self.show_main_page()
        self.mainloop()

    def switch_page(self, page_class):
        new_frame = page_class(self)
        if self.pages:
            for page in self.pages.values():
                page.pack_forget()
        self.pages[page_class] = new_frame
        new_frame.pack(fill="both", expand=True)
        

    def show_main_page(self):
        main_frame = IndexPage(self)
        main_frame.pack(fill="both", expand=True)
        self.pages[IndexPage] = main_frame


class IndexPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = customtkinter.CTkLabel(self, text="Text to image encrypter", font=("Arial", 24))
        self.label.pack(pady=20)

        self.page1_button = customtkinter.CTkButton(self, text="Encrypt", command=lambda: master.switch_page(EncryptPage))
        self.page1_button.pack(pady=10)

        self.page2_button = customtkinter.CTkButton(self, text="Decrypt", command=lambda: master.switch_page(DecryptPage))
        self.page2_button.pack(pady=10)

        self.quit_button = customtkinter.CTkButton(self, text="Quit", command=self.quit)
        self.quit_button.pack(pady=10)

class EncryptPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.translator = master.translator
        self.title = customtkinter.CTkLabel(self, text="Encrypt", font=("Arial", 24))
        self.title.pack(pady=10)

        self.title = customtkinter.CTkLabel(self, text="Type text to encrypt", font=("Arial", 12))
        self.title.pack(pady=0)
        self.text_entry = customtkinter.CTkTextbox(self, width=600, height=150)
        self.text_entry.pack(pady=5)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=5)

        self.seed_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Enter a seed (optional)", width=150)
        self.seed_entry.pack(padx=5, side="left")

        self.submit_button = customtkinter.CTkButton(self.frame, text="Encrypt", command=self.on_submit)
        self.submit_button.pack(padx=5, side="left")

        self.save_button = customtkinter.CTkButton(self.frame, text="Save", command=lambda: save_file(self.translated_image), state="disabled")
        self.save_button.pack(padx=5, side="left")

        self.back_button = customtkinter.CTkButton(self, text="Return", command=lambda: master.switch_page(IndexPage))
        self.back_button.place(x=10, y=10, anchor="nw")
        
        self.image = customtkinter.CTkLabel(self, text="")
        self.image.pack(pady=20)

    def on_submit(self):
        self.save_button.configure(state="normal")
        text = self.text_entry.get("1.0", "end-1c")
        seed = self.seed_entry.get()
        self.translator.set_seed(seed)
        self.translated_image = self.translator.encrypt(text)
        self.display_image(self.translated_image)

    def display_image(self, img=None):    
        try:
            if not img:
                img = customtkinter.CTkImage(Image.open("example.png"), size=(200, 200))
            else:
                img = img.resize((200, 200), Image.NEAREST)
                img = customtkinter.CTkImage(img, size=(200, 200))

            self.image.configure(image=img)
            self.image.image = img
        except Exception as e:
            self.image.configure(text=f"Error loading image: {e}")
    
    def save_image(self):
        save_file(self.translated_image)

class DecryptPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.title = customtkinter.CTkLabel(self, text="Decrypt", font=("Arial", 24))
        self.title.pack(pady=20)

        self.image = customtkinter.CTkLabel(self, text="")
        self.image.pack(pady=20)

        self.display_image()

        self.back_button = customtkinter.CTkButton(self, text="Back to Main", command=lambda: master.switch_page(IndexPage))
        self.back_button.pack(pady=10)

    def display_image(self, img=None):    
        try:
            if not img:
                img = customtkinter.CTkImage(Image.open("example.png"), size=(200, 200))
            else:
                img = customtkinter.CTkImage(img, size=(200, 200))

            self.image.configure(image=img)
            self.image.image = img
        except Exception as e:
            self.image.configure(text=f"Error loading image: {e}")
  

if __name__ == '__main__':
    TranslatorInterface()


    






