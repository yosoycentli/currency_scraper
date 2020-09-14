"""Formats of the scraper"""


#delete the fisrt character "$" from the price array
def del_dll_sign(price_with_dolar_sign):
    try:
         price = re.search('([-+]?[0-9]*\.?[0-9]+$)', price_with_dolar_sign[0]).group(1)
    except AttributeError:
        price = f'el precio sigue teniendo el signo de $: {price_with_dolar_sign[0]}'
#print(price)
