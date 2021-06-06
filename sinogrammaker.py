import os
import numpy as np
import pandas as pd

def getdimension(code1, code2, theta, path):
    """

    :param code1: Name of the csv file before angle. E.g.: for 'flame6view.csv', 'flame'
    :param code2: Name of the csv file after angle. E.g.: for 'flame6view.csv', 'view.csv'
    :param theta: array of values of the angle of each view used for the reconstruction
    :param path: Path to the folder where the images are found
    :return: dimension of the images
    """
    name = code1 + str(int(theta[0])) + code2

    line = path.split('/')
    folder = line[-1]
    fullname = folder + '/' + name
    for root, dirs, files in os.walk(path):
        if name in files:
            v = pd.read_csv(fullname).to_numpy()
            return v.shape

def find(code1, code2, theta, path ):
    """

        :param code1: Name of the csv file before angle. E.g.: for 'flame6view.csv', 'flame'
        :param code2: Name of the csv file after angle. E.g.: for 'flame6view.csv', 'view.csv'
        :param theta: array of values of the angle of each view used for the reconstruction
        :param path: Path to the folder where the images are found
        :return: Dictionary containing all the 2D matrices of each selected image.
        """
    d = {}

    for root, dirs, files in os.walk(path):

        for angle in theta:

            name = code1 + str(int(angle)) + code2
            line = path.split('/')
            folder = line[-1]
            fullname = folder + '/' + name
            if name in files:

                d["v{0}".format(int(angle))] = pd.read_csv(fullname).to_numpy()

            else:
                pass
    return d

def sinogram( depth, d):
    """

    :param depth: Float from 0 to 1: height or depth at which the cut is made: E.g. for 200px tall images,
     0.5 would mean the slice is at the plane of the 100th pixel
    :param d: dictonary containing all the 2D matrices of each image.
    :return: 2D matrix. Sinogram made using the arrays of the images of the selected angles.
    """
    i = 0
    b = np.array([])
    for arr in d:
        if i == 0:
            b = np.hstack((b, d[arr][depth, :]))
        else:
            b = np.vstack((b, d[arr][depth, :]))
        i = i + 1
    sinogram = b.transpose()
    return sinogram

