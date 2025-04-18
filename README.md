# Text and File Image Translator

Encrypt text/files into images and decrypt them back using custom seeds.

## Features
- Text to Image conversion
- File to Image conversion
- Seed-based encryption
- GUI and CLI interfaces

## Installation
```bash
git clone https://github.com/TheStrgamer/Text-as-image.git
cd Text-as-image
pip install -r requirements.txt
```

## Usage

### GUI
```bash
py TranslatorInterface.py
``` 

### CLI 
```bash
# Text
## Encrypt
python Text_Image_Translator.py encrypt "text" output.png [seed]

## Decrypt 
python Text_Image_Translator.py decrypt input.png [seed]

# File
# Encrypt
python File_Image_Translator.py encrypt input.file output.png [seed]

# Decrypt
python File_Image_Translator.py decrypt input.png output.file [seed]
```

## Some images of usage

### File encrypted using seed 3349
![result](images/used_seed_3349.png)

### The main menu of the GUI
![main menu](images/main.png)

### The page for encrypting text
![encrypt text](images/encrypt_text.png)

### The page for decrypting text
![decrypt text](images/decrypt_text.png)

### The result of decrypting with incorrect seed
![decrypt wrong seed](images/decrypt_text_wrong_seed.png)

### The page for encrypting a file
![encrypt file](images/encrypt_file.png)

### The page for decrypting a file
![decrypt file](images/decrypt_file.png)



