import os
import glob
from PIL import Image
import numpy as np


class ImageClass():
    def __init__(self, filename: str):
        self.filename = filename
        # Load image
        self.image = np.array(Image.open(filename), dtype='float64')
        self.width, self.height = self.image.shape[:-1]
        self.convert_to_rgb565()

    def convert_to_rgb565(self):
        meta_width = self.width.to_bytes(2, byteorder='big')
        meta_height = self.height.to_bytes(2, byteorder='big')

        self.image[:, :, 0] *= (2**5-1)/(2**8-1)
        self.image[:, :, 1] *= (2**6-1)/(2**8-1)
        self.image[:, :, 2] *= (2**5-1)/(2**8-1)

        buffer = b''
        for y_line in self.image:
            for pixel in y_line:
                binary = ''
                for i, color in enumerate(pixel):
                    color_binary = bin(int(color))[2:]
                    if i == 1:
                        binary += '0'*(6-len(color_binary)) + color_binary
                    else:
                        binary += '0'*(5-len(color_binary)) + color_binary

                buffer += int(binary, 2).to_bytes(2, 'big')

        self.rgb565 = meta_width + meta_height + buffer

    def save(self):
        save_filename = ''.join(self.filename.split('.')[:-1]) + '_cvt.tft'
        with open(save_filename, 'bw') as file:
            file.write(self.rgb565)


if __name__ == "__main__":
    directory = os.path.join(os.path.dirname(__file__), 'test_images/*.png')
    files_list = glob.glob(directory)
    print(files_list[0])
    image = ImageClass(files_list[0])
    image.save()
