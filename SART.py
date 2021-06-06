import numpy as np
import pandas as pd
from skimage.transform import iradon_sart
import matplotlib.pyplot as plt
"""
2nd attempt at making the reconstruction code. This time using SART

Do not use, only for documenting the process.
"""
def slicer2( ang, slicepoint, iter ):
    v0 = pd.read_csv('256px_flames/FL-90_256.csv').to_numpy()
    v1 = pd.read_csv('256px_flames/FL-84_256.csv').to_numpy()
    v2 = pd.read_csv('256px_flames/FL-78_256.csv').to_numpy()
    v3 = pd.read_csv('256px_flames/FL-72_256.csv').to_numpy()
    v4 = pd.read_csv('256px_flames/FL-66_256.csv').to_numpy()
    v5 = pd.read_csv('256px_flames/FL-60_256.csv').to_numpy()
    v6 = pd.read_csv('256px_flames/FL-54_256.csv').to_numpy()
    v7 = pd.read_csv('256px_flames/FL-48_256.csv').to_numpy()
    v8 = pd.read_csv('256px_flames/FL-42_256.csv').to_numpy()
    v9 = pd.read_csv('256px_flames/FL-36_256.csv').to_numpy()
    v10 = pd.read_csv('256px_flames/FL-30_256.csv').to_numpy()
    v11 = pd.read_csv('256px_flames/FL-24_256.csv').to_numpy()
    v12 = pd.read_csv('256px_flames/FL-18_256.csv').to_numpy()
    v13 = pd.read_csv('256px_flames/FL-12_256.csv').to_numpy()
    v14 = pd.read_csv('256px_flames/FL-6_256.csv').to_numpy()
    v15 = pd.read_csv('256px_flames/FL0_256.csv').to_numpy()
    v16 = pd.read_csv('256px_flames/FL6_256.csv').to_numpy()
    v17 = pd.read_csv('256px_flames/FL12_256.csv').to_numpy()
    v18 = pd.read_csv('256px_flames/FL18_256.csv').to_numpy()
    v19 = pd.read_csv('256px_flames/FL24_256.csv').to_numpy()
    v20 = pd.read_csv('256px_flames/FL30_256.csv').to_numpy()
    v21 = pd.read_csv('256px_flames/FL36_256.csv').to_numpy()
    v22 = pd.read_csv('256px_flames/FL42_256.csv').to_numpy()
    v23 = pd.read_csv('256px_flames/FL48_256.csv').to_numpy()
    v24 = pd.read_csv('256px_flames/FL54_256.csv').to_numpy()
    v25 = pd.read_csv('256px_flames/FL60_256.csv').to_numpy()
    nviews = 26


    theta = np.linspace(-90, -90 + ang, nviews + 1)
    theta = theta[:-1]

    i = int(slicepoint*174)
    b = np.array([v0[i, :], v1[i, :], v2[i, :], v3[i, :], v4[i, :], v5[i, :],v6[i, :], v7[i, :], v8[i, :], v9[i, :], v10[i, :], v11[i, :], \
                v12[i, :], v13[i, :], v14[i, :], v15[i, :], v16[i, :], v17[i, :],v18[i, :], v19[i, :], v20[i, :], v21[i, :], v22[i, :], v23[i, :], \
                v24[i, :], v25[i, :]])
    sinogram = b.transpose()
    print(sinogram.shape)
    x_init = iradon_sart(sinogram, theta=theta)

    x = iradon_sart(sinogram, theta=theta, image= x_init)
    if iter >0:
        for i in range(iter):
            x = iradon_sart(sinogram, theta=theta, image=x_init)
            x_init = x


    x[x<0]= 0
    plt.imshow(x, cmap='viridis')
    plt.colorbar()
    plt.show()
    return x
iterations = [0,1,2,3,4,5, 100]
maximum = []
sums = []
for i in range(6):
    y = slicer2( 156, 0.6, i)
    maximum.append(np.max(y))
    sums.append(np.sum(y))

z = slicer2( 156, 0.6, 100)
maximum.append(np.max(z))
sums.append(np.sum(z))
plt.imshow(z, cmap='viridis')
plt.colorbar()
plt.show()
fig , axs = plt.subplots(2,1)
axs[0].plot(iterations, maximum)
axs[1].plot(iterations, sums)
plt.show()




