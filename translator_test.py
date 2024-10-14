import unittest
import threading
import traceback
import time
import Text_Image_Translator
import PIL

TIMEOUT = 10  


class TestTranslator(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestTranslator, self).__init__(*args, **kwargs)
        self.translator = Text_Image_Translator.Text_Image_Translator(DEBUG=False)

    def run_with_timeout(self, method):
        """
        Runs the given test method with a timeout.
        If it takes longer than TIMEOUT seconds, it will print the stack trace.
        """
        def wrapper():
            try:
                method()
            except Exception as e:
                print(f"Exception in test '{method.__name__}': {str(e)}")
                traceback.print_exc()

        test_thread = threading.Thread(target=wrapper)
        test_thread.start()
        test_thread.join(TIMEOUT)

        if test_thread.is_alive():
            print(f"Test '{method.__name__}' is taking too long. Here's the current stack trace:")
            stack = traceback.format_stack()
            print("".join(stack))
            raise TimeoutError(f"Test '{method.__name__}' timed out.")


    def test_default_seed(self):
        self.run_with_timeout(self._test_default_seed)

    def _test_default_seed(self):
        self.assertEqual(self.translator.seed, 0)

    def test_set_seed(self):
        self.run_with_timeout(self._test_set_seed)

    def _test_set_seed(self):
        self.translator.set_seed(1)
        self.assertEqual(self.translator.seed, 1)

    def test_chars_original(self):
        self.run_with_timeout(self._test_chars_original)

    def _test_chars_original(self):
        for i in range(len(self.translator.chars)):
            self.assertEqual(self.translator.chars[i], self.translator.chars_original[i])

    def test_randomize_randomizes(self):
        self.run_with_timeout(self._test_randomize_randomizes)

    def _test_randomize_randomizes(self):
        testTranslator = Text_Image_Translator.Text_Image_Translator(DEBUG=False)
        testTranslator2 = Text_Image_Translator.Text_Image_Translator(DEBUG=False)
        testTranslator.randomize(1)
        self.assertNotEqual(testTranslator.chars[0], testTranslator2.chars[0])


    def test_get_rgb_returns_valid_rgb(self):
        self.run_with_timeout(self._test_get_rgb_returns_valid_rgb)

    def _test_get_rgb_returns_valid_rgb(self):
        r, g, b = self.translator.get_rgb('a')
        self.assertGreaterEqual(r, 0)
        self.assertLessEqual(r, 255)
        self.assertGreaterEqual(g, 0)
        self.assertLessEqual(g, 255)
        self.assertGreaterEqual(b, 0)
        self.assertLessEqual(b, 255)

    def test_get_rgb_returns_same_rgb(self):
        self.run_with_timeout(self._test_get_rgb_returns_same_rgb)
    def _test_get_rgb_returns_same_rgb(self):
        r,g,b = self.translator.get_rgb('a')
        r2,g2,b2 = self.translator.get_rgb('a')
        self.assertEqual(r, r2)
        self.assertEqual(g, g2)
        self.assertEqual(b, b2)

    def test_get_char_returns_valid_char(self):
        self.run_with_timeout(self._test_get_char_returns_valid_char)
    
    def _test_get_char_returns_valid_char(self):
        char = self.translator.get_char(0, 0, 0)
        self.assertIn(char, self.translator.chars)
    
    def test_get_char_returns_same_char(self):
        self.run_with_timeout(self._test_get_char_returns_same_char)
    def _test_get_char_returns_same_char(self):
        char = self.translator.get_char(0, 0, 0)
        char2 = self.translator.get_char(0, 0, 0)
        self.assertEqual(char, char2)

    
    def _test_encrypt_returns_same_image(self):
        img = self.translator.encrypt('a')
        img2 = self.translator.encrypt('a')
        self.assertEqual(img, img2)
    
    def test_encrypt_returns_same_image(self):
        self.run_with_timeout(self._test_encrypt_returns_same_image)
    def _test_encrypt_returns_different_image_with_different_text(self):
        img = self.translator.encrypt('a')
        img2 = self.translator.encrypt('b')
        self.assertNotEqual(img, img2)


    def test_decrypt_returns_text(self):
        self.run_with_timeout(self._test_decrypt_returns_text)

    def _test_decrypt_returns_text(self):
        img = self.translator.encrypt('a')
        text = self.translator.decrypt(img)
        self.assertEqual(text, 'a')
    
    def _test_decrypt_returns_same_text(self):
        img = self.translator.encrypt('a')
        text = self.translator.decrypt(img)
        text2 = self.translator.decrypt(img)
        self.assertEqual(text, text2)
    
    def test_decrypt_returns_same_text(self):
        self.run_with_timeout(self._test_decrypt_returns_same_text)
    def _test_decrypt_returns_different_text_with_different_image(self):
        img = self.translator.encrypt('a')
        img2 = self.translator.encrypt('b')
        text = self.translator.decrypt(img)
        text2 = self.translator.decrypt(img2)
        self.assertNotEqual(text, text2)
    
    def test_decrypt_returns_different_text_with_different_image(self):
        self.run_with_timeout(self._test_decrypt_returns_different_text_with_different_image)
    def _test_decrypt_returns_incorrect_text_with_different_seed(self):
        img = self.translator.encrypt('ape')

        text = self.translator.decrypt(img)
        self.assertEqual(text, 'ape')
        self.translator.randomize(1)
        text2 = self.translator.decrypt(img)
        self.assertNotEqual(text, text2)


if __name__ == '__main__':
    unittest.main()

                         

    


    


if __name__ == '__main__':
    unittest.main()
