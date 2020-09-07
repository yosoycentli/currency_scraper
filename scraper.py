import requests
import lxml.html as html
import os
import datetime
import re


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
                status_with_dolar_sign = parsed.xpath(XPATH_CURRENCY_STATUS_LEVEL)
                now = datetime.datetime.now()
            except IndexError:
                return
            

            #delete the fisrt character "$" from the price array
            try:
                price = re.search('([-+]?[0-9]*\.?[0-9]+$)', price_with_dolar_sign[0]).group(1)
            except AttributeError:
                price = f'el precio sigue teniendo el signo de $: {price_with_dolar_sign[0]}'
            
            #print(price)

            id = len(price)


            #delete de last character '%' from the status array
            try:
                status = re.search('(^[-+]?[0-9]*\.?[0-9]+)', status_with_dolar_sign[0]).group(1)
            except AttributeError:
                status = f'el precio sigue teniendo el signo de $: {status_with_dolar_sign[0]}'
            
            #print(status)


            """Solution to make an id for each entry of data"""
            currencies_record_json = 'currencies_record.json'
            currencies_record = 'currencies_record'
            json_content = open(f'{currencies_record}/{currencies_record_json}', 'r', encoding= 'utf-8')
            #print(json_content.read())
            """id_str is the string we gonna search in the json doc, so we can get the number of
            times that appears and give that value to the id field"""
            id_str = 'id'
            """The next line is the logic of the search"""
            id = (json_content.read()).count(id_str)
            #print(id)


            #If there's no folder for this currency:
            currencies_record_json = 'currencies_record.json'
            currencies_record = 'currencies_record'
            if not os.path.isfile(f'{currencies_record}/{currencies_record_json}'):
                with open(f'{currencies_record}/{currencies_record}.json', 'w', encoding= 'utf-8') as f:
                    f.write('[')
                    f.write('\n')
                    f.write(' {')
                    f.write('\n')
                    f.write(f'    "id": {int(0)}')
                    f.write('\n')
                    f.write(f'    "currency": {currency[0]},')
                    f.write('\n')
                    f.write(f'    "price": {float(price)},')
                    f.write('\n')
                    f.write(f'    "status": {float(status)},')
                    f.write('\n')
                    f.write(f'    "date": {now}')
                    f.write('\n')
                    f.write(' }')
                    f.write('\n')
                    f.write(']')
            else:
                """Delete the last line of the file so we can add the last bracket after the last data query"""
                with open(f'{currencies_record}/{currencies_record}.json', 'r', encoding= 'utf-8'):
                    json_content = open(f'{currencies_record}/{currencies_record_json}', 'r', encoding= 'utf-8')
                    json_content_read = json_content.read()
                    json_content.close
                    m = json_content_read.split("\n")
                    s = "\n".join(m[:-1])
                    json_content = open(f'{currencies_record}/{currencies_record_json}',"w+")
                    for i in range(len(s)):
                        json_content.write(s[i])
                    json_content.close()
                """Append the last data query to the file"""
                with open(f'{currencies_record}/{currencies_record}.json', 'a', encoding= 'utf-8') as a:
                    a.write(',')
                    a.write('\n')
                    a.write(' {')
                    a.write('\n')
                    a.write(f'   "id": {id}')
                    a.write('\n')
                    a.write(f'    "currency": {currency[0]},')
                    a.write('\n')
                    a.write(f'    "price": {float(price)},')
                    a.write('\n')
                    a.write(f'    "status": {float(status)},')
                    a.write('\n')
                    a.write(f'    "date": {now}')
                    a.write('\n')
                    a.write(' }')
                    a.write('\n')
                    a.write(']')

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
            currencies_record='currencies_record'
            if not os.path.isdir(currencies_record):
                os.mkdir(currencies_record)

            for link in validation_link:
                parse_currency(link, currencies_record)
            print(f'The name of the directory where the info is: {currencies_record}')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()