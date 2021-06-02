""" Модуль, содержащий функции для парсинга информации об акциях (общая информация, показатели) """

__all__ = ('parse_stocks',)

import os

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup


async def parse_url(url):
    indexs = []
    names = []
    tikers = []
    last_price = []
    persent = []
    volume = []
    week = []
    month = []
    beginning_year = []
    year = []
    capitalization_rub = []
    capitalization_dollar = []
    volume_change = []
    change_position_by_volume = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            soup = BeautifulSoup(await resp.text(), 'lxml')
            table = soup.find('div', class_='trades-table_wrapper').find(
                'table',
                class_='simple-little-table trades-table'
            )
            rows = table.find_all("tr")

    df = None
    for i in range(2, len(rows)):
        # порядковый номер
        indexs.append(rows[i].find_all("td")[0].text)
        # название
        names.append(rows[i].find_all("td")[2].text)
        # тикер
        tikers.append(rows[i].find_all("td")[3].text)
        # цена, посл.
        last_price.append(rows[i].find_all("td")[7].text)
        # Изм, %
        persent.append(rows[i].find_all("td")[8].text.replace('\t', '').replace('\n', ''))
        # Объем, млн руб
        volume.append(rows[i].find_all("td")[9].text.replace(' ', ''))
        # 1 нед, %
        week.append(rows[i].find_all("td")[10].text)
        # 1 м, %
        month.append(rows[i].find_all("td")[11].text)
        # изменение цены с начала года
        beginning_year.append(rows[i].find_all("td")[12].text)
        # изменение цены за год
        year.append(rows[i].find_all("td")[13].text)
        # Капит-я млрд руб
        capitalization_rub.append(rows[i].find_all("td")[14].text.replace(' ', ''))
        # Капит-я млрд долларов
        capitalization_dollar.append(rows[i].find_all("td")[15].text.replace(' ', ''))
        # Изм объема
        volume_change.append(rows[i].find_all("td")[16].text)
        # Изм поз по объему
        change_position_by_volume.append(rows[i].find_all("td")[17].text)
        df = pd.DataFrame({'indexs': indexs,
                           'names': names,
                           'tikers': tikers,
                           'last_price': last_price,
                           'persent': persent,
                           'volume': volume,
                           'week': week,
                           'month': month,
                           'beginning_year': beginning_year,
                           'year': year,
                           'capitalization_rub': capitalization_rub,
                           'capitalization_dollar': capitalization_dollar,
                           'volume_change': volume_change,
                           'change_position_by_volume': change_position_by_volume})
    return df, tikers


def write_doc(df, name):
    name_file = name + '.csv'
    df.to_csv(name_file, index=False, sep='\t')


async def download_csv_for_tiker(tikers):
    os.makedirs('tikers_csv/', exist_ok=True)
    unknown_tikers = []
    for name in tikers:
        url = 'https://www.smart-lab.ru/q/' + name + '/f/y/MSFO/download/'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                soup = BeautifulSoup(await resp.text(), 'lxml')
        if soup.text[4:29] == '404 - Страница не найдена':
            unknown_tikers.append(name)
        else:
            with open('tikers_csv/' + name + '.csv', 'w', newline='') as csvfile:
                spamwriter = csvfile.write(soup.text)
    return unknown_tikers


async def parse_description_tikers(tikers):
    description_tikers = []
    unknown_tikers = []
    for name in tikers:
        url = 'https://www.tinkoff.ru/invest/stocks/' + name + '/'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                soup = BeautifulSoup(await resp.text(), 'lxml')

        try:
            description_tikers.append(
                soup.find('div', class_='SecurityInfoPure__wrapper_35vdA').text)
        except:
            description_tikers.append('-')
            unknown_tikers.append(name)
    df_description = pd.DataFrame({'tikers': tikers, 'description': description_tikers})
    return df_description, unknown_tikers_2


async def parse_stocks() -> int:
    """
    Парсит данные об акциях

    Returns:
        Количество спарсенных акций.
    """
    url = 'https://www.smart-lab.ru/q/shares/'
    df, tikers = await parse_url(url)
    write_doc(df, 'stock_statistics')
    unknown_tikers = await download_csv_for_tiker(tikers)

    # TODO: fix data from tinkoff
    # df_description, unknown_tikers_2 = await parse_description_tikers(tikers)
    # write_doc(df_description, 'stock_description')

    return len(tikers)


if __name__ == "__main__":
    import asyncio

    asyncio.run(parse_stocks())
