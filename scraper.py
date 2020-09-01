import requests
import lxml.html as html
import os
import datetime


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


def parse_currency (link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            currency_now = response.content.decode('utf-8')
            parsed = html.fromstring(currency_now)

            try:
                title = parsed.xpath(XPATH_TITLE)
                currency = parsed.xpath(XPATH_CURRENCY)
                price = parsed.xpath(XPATH_USD_PRICE)
                status = parsed.xpath(XPATH_CURRENCY_STATUS_LEVEL)
                now = datetime.datetime.now()
            except IndexError:
                return

            with open(f'{today}/{now}.txt', 'w', encoding= 'utf-8') as f:
                f.write(f'{currency[0]},{price[0]},{status[0]},{now}')
                
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

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in validation_link:
                parse_currency(link, today)
            print(f'Name of the directory where the info is: {today}')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()