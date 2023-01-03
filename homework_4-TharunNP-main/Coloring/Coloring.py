import numpy as np
import cv2 #testing
import random
class Coloring:

    def intensity_slicing(self, image, n_slices):
        '''
       Convert greyscale image to color image using color slicing technique.
       takes as input:
       image: the grayscale input image
       n_slices: number of slices
        
       Steps:
 
        1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
        2. Randomly assign a color to each interval
        3. Create and output color image
        4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
 
       returns colored image
       '''
        tslices = n_slices + 1
        new_img = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

        red = [0] * tslices
        green = [0] * tslices
        blue = [0] * tslices

        for i in range(1, tslices):
            red[i] = random.randrange(256)
            green[i] = random.randrange(256)
            blue[i] = random.randrange(256)

        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                spots = int(image[i][j] / (256 / tslices))
                new_img[i][j] = [red[spots], green[spots], blue[spots]]

        return new_img

    def color_transformation(self, image, n_slices, theta):
        '''
        Convert greyscale image to color image using color transformation technique.
        takes as input:
        image:  grayscale input image
        colors: color array containing RGB values
        theta: (phase_red, phase,_green, phase_blue) a tuple with phase values for (r, g, b) 
        Steps:
  
         1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
         2. create red values for each slice using 255*sin(slice + theta[0])
            similarly create green and blue using 255*sin(slice + theta[1]), 255*sin(slice + theta[2])
         3. Create and output color image
         4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
  
        returns colored image
        '''
        tslices = n_slices + 1
        new_img = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        pi = 3.14

        red = [0] * tslices
        green = [0] * tslices
        blue = [0] * tslices

        for i in range(1, tslices):
            red[i] = 255 * np.sin(i + (theta[0] * pi / 180))
            green[i] = 255 * np.sin(i + (theta[1] * pi / 180))
            blue[i] = 255 * np.sin(i + (theta[2] * pi / 180))

        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                spots = int(image[i][j] / (256 / tslices))
                new_img[i][j] = [red[spots], green[spots], blue[spots]]

        return new_img



        

