import typing
from bs4 import BeautifulSoup
from typing import List
import requests

def scrapeDataFromSpreadsheet() -> List[List[str]]:
    try:
        html = requests.get('https://docs.google.com/spreadsheets/u/2/d/1zqEIMnOyAdTvUi1h63vaIlmPlvygIV0haxU23a9ei9c/edit?usp=drive_web&ouid=101818999536615962160').text
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find_all('table')[0]
        lista = []

        for element in table.find_all('tr'):
            i = 0
            aux = []
            if element.text.strip() != "":
                while i < len(element.find_all("td")):
                    if len(aux) < 7:
                        aux.append(element.find_all("td")[i].text.strip())
                    else:
                        if aux[0] != '':
                            lista.append(aux)
                        aux = []
                    i += 1
        return lista
    except Exception as e:
        print(f"Error al raspar datos: {e}")
        return []