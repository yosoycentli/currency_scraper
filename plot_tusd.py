import time
import scipy.stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import json
import requests
import lxml.html as html

HOME_URL1 = 'https://www.google.com/search?client=opera&hs=TXN&sxsrf=ALeKk01dEUy_DMMGnUkrjm_7PFVbF66ZQg%3A1600052456558&ei=6NxeX9_NIYattQawvoywBA&q=dolar+a+pesos&oq=dolar+a+pesos&gs_lcp=CgZwc3ktYWIQAzIECAAQQzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzICCAAyAggAMgIIADoECAAQRzoHCCMQ6gIQJzoECCMQJzoJCCMQJxBGEIICOgUIABCxA1CFaVjifGDCfmgBcAJ4AIABgAGIAbgKkgEDNi43mAEAoAEBqgEHZ3dzLXdperABCsgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjf4a3y0-frAhWGVs0KHTAfA0YQ4dUDCAw&uact=5'

#Variables del HOME_URL1
EXCHANGE_USD_PESOS = '//table[@class="qzNNJ"]/tbody/tr/td/input[@class="a61j6 vk_gy vk_sh Hg3mWc"]/@value'


def parse_exchange (url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            currency_now = response.content.decode('utf-8')
            parsed = html.fromstring(currency_now)

            try:
                actual_exchange = parsed.xpath(EXCHANGE_USD_PESOS)
            except IndexError:
                return actual_exchange
        else: 
            pass
        return actual_exchange
    except AttributeError:
                response = f'there is something wrong here'


# %matplotlib inline -> this code line allows see the plots in a jupyter notebook

#df stands for data frame
def plot():
    df = pd.read_json(r'currencies_record/currencies_record.json')
    cols = df.columns
    rows = df.id

    data = pd.read_json(r'currencies_record/currencies_record.json')
    CURRENCIES_df = pd.DataFrame(data, columns=cols[1:5], index=rows)


    #Transform the "price" column data so we can get a new "mxn" column

    CURRENCIES_df['mxn'] = CURRENCIES_df ['price'].apply(lambda n: n *(21.1203))
    CURRENCIES_df.tail()

    #Select all the values of the price column
    TUSD_df = CURRENCIES_df[(CURRENCIES_df['currency'] == "TUSD" )]
    TUSD_df.tail()
    #price_MXN = TUSD_df['mxn']
    #price_MXN.head()


    #Plot the dataframe
    fig, ax = plt.subplots()
    ax.plot('date', 'mxn', data=TUSD_df)

    #Format the thicks
    ax.grid(True)

    # format the coords message box
    ax.format_xdata = mdates.DateFormatter('%Y')

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

    plt.ylabel('price at MXN')
    plt.xlabel('dates')

    plt.show()

plt.show()



def run():
    plot()


if __name__ == '__main__':
    run()