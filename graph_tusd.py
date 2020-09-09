import scipy.stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

"""%matplotlib inline -> this code line allows see the plots in a jupyter notebook"""

#df stands for data frame
def plot():
    df = pd.read_json(r'currencies_record/currencies_record.json')
    #Categoric variables
    print (df.columns)
    y = df['price'].apply(lambda x: 'precio' + str(int(x)))


    #Plot elements
    fig, ax = plt.subplots()
    ax.bar(y.value_counts().index, value_counts())



def run():
    plot()


if __name__ == '__main__':
    run()