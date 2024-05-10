import typing
from bs4 import BeautifulSoup
import requests

def scrapeDataFromSpreadsheet() -> typing.List[typing.List[str]]:
    html = requests.get('https://docs.google.com/spreadsheets/u/2/d/1zqEIMnOyAdTvUi1h63vaIlmPlvygIV0haxU23a9ei9c/edit?usp=drive_web&ouid=101818999536615962160').text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')[0]
    # rows = [[td.text for td in row.find_all("td")] for row in table.find_all('tr')]
    lista = []
    for element in table.find_all('tr'):
        i = 0
        aux = []
        if element.text != "":
            while i < len(element.find_all("td")):
                if len(aux) != 7:
                    aux.append(element.find_all("td")[i].text)
                else:
                    if aux[0] != '':
                        lista.append(aux)
                    aux = []
                i += 1
    return lista
