import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def make_data_set(step=0.01):
    """
    Make a random 
    """
    x, y, label = [], [], []
    for i in np.arange(0, 4, step):
        for j in np.arange(0, 4, step):
            if ((i - 1.5)**2 + (j - 2.0)**2 < 1) or (i - 2.5)**2 + (j - 2.0)**2 <= 1:
                if ((i - 1.5)**2 + (j - 2.0)**2 < 1) and (i - 2.5)**2 + (j - 2.0)**2 <= 1:
                    z = 0
                else:
                    z = 1
            else:
                z = 0
            x.append(i)
            y.append(j)
            label.append(z)
    df = pd.DataFrame({'x':x, 'y':y, 'label':label})
    
    return df

def plot_data(df):
    ax = df[df['label'] == 0].plot(x='x', y='y', kind='scatter', marker='.', color='r', lw=0)
    df[df['label'] == 1].plot(x='x', y='y', kind='scatter', marker='+', color='b', ax=ax)
    # plt.xlim([0, 4])
    # plt.ylim([0, 4])
    # plt.axes().set_aspect('equal')
    plt.show()

    return None