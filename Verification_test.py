from SART_OP import sart
from sinogrammaker import getdimension
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
"""
File created specially for the verification test shown in the report.
"""
def reconstruction_test(angmin, angmax, deltaang, orientation, code1, code2, path, ratio, iter):
    """

    :param angmin: Angle of view of the first mage used for the reconstruction
    :param angmax: Angle of view of the last image used for the reconstruction
    :param deltaang: Difference in angle between views
    :param orientation: axis to which the plane of the desired slice is perpendicular. Options: 'x', 'y' or 'z'.
    :param code1: Name of the csv file before angle. E.g.: for 'flame6view.csv', 'flame'
    :param code2: Name of the csv file after angle. E.g.: for 'flame6view.csv', 'view.csv'
    :param path: Path to the folder where the images are found
    :param ratio: Ratio of new pixels/ original pixels. E.g.: if the 512px images ae used: 512/2048 = 0.25.
    :param iter: Number of SART iterations to be used for the reconstruction
    :return: 2D matrix. Reconstruction of -90 deg view original image using SART
    """
    theta = np.arange(angmin, angmax + deltaang, deltaang)
    pixels = getdimension(code1, code2, theta, path)
    slicepoints = np.linspace(0,pixels[0]-1, pixels[0])*(1/pixels[0])
    y = np.array([])
    for number in slicepoints: # Use SART at all pixel planes
        x = sart(angmin, angmax, deltaang, orientation, number, code1, code2, path, ratio, iter)
        xi = np.sum(x, axis=1).tolist() #Sum all columns of the matrix to make a list
        xi = np.array(xi)
        x1 = xi * (1/ratio) #Multiply result by the relevant ratio to correct for different resolutions
        if number == 0:
            y = np.hstack((y, x1))
        else:
            y = np.vstack((y, x1))  # Create image layer by layer

    return y

y = reconstruction_test(-90, 60, 6, 'z', 'FL','_256.csv', 'C:/Users/alexm/PycharmProjects/HonoursPy/256px_flames', 0.25,5)

#Reconstruction
im1 = plt.imshow(y, cmap='viridis', vmin=0, vmax=1000)
plt.colorbar(im1, label = "Photons per pixel")
plt.show()
#Original
df1 = pd.read_csv('256px_flames/FL-90_256.csv')
array1 = df1.to_numpy()
im = plt.imshow(array1, cmap='viridis', vmin=0, vmax=1000)
plt.colorbar(im, label = "Photons per pixel")
plt.show()
#Error
e = np.subtract(y,df1)

error= plt.imshow(e, cmap = 'bwr', vmin=-300, vmax=300)
plt.colorbar(error, label = " Error in Photons per pixel")
plt.show()

#Error vs Iterations
print(np.average(np.abs(e)))

"""
The error for each number of iterations was found and hard coded below to create the graph
"""

iterations = [1,2,3,4,5,6,7,8,9,10]
lst =[36.903, 36.578, 36.429, 36.342, 36.291, 36.259, 36.237,36.223, 36.213, 36.207]
plt.plot(iterations,lst)
plt.xlabel("Iteration")
plt.ylabel("Average absolute error [Photons/pixel]")
plt.ylim(35.5,37.5)
plt.show()

