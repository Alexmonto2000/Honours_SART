import numpy as np
from skimage.transform import iradon_sart
import matplotlib.pyplot as plt
from sinogrammaker import sinogram
from sinogrammaker import find
from sinogrammaker import getdimension
"""
Final version of the reconstruction code function.
"""
def sart( angmin, angmax, deltaang, orientation, slicepoint, code1, code2, path, ratio, iter):
    """

    :param angmin: : Angle of view of the first mage used for the reconstruction
    :param angmax: Angle of view of the last image used for the reconstruction
    :param deltaang: Difference in angle between views
    :param orientation: axis to which the plane of the desired slice is perpendicular. Options: 'x', 'y' or 'z'.
    :param slicepoint: Float from 0 to 1: height or depth at which the cut is made: E.g. for 200px tall images,
     0.5 would mean the slice is at the plane of the 100th pixel
    :param code1: Name of the csv file before angle. E.g.: for 'flame6view.csv', 'flame'
    :param code2: Name of the csv file after angle. E.g.: for 'flame6view.csv', 'view.csv'
    :param path: Path to the folder where the images are found
    :param ratio: Ratio of new pixels/ original pixels. E.g.: if the 512px images ae used: 512/2048 = 0.25.
    :param iter: Number of SART iterations to be used for the reconstruction
    :return: 2D matrix. Reconstruction of the light intensity of the flame at the desired plane
    """
    theta = np.arange(angmin, angmax + deltaang, deltaang) # np.array with the angle of each view in degrees.
    pixels = getdimension(code1, code2, theta, path) # Dimensions of picture in pixels
    d = find(code1, code2, theta, path) # Creating dictionary with arrays
    if orientation == 'z':
        i = int(slicepoint*pixels[0]) # Choosing plane of pixels to make slice

        si = sinogram(i, d) # Creating sinogram for reconstruction
        print(si.shape) # Printing shape of sinogram for quick check

        x_init = iradon_sart(si, theta=theta) # initial SART reconstruction

        if iter > 0: #Iterations
            for i in range(iter):
                x = iradon_sart(si, theta=theta, image=x_init)
                x_init = x
        else:
            x = x_init
    if orientation == 'x':
        x = np.array([])
        depth = int(slicepoint*pixels[1])
        for i in range(pixels[0]): # Process has to be repeated for all planes of pixels

            si = sinogram(i, d) # Creating sinogram

            x_init = iradon_sart(si, theta=theta) # SART reconstruction

            if iter > 0: # Iterate
                for i in range(iter):
                    xnew = iradon_sart(si, theta=theta, image=x_init)
                    x_init = xnew
            else:
                xnew = x_init

            if i ==0:
                x = np.hstack((x, xnew[depth,:]))  # Add line of pixels of the selected depth
            else:
                x = np.vstack((x, xnew[depth, :]))  # Add line of pixels of the selected depth
    if orientation == 'y':
        x = np.array([])

        depth = int(slicepoint * pixels[1])
        for i in range(pixels[0]):  # Process has to be repeated for all planes of pixels

            si = sinogram(i, d)  # Creating sinogram
            x_init = iradon_sart(si, theta=theta) # SART reconstruction

            if iter > 0:  # Iterate
                for i in range(iter):
                    xnew = iradon_sart(si, theta=theta, image=x_init)
                    x_init = xnew
            else:
                xnew = x_init
            if i == 0:
                x = np.hstack((x, xnew[:, depth]))  # Add line of pixels of the selected depth
            else:
                x = np.vstack((x, xnew[:, depth]))  # Add line of pixels of the selected depth
    x[x<0]= 0
    x = ratio * x
    return x

