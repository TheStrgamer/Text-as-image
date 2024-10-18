from Text_Image_Translator import Text_Image_Translator
from File_Image_Translator import File_Image_Translator
import customtkinter

from Pages import IndexPage, EncryptPage, DecryptPage

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue") 

class TranslatorInterface(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.translator = Text_Image_Translator(DEBUG=True)
        self.file_translator = File_Image_Translator(DEBUG=True)


        self.title('Text Image Translator')

        self.width = 650
        self.height = 510
        self.geometry(f"{self.width}x{self.height}")

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


if __name__ == '__main__':
    TranslatorInterface()


    






