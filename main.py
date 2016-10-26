#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


FONTS = ['Arial', 'Times New Roman', 'Handwriting', 'Calibri']  # Remove the font that you are using as input
CHARACTERS = ['e', 'o', 't', 'w', 'm', 'x', 's']

class Letter(object):

    IMAGE_SIZE = 255.0
    
    def __init__(self, font, letter):
        self.file_name = 'img/' + font + '/' + letter + '.jpg'
        self.font = font
        self.letter = letter
        self.normalized_dct = self.setup()

    def get_normalized_intensity_matrix(self):
        img = cv2.imread(self.file_name, 0)
        normalized_img = np.float32(img) / Letter.IMAGE_SIZE

        return normalized_img

    def get_normalized_dct(self, normalized_img):
        dct = cv2.dct(normalized_img)
        normalized_dct = dct / self.compute_frobenius_norm(dct)

        return normalized_dct

    def compute_frobenius_norm(self, normalized_dct):
        frobenius_norm = 0

        for m in range(int(self.IMAGE_SIZE) + 1):
            for n in range(int(self.IMAGE_SIZE) + 1):
                frobenius_norm += abs((normalized_dct[m][n]) ** 2)

        return frobenius_norm ** 0.5

    def setup(self):
        normalized_img = self.get_normalized_intensity_matrix()
        normalized_dct = self.get_normalized_dct(normalized_img)

        return normalized_dct

    def __str__(self):
        return self.font + ' ' + self.letter


def initialize_training_set():
    training_set_keys = []
    training_set = {}

    for font in FONTS:
        for character in CHARACTERS:
            letter = Letter(font, character)
            training_set_keys.append(str(letter))
            training_set[str(letter)] = letter
            
    return training_set_keys, training_set
    
def initialize_output_results():
    output_results = {}

    for character in CHARACTERS:
        output_results[character] = 0.0

    return output_results

def compute_l1_1_norm(input_matrix, comparing_matrix, compression):
    average_distance = 0
    
    for m in range(compression):
        for n in range(compression):
            average_distance += abs(input_matrix[m][n] - comparing_matrix[m][n])
    
    average_distance = average_distance / (compression ** 2)
    
    return average_distance

def compute_nearest_neighbor(input_data, training_set, compression=32):
    output_results = initialize_output_results()
    
    print 'Comparing ' + str(input_data) + ' to:'
    print '------------------------------------------------------'
    
    for training_set_key in training_set_keys:
        input_matrix = input_data.normalized_dct
        comparing_matrix = training_set[training_set_key].normalized_dct
        
        total_distance = compute_l1_1_norm(input_matrix, comparing_matrix, compression)
        
        training_set_letter = training_set[training_set_key].letter
        output_results[training_set_letter] += total_distance

        print (total_distance, training_set_key)
        
    print 
    for character in output_results:
        print 'The total distance for character ' + character + ' is: ' + str(output_results[character])
    print 'The lowest total distance is: ' + str(min(output_results.itervalues()))
    print 'Therefore, the algorithm guesses the letter: ' + str(min(output_results.iterkeys(),
                                                                    key=lambda k: output_results[k]))
    print


if __name__ == '__main__':
    (training_set_keys, training_set) = initialize_training_set()

    arial_e = Letter('Arial', 'e')
    arial_o = Letter('Arial', 'o')
    arial_t = Letter('Arial', 't')
    arial_w = Letter('Arial', 'w')
    arial_m = Letter('Arial', 'm')
    arial_x = Letter('Arial', 'x')
    arial_s = Letter('Arial', 's')

    compute_nearest_neighbor(arial_e, training_set)
    compute_nearest_neighbor(arial_o, training_set)
    compute_nearest_neighbor(arial_t, training_set)
    compute_nearest_neighbor(arial_w, training_set)
    compute_nearest_neighbor(arial_m, training_set)
    compute_nearest_neighbor(arial_x, training_set)
    compute_nearest_neighbor(arial_s, training_set)
