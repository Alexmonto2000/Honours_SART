import pandas as pd
import numpy as np
"""
Small code to substract the background from the original images
"""
df = pd.read_csv('flame-90_1.csv')
arr = df.to_numpy()
bk = pd.read_csv('background.csv')
bg = bk.to_numpy()

arr1 = arr - bg

np.savetxt("FL-90_2048.csv", arr1, delimiter=",")