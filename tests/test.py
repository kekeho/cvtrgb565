import os
import sys
import glob
import unittest

CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIRNAME + '/../')
from cvtrgb565 import ImageClass

directory = os.path.join(os.path.dirname(__file__), 'sources/*.png')
files_list = glob.glob(directory)


class TestConvert(unittest.TestCase):
    def test_convert(self):
        for file in files_list:
            binary_filename = ''.join(file.split('.')[:-1]) + '_cvt.tft'
            image = ImageClass(file)
            with open(binary_filename, 'rb') as binary_file:
                binary = binary_file.read()
                self.assertEqual(image.rgb565, binary)


if __name__ == "__main__":
    unittest.main()
