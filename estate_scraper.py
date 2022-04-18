from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np


# TEXTER - extracts text
def texter(obj):
    try:
        obj = " ".join(map(lambda x: x.text, obj))
    except:
        obj = "NaN"
    finally:
        return(obj)
    
# LINKER - extracts links
def linker(obj): 
    obj = map(lambda x: x.get('href'), obj)
    return(obj)


                        ### - = S C R A P E R = - ###
df = pd.DataFrame(columns = [
    'link',
    'name',
    'price',
    'pricem2',
    'location',
    'area',
    'ownership',
    'rooms',
    'state',
    'level',
    'features',
    'rent',
    'parking',
    'remote',
    'heating',
    'description',
    'market',
    'adv_type',
    'avaliable',
    'const_year',
    'building_type',
    'windows',
    'lift',
    'media',
    'security',
    'equipment',
    'add_info',
    'building_material'])
for w in range(1,5):
    url = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/wroclaw?page=' + str(w) + '&limit=1000'
    page = requests.get(url)
    content = page.content
    soup = bs(content, 'html.parser')
    linki = list(linker(soup.find_all('a', {'class':'css-rvjxyq es62z2j14'})))
    for i in linki:
        link = str('https://www.otodom.pl' + i)
        page = requests.get(link)
        page_content = page.content
        soup_page = bs(page_content, 'html.parser')
        name = texter(soup_page.find('h1', {'class':'css-11kn46p eu6swcv17'}))
        price = texter(soup_page.find('strong', {'class':'css-8qi9av eu6swcv16'}))
        pricem2 = texter(soup_page.find('div', {'class':'css-1p44dor eu6swcv13'}))         
        location = texter(soup_page.find('a', {'class':'e1nbpvi60 css-1kforri e1enecw71'})) 
        details = soup_page.find('div', {'class':'css-wj4wb2 emxfhao1'})
        if details is not None:
            area = texter(list(details)[1])
            ownership = texter(list(details)[2])
            rooms = texter(list(details)[3])
            state = texter(list(details)[4])
            level = texter(list(details)[5])
            features = texter(list(details)[6])
            rent = texter(list(details)[7])
            parking = texter(list(details)[8])
            remote = texter(list(details)[9])
            heating = texter(list(details)[10])
        else:
            area = 'NaN'
            ownership = 'NaN'
            rooms = 'NaN'
            state = 'NaN'
            level = 'NaN'
            features = 'NaN'
            rent = 'NaN'
            parking = 'NaN'
            remote = 'NaN'
            heating = 'NaN'
        description = 'NaN'
        description = soup_page.find('section', {'class':'css-3hljba e1r1048u3'})
        description = texter(description)
        details2 = soup_page.find('div', {'class':'css-1l1r91c emxfhao1'}) 
        if details2 is not None:
            market = texter(list(details2)[1])
            adv_type = texter(list(details2)[2])
            avaliable = texter(list(details2)[3])
            const_year = texter(list(details2)[4])
            building_type = texter(list(details2)[5])
            windows = texter(list(details2)[6])
            lift = texter(list(details2)[7])
            media = texter(list(details2)[8])
            security = texter(list(details2)[9])
            equipment = texter(list(details2)[10])
            add_info = texter(list(details2)[11])
            building_material = texter(list(details2)[12])
        else:
            market = 'NaN'
            adv_type = 'NaN'
            avaliable = 'NaN'
            const_year = 'NaN'
            building_type = 'NaN'
            windows = 'NaN'
            lift = 'NaN'
            media = 'NaN'
            security = 'NaN'
            equipment = 'NaN'
            add_info = 'NaN'
            building_material = 'NaN'
        df.loc[i, df.columns.values] = link, name, price, pricem2, location, area, ownership, rooms, state, level, features, rent, parking,remote,heating, description, market, adv_type, avaliable, const_year,building_type, windows, lift,media, security, equipment, add_info, building_material
        print('[' + str(linki.index(i)+(w*1003-1003))+ ' /', str(len(linki)*5) + '] -', i)
df.to_csv('scrape_data.csv')
