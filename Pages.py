import customtkinter
from File_Handler import save_image_file, upload_image_file, save_file, upload_file
from PIL import Image



class IndexPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = customtkinter.CTkLabel(self, text="Text to image encrypter", font=("Arial", 24))
        self.label.pack(pady=20)

        self.page1_button = customtkinter.CTkButton(self, text="Encrypt", command=lambda: master.switch_page(EncryptPage))
        self.page1_button.pack(pady=10)

        self.page2_button = customtkinter.CTkButton(self, text="Decrypt", command=lambda: master.switch_page(DecryptPage))
        self.page2_button.pack(pady=10)

        self.page3_button = customtkinter.CTkButton(self, text="Encrypt File", command=lambda: master.switch_page(EncryptFilePage))
        self.page3_button.pack(pady=10)

        self.page4_button = customtkinter.CTkButton(self, text="Decrypt File", command=lambda: master.switch_page(DecryptFilePage))
        self.page4_button.pack(pady=10)

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

        self.save_button = customtkinter.CTkButton(self.frame, text="Save", command=lambda: save_image_file(self.translated_image), state="disabled")
        self.save_button.pack(padx=5, side="left")

        self.back_button = customtkinter.CTkButton(self, text="Return", command=lambda: master.switch_page(IndexPage))
        self.back_button.place(x=10, y=10, anchor="nw")
        
        self.image = customtkinter.CTkLabel(self, text="")
        self.image.pack(pady=20)

    def on_submit(self):
        self.save_button.configure(state="normal")
        text = self.text_entry.get("1.0", "end-1c")
        seed = self.seed_entry.get()
        seed = seed.strip()

        if seed != "":
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
        save_image_file(self.translated_image)

class DecryptPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.translator = master.translator

        self.title = customtkinter.CTkLabel(self, text="Decrypt", font=("Arial", 24))
        self.title.pack(pady=10)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=5)

        self.seed_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Enter a seed (optional)", width=150)
        self.seed_entry.pack(padx=5, side="left")

        self.load_button = customtkinter.CTkButton(self.frame, text="Load image", command=self.load_image)
        self.load_button.pack(padx=5, side="left")

        self.decrypt_button = customtkinter.CTkButton(self.frame, text="Decrypt", command=self.decrypt, state="disabled")
        self.decrypt_button.pack(padx=5, side="left")

        self.back_button = customtkinter.CTkButton(self, text="Return", command=lambda: master.switch_page(IndexPage))
        self.back_button.place(x=10, y=10, anchor="nw")
        
        self.image = customtkinter.CTkLabel(self, text="")
        self.image.pack(pady=20)

        self.text_entry = customtkinter.CTkTextbox(self, width=600, height=150, state="disabled")
        self.text_entry.pack(pady=5)

    def display_image(self, image=None):    
        try:
            if not image:
                img = customtkinter.CTkImage(Image.open("example.png"), size=(200, 200))
            else:
                img = image
                img = img.resize((200, 200), Image.NEAREST)
                img = customtkinter.CTkImage(img, size=(200, 200))

            self.image.configure(image=img)
            self.image.image = img
        except Exception as e:
            self.image.configure(text=f"Error loading image: {e}")
    def load_image(self):
        self.image_file = upload_image_file()
        self.display_image(self.image_file)
        self.decrypt_button.configure(state="normal")

    def fill_text_entry(self):
        print(self.text)
        self.text_entry.configure(state="normal")
        self.text_entry.delete("1.0", "end")
        self.text_entry.insert("1.0", self.text)
        self.text = ""
        self.text_entry.configure(state="disabled")

    def decrypt(self):
        try:
            seed = self.seed_entry.get()
            seed = seed.strip()
            if seed != "":
                self.translator.set_seed(seed)
            self.text = self.translator.decrypt(self.image_file)
            self.fill_text_entry()
        except UnicodeEncodeError:
            self.text_entry.configure(state="normal")
            self.text_entry.delete("1.0", "end")
            self.text_entry.insert("1.0", "Error: Image with binary data cannot be decrypted as text\n Try the decrypt file option on the main menu")
            self.text_entry.configure(state="disabled")
  

  
class EncryptFilePage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.translator = master.file_translator
        self.title = customtkinter.CTkLabel(self, text="Encrypt File", font=("Arial", 24))
        self.title.pack(pady=10)

        self.title = customtkinter.CTkLabel(self, text="Upload a file to encrypt", font=("Arial", 12))
        self.title.pack(pady=0)

        self.upload_frame = customtkinter.CTkFrame(self)
        self.upload_frame.pack(pady=5)

        self.upload_button = customtkinter.CTkButton(self.upload_frame, text="Upload file", command=self.upload_file)
        self.upload_button.pack(padx=5)

        self.file_name_label = customtkinter.CTkLabel(self.upload_frame, text="")
        self.file_name_label.pack(padx=5)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=5)

        self.seed_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Enter a seed (optional)", width=150)
        self.seed_entry.pack(padx=5, side="left")
        
        self.submit_button = customtkinter.CTkButton(self.frame, text="Encrypt", command=self.on_submit)
        self.submit_button.pack(padx=5, side="left")

        self.save_button = customtkinter.CTkButton(self.frame, text="Save", command=lambda: save_image_file(self.translated_image), state="disabled")
        self.save_button.pack(padx=5, side="left")

        self.back_button = customtkinter.CTkButton(self, text="Return", command=lambda: master.switch_page(IndexPage))
        self.back_button.place(x=10, y=10, anchor="nw")
        
        self.image = customtkinter.CTkLabel(self, text="")
        self.image.pack(pady=20)

    def upload_file(self):
        self.file, self.filename = upload_file()
        self.file_name_label.configure(text=self.filename)
        self.submit_button.configure(state="normal")
        
    def on_submit(self):
        self.save_button.configure(state="normal")
        seed = self.seed_entry.get()
        seed = seed.strip()

        if seed != "":
            self.translator.set_seed(seed)
        self.translated_image = self.translator.encrypt(data=self.file, file_path=self.filename)    
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
        save_image_file(self.translated_image)

class DecryptFilePage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.translator = master.file_translator

        self.title = customtkinter.CTkLabel(self, text="Decrypt", font=("Arial", 24))
        self.title.pack(pady=10)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=5)

        self.seed_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Enter a seed (optional)", width=150)
        self.seed_entry.pack(padx=5, side="left")

        self.load_button = customtkinter.CTkButton(self.frame, text="Load image", command=self.load_image)
        self.load_button.pack(padx=5, side="left")

        self.decrypt_button = customtkinter.CTkButton(self.frame, text="Decrypt", command=self.decrypt, state="disabled")
        self.decrypt_button.pack(padx=5, side="left")

        self.back_button = customtkinter.CTkButton(self, text="Return", command=lambda: master.switch_page(IndexPage))
        self.back_button.place(x=10, y=10, anchor="nw")
        
        self.image = customtkinter.CTkLabel(self, text="")
        self.image.pack(pady=20)

        self.save_button = customtkinter.CTkButton(self, text="Save", command=self.save_file, state="disabled")
        self.save_button.pack(pady=5)


    def display_image(self, image=None):    
        try:
            if not image:
                img = customtkinter.CTkImage(Image.open("example.png"), size=(200, 200))
            else:
                img = image
                img = img.resize((200, 200), Image.NEAREST)
                img = customtkinter.CTkImage(img, size=(200, 200))

            self.image.configure(image=img)
            self.image.image = img
        except Exception as e:
            self.image.configure(text=f"Error loading image: {e}")
    def load_image(self):
        self.image_file = upload_image_file()
        self.display_image(self.image_file)
        self.decrypt_button.configure(state="normal")

    def save_file(self):
        save_file(self.file, extension=self.extencion)


    def decrypt(self):
        try:
            seed = self.seed_entry.get()
            seed = seed.strip()
            if seed != "":
                self.translator.set_seed(seed)
            self.file, self.extencion = self.translator.decrypt(self.image_file)
            self.save_button.configure(state="normal")

        except Exception as e:
            print(e)
