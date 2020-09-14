import paths
import os


def json_maker(currency, price, status, now):
    """Solution to make an id for each entry of data"""
    try:
        json_content = open(paths.json_path, 'r', encoding= 'utf-8')
        #print(json_content.read())
        #id_str is the string we gonna search in the json doc, so we can get the number of
        #times that appears and give that value to the id field
        id_str = 'id'
        #The next line is the logic of the search
        id = (json_content.read()).count(id_str)
        #print(id)
    except AttributeError:
        pass


    #If there's no folder for this currency:
    try:
        if not os.path.isfile(f'{paths.json_path}'):
            with open(f'{paths.json_path}', 'w', encoding= 'utf-8') as f:
                f.write('[')
                f.write('\n')
                f.write(' {')
                f.write('\n')
                f.write(f'     "id": {int(0)},')
                f.write('\n')
                f.write(f'    "currency": "{str(currency[0])}",')
                f.write('\n')
                f.write(f'    "price": {float(price)},')
                f.write('\n')
                f.write(f'    "status": {float(status)},')
                f.write('\n')
                f.write(f'    "date": "{str(now)}"')
                f.write('\n')
                f.write(' }')
                f.write('\n')
                f.write(']')
        else:
            """Delete the last line of the file so we can add the last bracket after the last data query"""
            with open(f'{paths.json_path}', 'r', encoding= 'utf-8'):
                json_content = open(f'{paths.json_path}', 'r', encoding= 'utf-8')
                json_content_read = json_content.read()
                json_content.close
                m = json_content_read.split("\n")
                s = "\n".join(m[:-1])
                json_content = open(f'{paths.json_path}',"w+")
                for i in range(len(s)):
                    json_content.write(s[i])
                json_content.close()
            """Append the last data query to the file"""
            with open(f'{paths.json_path}', 'a', encoding= 'utf-8') as a:
                a.write(',')
                a.write('\n')
                a.write(' {')
                a.write('\n')
                a.write(f'    "id": {id},')
                a.write('\n')
                a.write(f'    "currency": "{str(currency[0])}",')
                a.write('\n')
                a.write(f'    "price": {float(price)},')
                a.write('\n')
                a.write(f'    "status": {float(status)},')
                a.write('\n')
                a.write(f'    "date": "{str(now)}"')
                a.write('\n')
                a.write(' }')
                a.write('\n')
                a.write(']')
    except AttributeError:
        pass