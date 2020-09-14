import requests
import lxml.html as html
import os
import datetime
import re
import time


import paths
import formats
import json_maker


HOME_URL1 = 'https://www.coingecko.com'
HOME_URL2 = 'https://global.bittrex.com/Market/Index?MarketName=USDT-TUSD'
HOME_URL3 = 'https://coinsbit.io'


#Variables del HOME_URL1
XPATH_TRUEUSD = '//div[@class="d-flex"]/div[@class= "center"]/a[contains(.,"TrueUSD")]/@href'
XPATH_TITLE = '//h1/text()'
XPATH_CURRENCY = '//span[@class="calc-symbol-box center" and contains(.,"TUSD")]/text()'
XPATH_USD_PRICE = '//div[@class="text-3xl"]/span[@class= "no-wrap"]/text()'
XPATH_CURRENCY_STATUS_LEVEL = '//span[@class= "live-percent-change ml-1"]/span[contains(.,"%")]/text()'


#Variables del HOME_URL2
XPATH_LINK_TO_MARKETS2= '//div[@class="nav-bar-menu--list"]/a[1]/@href'


#Variables del HOME_URL3
XPATH_XCHANGE_3= '//div[@class= "cnb-header__desk-right-container"]/a/@href'


def parse_currency (link, currencies_record):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            currency_now = response.content.decode('utf-8')
            parsed = html.fromstring(currency_now)

            try:
                title = parsed.xpath(XPATH_TITLE)
                currency = parsed.xpath(XPATH_CURRENCY)
                price_with_dolar_sign = parsed.xpath(XPATH_USD_PRICE)
                status_with_percent_sign = parsed.xpath(XPATH_CURRENCY_STATUS_LEVEL)
                local_time = time.localtime()
                now = time.strftime("%d/%m/%Y - %H:%M:%S", local_time)
            except IndexError:
                return
            

            #delete the fisrt character "$" from the price array
            try:
                price = re.search('([-+]?[0-9]*\.?[0-9]+$)', price_with_dolar_sign[0]).group(1)
            except AttributeError:
                price = f'the price still has the $ sign: {price_with_dolar_sign[0]}'
            
            #print(price)
            formats.del_dll_sign


            #delete de last character '%' from the status array
            try:
                status = re.search('(^[-+]?[0-9]*\.?[0-9]+)', status_with_percent_sign[0]).group(1)
            except AttributeError:
                status = f'the status still has the % sign: {status_with_percent_sign[0]}'            
            #print(status)

            try:
                #TUSD entry
                json_maker.json_maker(currency, price, status, now)
            except AttributeError:
                pass

        pass

    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL1)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            #The main rout must be here
            route = parsed.xpath(XPATH_TRUEUSD)
            #Since the URL we need for currency is an extension (not a complete URL) we must add it to the main url
            validation_link_str = str((HOME_URL1+(route[0])))
            #The validation_link is the complete URL where our currency is
            validation_link = [validation_link_str]
            print(f'URL queried: {validation_link}')

            #today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(paths.currency_folder_path):
                os.mkdir(paths.currency_folder_path)

            for link in validation_link:
                parse_currency(link, paths.currency_folder_path)
            print(f'The name of the directory where the info is: {paths.currency_folder_path}')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()