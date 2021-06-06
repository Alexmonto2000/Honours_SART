import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def binner(a, n_averaged_elements):
    """
    :param a: 2D numpy array of the desired image to be binned
    :param n_averaged_elements: How many elements are to be averaged into one. E.g.:  if from a 2048px image you want a 512 px image, n = 4.
    :return: 2D numpy array of the binned image.
    """
    final = np.array([])
    inter = np.array([])
    print(a.shape)
    for j in range(a.shape[0]):
        line = []
        for i in range(0, len(a[j,:]), n_averaged_elements):
            slice_from_index = i
            slice_to_index = slice_from_index + n_averaged_elements
            line.append(np.mean(a[j,:][slice_from_index:slice_to_index]))
        if j == 0:
            inter = np.hstack((inter, line ))
        else:
            inter = np.vstack((inter, line ))
    for k in range(inter.shape[1]):
        line = []
        for i in range(0, len(inter[:, k]), n_averaged_elements):
            slice_from_index = i
            slice_to_index = slice_from_index + n_averaged_elements

            line.append(np.mean(inter[:, k][slice_from_index:slice_to_index]))
        if k == 0:
            final = np.hstack((final, line))
        else:
            final = np.vstack((final, line))
    final = final.transpose()
    print(final.shape)
    return final
#array = np.array([[ 2,  2,  2,  8,  9, 10],[ 2,  2,  2,  8,  9, 10],[ 2,  2,  2,  8,  9, 10],[ 3,  3,  3,  8,  9, 10],[ 3,  3,  3,  8,  9, 10]])

fig , axs = plt.subplots(4, 4)

df = pd.read_csv('2048px_flames/FL60_2048.csv')
array = df.to_numpy()
final = binner(array,8)

np.savetxt("FL60_256.csv", final, delimiter=",")