import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

def parse_stock ():
    names = []
    tikers = []
    price = []
    sector = []
    for sect in ['Other', 'HealthCare', 'IT', 'Industrials', 'RealEstate', 'Consumer', 'Materials', 'Telecom',
                 'Financial', 'Utilities', 'Energy']:
        len_rows = 0
        page = 0
        while len_rows != 1:
            url = 'https://www.tinkoff.ru/invest/stocks/?country=Russian&orderType=Asc&sortType=ByName&sector=' + sect + '&start=' + str(
                page) + '&end=' + str(page + 12)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            table = soup.find('div', class_='Table__overflowWrapper_ZwEm5')
            try:
                rows = table.find_all("tr")
                len_rows = len(rows)
                for i in range(1, len(rows)):
                    try:
                        rows[i].find_all("span")[14].text
                        num = 0
                    except:
                        num = 1
                    if num == 1:
                        names.append(rows[i].find_all("span")[3].text)
                        tikers.append(rows[i].find_all("div")[11].text)
                        price.append(str(rows[i].find_all("span")[9].text).replace('\xa0', '').replace('₽', ''))
                    else:
                        names.append(rows[i].find_all("span")[8].text)
                        tikers.append(rows[i].find_all("div")[12].text)
                        if str(rows[i].find_all("span")[14].text).replace('\xa0', '').replace('₽', '') != '':
                            price.append(str(rows[i].find_all("span")[14].text).replace('\xa0', '').replace('₽', ''))
                        else:
                            price.append(str(rows[i].find_all("span")[13].text).replace('\xa0', '').replace('₽', ''))
                    sector.append(sect)
            except:
                pass
            page += 12
    return pd.DataFrame({'names' :names,'tikers':tikers,'price':price,'sector':sector})

def analysis (df):
    df['price'] = df['price'].apply(lambda x: float(x.replace(',', '.')))
    df['price_all'] = df['price'] * df['count']
    diagram_df = df.groupby('sector')['price_all'].sum().reset_index()
    diagram_df['persent'] = diagram_df['price_all'].apply(
        lambda x: format((x / diagram_df['price_all'].sum()) * 100, '.2f'))
    sfers = ['Other', 'HealthCare', 'IT', 'Industrials', 'RealEstate', 'Consumer', 'Materials', 'Telecom',
             'Financial', 'Utilities', 'Energy']
    price = []
    percent = []
    for sfer in sfers:
        if sfer in list(diagram_df['sector']):
            price.append(float(diagram_df[diagram_df['sector'] == sfer]['price_all']))
            percent.append(float(diagram_df[diagram_df['sector'] == sfer]['persent']))
        else:
            price.append(0.0)
            percent.append(0.0)
    diagram = {'sector':sfers,
                'price':price,
                'percent':percent}
    table = {
    'Other': {'names': list(df[df['sector']=='Other']['names']), 'tikers': list(df[df['sector']=='Other']['tikers']), 'price': list(df[df['sector']=='Other']['price'])},
    'HealthCare': {'names': list(df[df['sector']=='HealthCare']['names']), 'tikers': list(df[df['sector']=='HealthCare']['tikers']), 'price': list(df[df['sector']=='HealthCare']['price'])},
    'IT': {'names': list(df[df['sector']=='IT']['names']), 'tikers': list(df[df['sector']=='IT']['tikers']), 'price': list(df[df['sector']=='IT']['price'])},
    'Industrials': {'names': list(df[df['sector']=='Industrials']['names']), 'tikers': list(df[df['sector']=='Industrials']['tikers']), 'price': list(df[df['sector']=='Industrials']['price'])},
    'RealEstate': {'names': list(df[df['sector']=='RealEstate']['names']), 'tikers': list(df[df['sector']=='RealEstate']['tikers']), 'price': list(df[df['sector']=='RealEstate']['price'])},
    'Consumer': {'names': list(df[df['sector']=='Consumer']['names']), 'tikers': list(df[df['sector']=='Consumer']['tikers']), 'price': list(df[df['sector']=='Consumer']['price'])},
    'Materials': {'names': list(df[df['sector']=='Materials']['names']), 'tikers': list(df[df['sector']=='Materials']['tikers']), 'price': list(df[df['sector']=='Materials']['price'])},
    'Telecom': {'names': list(df[df['sector']=='Telecom']['names']), 'tikers': list(df[df['sector']=='Telecom']['tikers']), 'price': list(df[df['sector']=='Telecom']['price'])},
    'Financial': {'names': list(df[df['sector']=='Financial']['names']), 'tikers': list(df[df['sector']=='Financial']['tikers']), 'price': list(df[df['sector']=='Financial']['price'])},
    'Utilities': {'names': list(df[df['sector']=='Utilities']['names']), 'tikers': list(df[df['sector']=='Utilities']['tikers']), 'price': list(df[df['sector']=='Utilities']['price'])},
    'Energy': {'names': list(df[df['sector']=='Energy']['names']), 'tikers': list(df[df['sector']=='Energy']['tikers']), 'price': list(df[df['sector']=='Energy']['price'])}
    }
    if max(percent) <40:
        recommendation = 'Оптимальная диверсификация портфеля.'
    else:
        recommendation = 'Неоптимальная диверсификация портфеля.'

    text = {
        'risk':'Умеренный',
        'recommendation':recommendation
    }
    final_df = {'diagram':diagram, 'table':table, 'text':text}
    return final_df

def add_cost_sector (df_user):
    df = pd.read_csv('stock.csv',sep='\t')
    full_df = df_user.merge(df)
    return full_df

def main():
    #df_all = parse_stock ()
    #print(len(df_all))
    names = ['MD Medical Group Investments PLC', 'Globaltrans Investment PLC', 'Транснефть']
    count = [1, 2, 3]
    df_user = pd.DataFrame({'names': names, 'count': count})

    df = add_cost_sector(df_user)
    final_df = analysis (df)
    print(final_df)


if __name__ == "__main__":
    main()
