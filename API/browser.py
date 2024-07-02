import requests
import os
from dotenv import load_dotenv
import openai
import pyshorteners
from bs4 import BeautifulSoup
from data import STATIONERY_STORE, SUPERMARKET, HARDWARE_STORE, CAKE_SHOP, TECHNOLOGY_STORE

#google custom search json api
def google_search(query, num):
    """
    Do a search with google search custom json
        query: search in google
        num: num of results
    """
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'num':num
    }
    response = requests.get(url, params=params)
    results = response.json()
    if  'items' in results:
        return results["items"]
    else:
        return

#API OpenAI
def openai_api(query, role):
    """
    Question to OpenAI
        query: Question to OpenAI
        role: Role of Chatgpt
    """
    openai.api_key = API_OPENAI_KEY
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": query}
            ]
        )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

def search_tallerista(requeriments):
    tallerista = requeriments[2]
    workshoppers = []
    emails = set()
    email_domains = ["@gmail.com", "@outlook.com", "@hotmail.com", "@yahoo.com"]

    for domain in email_domains:
        search_query = f'"{domain}" site:cl.linkedin.com/in/ {tallerista}'
        linkedin_results = google_search(search_query, 10)
        for result in linkedin_results:
            email = extract_email(result["snippet"])
            if email:
                emails.add(email)
                url = result['link']
                workshoppers.append([url[27:].split("-")[0], url, email])
                break

    if not workshoppers:
        workshoppers.append("No se han encontrado talleristas para la ocasión")

    return workshoppers, tallerista

def extract_email(text):
    for element in text.split():
        if "@" in element:
            email = element.strip().replace("http://", "")
            if "m" in email:
                return email[:email.index("m")]
    return None


# Suposición de la función google_search existente para completar la implementación
def google_search(query, num_results):
    # Simula una búsqueda en Google. Implementa esta función con la lógica de búsqueda real.
    return [{'snippet': 'Contacto http://profile @gmail.com', 'link': 'https://cl.linkedin.com/in/johndoe'}]

def search_material(requeriments):
    implementos = list(map(lambda x: x.strip(), requeriments[1].split(",")))
    materials = [[],[]]
    if ("FALTANTE" not in implementos):
        print("\nMATERIALES")
        print("SUGERIDOS: ")
        for elemento in implementos:
            if "." in elemento:
                elemento = elemento.replace(".", "")
            # print("\t",elemento)
            if ("etc" not in elemento) and ("(" not in elemento) and (")" not in elemento):
                materials[0].append(elemento)
        print("\nENCONTRADOS:")
        shortener = pyshorteners.Shortener()
        presupuesto = 0
        for implemento in materials[0]:
            print(implemento.lower())
            if implemento.lower() in STATIONERY_STORE:
                print("STATIONARY")
                item = google_search("site:/nacional.cl/ " + implemento, 1)
                try:
                    url = item[0]["link"]
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    name_element = soup.find('span', class_='base')
                    price_element = soup.find('span', class_='price')
                    if name_element and price_element:
                        product_name = name_element.text.strip()
                        precio = price_element.text.strip()
                        materials[1].append([product_name, precio, shortener.tinyurl.short(url)])
                        presupuesto += int(precio[3:].replace(".", "").replace("$",""))
                    else:
                        print("\t No se encontró", implemento)
                except:
                    print("\t No se encontró", implemento)
            else:
                item = google_search("site:sodimac.falabella.com/sodimac-cl/product/ " + implemento, 1)
                try:
                    url = item[0]["link"]
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    span_element = soup.find('span', class_='copy17')

                    # Verificamos si se encontró el elemento
                    h1_element = soup.find('h1', class_='jsx-1680787435')

                    # Verificamos si se encontró el elemento
                    if h1_element and span_element:
                        product_name = h1_element.text.strip()
                        precio = span_element.text.strip()
                        materials[1].append([product_name, precio[3:], shortener.tinyurl.short(url)])
                        presupuesto += int(precio[3:].replace(".", ""))
                    else:
                        print("\t No se encontró", implemento)
                except:
                    print("\t No se encontró", implemento)

        if presupuesto != 0:
            print(f"PRESUPUESTO SUGERIDO: {presupuesto}")
        else:
            print("No se pudo calculcular el presupuesto")
    else:
        print("NO SE SUGIEREN MATERIALES")
    print()
    return materials

#KEYS
load_dotenv()
API_KEY = os.getenv("API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
API_OPENAI_KEY = os.getenv("API_OPENAI_KEY")

def caller(mensaje):
    fine = False
    formato = ""
    role_system = "Classify in the format. Type of workshop: \nNecessary implements: (if not indicated, propose the minimum necessary in SINGULAR, only put each implement followed by a comma, without putting etc or and)\nWorkshop skill: (which must be the person in charge of the workshop in few words. trade or profession)\nAge range: (children/adults/seniors/adolescents/etc)\nCity for the workshop: (if not indicated, put FALTANTE)\nSector of the city: \nBudget: . The previous format must be followed; if you cannot find a point in the prompt, it must be indicated with FALTANTE. You must respond in Spanish"
    #0: Tipo de taller
    #1: Implementos
    #2: Habilidad tallerista
    #3: Ciudad taller
    #4: Sector ciudad
    #5: Presupuesto
    if (len(mensaje) != 0):
        print(mensaje)
        response = openai_api(mensaje + formato, role_system)
        requeriments_list = list(map(lambda x: x.split(":")[1][1:] if ":" in x else x,response.strip().split("\n")))
        if ("FALTANTE" not in requeriments_list[0]):
            posibles_talleristas, type_of = search_tallerista(requeriments_list)
        else:
            return {"workshoppers": ["No se han encontrado talleristas para la ocasión"]}
    else:
        return {"workshoppers": ["No se han encontrado talleristas para la ocasión"]}
    return {"workshoppers": posibles_talleristas, "type_of": type_of}