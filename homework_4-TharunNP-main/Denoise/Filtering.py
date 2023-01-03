import numpy as np
import cv2 # testing

class Filtering:

    def __init__(self, image, filter_name, filter_size, var = None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        global_var: noise variance to be used in the Local noise reduction filter
        S_max: Maximum allowed size of the window that is used in adaptive median filter
        """

        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size
        self.global_var = var
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""
        mean = sum(roi) / len(roi)

        return mean

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""
        gm = 1
        for index in range(len(roi)):
            gm = gm * roi[index]
        g_mean = pow(gm, (1.0 / len(roi)))

        return g_mean

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""
        mean1 = self.get_arithmetic_mean(roi)
        var = 0

        for x in range(len(roi)):
            var += pow(roi[x] - mean1, 2)
        var /= len(roi) - 1

        roi.sort()

        if len(roi) % 2 == 1:
            index = (len(roi) + 1) / 2
            g = roi[int(index)]
        else:
            g = roi[int(len(roi) / 2)] + roi[int((len(roi) + 1) / 2)]
            g /= 2

        variance_frac = self.global_var / var
        adjustment = g - mean1
        n_value = g - (variance_frac * adjustment)

        return n_value

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi"""
        roi.sort()
        median = roi[len(roi) // 2]

        return median

    def get_adaptive_median(self, roi):
        """Use this function to implment the adaptive median.
        It is left up to the student to define the input to this function and call it as needed. Feel free to create
        additional functions as needed.
        """

    def filtering(self):
        """performs filtering on an image containing gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernal and apply a mathematical
        operation for all the elements with in the kernel. For example, mean, median and etc.

        Steps:
        1. add the necesssary zero padding to the noisy image, that way we have sufficient values to perform the operati
        ons on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the ouput image.
        5. return the output image

        Note: You can create extra functions as needed. For example if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """
        pad = int(self.filter_size / 2)
        pad_img = np.zeros((len(self.image) + pad * 2, len(self.image) + pad * 2))   # for the padding
        new_img = np.zeros((len(self.image), len(self.image[0])))

        for x in range(1, len(self.image)):
            for y in range(1, len(self.image[0])):
                pad_img[x, y] = self.image[x, y]
        count_x = -1
        for i in range(pad, len(pad_img) - pad):
            count_x = count_x + 1
            count_y = -1
            for j in range(pad, len(pad_img[0]) - pad):
                count_y = count_y + 1
                roi = []
                for x in range(i - pad, i + pad):
                    for y in range(j - pad, j + pad):
                        roi.append(pad_img[x, y])
                new_img[count_x, count_y] = self.filter(roi)

        return new_img