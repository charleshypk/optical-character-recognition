#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class Letter(object):

    IMAGE_SIZE = 255.0
    
    def __init__(self, font, letter):
        self.file_name = 'img/' + font + '/' + letter + '.jpg'
        self.font = font
        self.letter = letter
        self.dct = self.setup()

    def get_normalized_intensity_matrix(self):
        img = cv2.imread(self.file_name, 0)
        normalized_img = np.float32(img) / Letter.IMAGE_SIZE

        return normalized_img

    def setup(self):
        normalized_img = self.get_normalized_intensity_matrix()
        dct = cv2.dct(normalized_img)

        return dct

    def __str__(self):
        return self.font + ' ' + self.letter


def compress(input_data, compression):
    dct = input_data.dct[:]

    for m in range(int(input_data.IMAGE_SIZE) + 1):
        for n in range(int(input_data.IMAGE_SIZE) + 1):
            if (m >= compression) or (n >= compression):
                dct[m][n] = 0

    compressed_img = cv2.idct(dct)

    return compressed_img

def show_compressed_image(input_data, compression=32):
    compressed_img = compress(input_data, compression)

    cv2.imshow(str(input_data), compressed_img)
    cv2.waitKey(0)

def save_compressed_image(input_data, compression=32):
    compressed_img = compress(input_data, compression)
    converted_img = np.float32(compressed_img) * 255.0

    cv2.imwrite('img/Compressed/' +  input_data.font + '_' +
                input_data.letter + '.jpg', converted_img)


if __name__ == '__main__':
    arial_b = Letter('Arial', 'b')

    show_compressed_image(arial_b, compression=16)
    save_compressed_image(arial_b, compression=16)
