import requests
import openai
import pyshorteners
from bs4 import BeautifulSoup

"""
Grupo 9
Joaquín Lopez
Matías Guerra
"""

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
    return completion.choices[0].message.content

def search_tallerista(requeriments):
    tallerista = requeriments[2]
    boolean_talleristas = True

    print("TALLERISTAS SUGERIDOS")

    linkedin = google_search("site:cl.linkedin.com/in/ " + tallerista, 5)
    try:
        for item in linkedin:
            url = item['link']
            print("\t", url[27:].split("-")[0], url)
    except:
        boolean_talleristas = False
    superprof = google_search("site:superprof.com/ " + tallerista, 5)
    try:
        for item in superprof:
            url = item['link']
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            elements_with_class = (soup.find_all(attrs={"class": "name"}))
            elements_with_class2 = (soup.find_all(attrs={"class": "landing-v4-ads-pic-firstname"}))
            try:
                if len(elements_with_class) != 0:
                    print("\t",elements_with_class[0].text, url)
                elif len(elements_with_class2) != 0:
                    print("\t",elements_with_class2[0].text, url)
            except:
                # print(url)
                pass
            if boolean_talleristas == False:
                boolean_talleristas = True
    except:
        pass
    if boolean_talleristas == False:
        print("No se han encontrado talleristas para la ocasión...")
    print()

def search_material(requeriments):
    implementos = list(map(lambda x: x.strip(), requeriments[1].split(",")))
    if ("FALTANTE" not in implementos):
        print("\nMATERIALES")
        print("SUGERIDOS: ")
        for elemento in implementos:
            if "." in elemento:
                elemento = elemento.replace(".", "")
            print("\t",elemento)
        print("\nENCONTRADOS:")
        shortener = pyshorteners.Shortener()
        presupuesto = 0
        for implemento in implementos:
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
                    print(f"\t {product_name} - {precio[3:]} - {shortener.tinyurl.short(url)}")
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

#KEYS
API_KEY = open("API_KEY").read()
SEARCH_ENGINE_ID = open('SEARCH_ENGINE_ID').read()
API_OPENAI_KEY = open("API_OPENAI_KEY").read()

fine = False
while fine == False:
    #Question to the user
    mensaje = input("Que taller desea realizar?: ")
    print()

    formato = " | Clasificar en el formato. Tipo de taller: \nImplementos necesarios: (en caso de no indicarse, proponer los minimos necesarios en SINGULAR, solo poner cada implemento seguido de una coma)\nHabilidad tallerista: (lo que tiene que ser el encargado del taller en pocas palabras. oficio o profesion)\nRango de edad: (niños/adultos/tercera edad/adolecentes/etc)\nCiudad para el taller: \nSector de la ciudad: \nPresupuesto: . (Se debe seguir el anterior formato, en caso de no poder encontrar un punto en el prompt se debe indicar con FALTANTE. En caso de la busqueda ser insuficiente para clasificar poner FALTANTE"
    role_system = "Recibes el prompt para la creación de un taller. Solo clasificar el mismo, sin palabras innecesarias"
    #0: Tipo de taller
    #1: Implementos
    #2: Habilidad tallerista
    #3: Ciudad taller
    #4: Sector ciudad
    #5: Presupuesto
    response = openai_api(mensaje + formato, role_system)
    requeriments_list = list(map(lambda x: x.split(":")[1][1:] if ":" in x else x,response.strip().split("\n")))
    if "FALTANTE" not in requeriments_list[0]:
        posibles_talleristas = search_tallerista(requeriments_list)
        if "FALTANTE" not in requeriments_list[1]:
            materiales = search_material(requeriments_list)
        else:
            print("No se sugieren materiales...")
    else:
        print("No se cumplen con los minimos requerimientos para realizar la busqueda...\n")
    
    final = input("¿Está conforme con los resultados: Y/n: ")
    while final not in ("Y", "y", "N", "n"):
        print("Indique una respuesta valida")
        final = input("¿Está conforme con los resultados: Y/n: ")
    if final in ("Y", "y"):
            fine = True
    elif final in ("N", "n"):
        fine = False