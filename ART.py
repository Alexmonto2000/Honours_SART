import numpy as np
import pandas as pd
from skimage.transform import radon, iradon
from scipy.stats import poisson
from skimage.measure import compare_mse as mse
from skimage.measure import compare_psnr as psnr
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
from datetime import datetime
n = 6
# from https://github.com/hanyoseob/python-ART/blob/master/ART.py
"""
First attempt at creating an ART reconstruction code.

Do not use, only for documenting the process.
"""
def art(A, AT, b, x, mu, niter, bpos=True):

    ATA = AT(A(np.ones_like(x)))

    for i in range(int(niter)):
        x[np.isnan(x)] = 0
        x = x + mu*np.divide(AT(b - A(x)), ATA)
        if bpos:
            x[x < 0] = 0

    return x

def slicer(nviews,pixels, orientation, slicepoint):
    bk = pd.read_csv('background.csv')
    bg = bk.to_numpy()
    if nviews == 5:
        df0 = pd.read_csv('flame-90_1.csv')
        df1 = pd.read_csv('flame-54.csv')
        df2 = pd.read_csv('flame-18.csv')
        df3 = pd.read_csv('flame18.csv')
        df4 = pd.read_csv('flame54.csv')
        v0 = df0.to_numpy() - bg
        v1 = df1.to_numpy() - bg
        v2 = df2.to_numpy() - bg
        v3 = df3.to_numpy() - bg
        v4 = df4.to_numpy() - bg
    if nviews == 6:
        df0 = pd.read_csv('flame-90_1.csv')
        df1 = pd.read_csv('flame-60.csv')
        df2 = pd.read_csv('flame-30.csv')
        df3 = pd.read_csv('flame0.csv')
        df4 = pd.read_csv('flame30.csv')
        df5 = pd.read_csv('flame60.csv')
        v0 = df0.to_numpy() - bg
        v1 = df1.to_numpy() - bg
        v2 = df2.to_numpy() - bg
        v3 = df3.to_numpy() - bg
        v4 = df4.to_numpy() - bg
        v5 = df5.to_numpy() - bg

    theta = np.linspace(0,180,nviews+1)
    theta = theta[:-1]
    A = lambda x: radon(x, theta, circle=True).astype(np.float32)
    AT = lambda y: iradon(y, theta, circle=True, filter=None, output_size=pixels).astype(np.float32) / (np.pi / (2 * len(theta)))
    if orientation == 'z':
        i = 1399- int(slicepoint*1399)
        x0 = np.zeros((pixels, pixels))
        bpos = True
        if nviews == 6:
            b = np.array([v0[i, :], v1[i, :], v2[i, :], v3[i, :], v4[i, :], v5[i, :]])
        if nviews == 5:
            b = np.array([v0[i, :], v1[i, :], v2[i, :], v3[i, :], v4[i, :]])
        bt = b.transpose()
        x = art(A, AT, bt, x0,0.5, 100, bpos)


    if orientation == 'x':
        x = np.array([])
        print(x.shape)
        depth = int(slicepoint*2048)
        for i in range(bg.shape[0]):
            x0 = np.zeros((pixels,pixels))
            bpos = True
            if nviews == 6:
                b = np.array([v0[i,:],v1[i,:],v2[i,:],v3[i,:],v4[i,:], v5[i,:]])
            if nviews == 5:
                b = np.array([v0[i, :], v1[i, :], v2[i, :], v3[i, :], v4[i, :]])
            bt = b.transpose()
            xnew = art( A, AT, bt, x0, 20, bpos)
            if i ==0:
                x = np.hstack((x, xnew[depth,:]))
            else:
                x = np.vstack((x, xnew[depth, :]))
            print(x.shape)
    #x[x<0] = 0
    np.savetxt("foo.csv", x, delimiter=",")
    plt.imshow(x,cmap= 'viridis')
    plt.colorbar()
    plt.show()
    print(datetime.datetime.now())
slicer(6,2048, 'x', 0.8)



