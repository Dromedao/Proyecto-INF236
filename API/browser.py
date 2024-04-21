import requests
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
    boolean_talleristas = True

    workshoppers = []
    emails = []
    print("TALLERISTAS SUGERIDOS")
    #ANTERIORMENTE 5
    linkedin = google_search('"@gmail.com" site:cl.linkedin.com/in/ ' + tallerista , 10)
    # print("\n\n",linkedin,"\n\n")
    try:
        for item in linkedin:
            # print("\n\n",item["snippet"],"\n\n")
            for element in item["snippet"].split():
                element = element.replace("http://","")
                if "@" in element:
                    if element[-1] != "m" and "m" in element:
                        element = element[:len(element)-element[::-1].index("m")]
                    print("\n\n",element.strip(),"\n\n")
                    emails.append(element.strip())
                    url = item['link']
                    workshoppers.append([url[27:].split("-")[0], url, element.strip()])
                    break
    except:
        boolean_talleristas = False

    linkedin = google_search('"@outlook.com" site:cl.linkedin.com/in/ ' + tallerista , 10)
    # print("\n\n",linkedin,"\n\n")
    try:
        for item in linkedin:
            # print("\n\n",item["snippet"],"\n\n")
            for element in item["snippet"].split():
                if "@" in element:
                    element = element.replace("http://","")
                    if element[-1] != "m" and "m" in element:
                        element = element[:len(element)-element[::-1].index("m")]
                    print("\n\n",element.strip(),"\n\n")
                    emails.append(element.strip())
                    url = item['link']
                    workshoppers.append([url[27:].split("-")[0], url, element.strip()])
                    break
    except:
        boolean_talleristas = False

    linkedin = google_search('"@hotmail.com" site:cl.linkedin.com/in/ ' + tallerista , 10)
    # print("\n\n",linkedin,"\n\n")
    try:
        for item in linkedin:
            # print("\n\n",item["snippet"],"\n\n")
            for element in item["snippet"].split():
                if "@" in element:
                    element = element.replace("http://","")
                    if element[-1] != "m" and "m" in element:
                        element = element[:len(element)-element[::-1].index("m")]
                    print("\n\n",element.strip(),"\n\n")
                    emails.append(element.strip())
                    url = item['link']
                    workshoppers.append([url[27:].split("-")[0], url, element.strip()])
                    break
    except:
        boolean_talleristas = False

    linkedin = google_search('"@yahoo.com" site:cl.linkedin.com/in/ ' + tallerista , 10)
    # print("\n\n",linkedin,"\n\n")
    try:
        for item in linkedin:
            # print("\n\n",item["snippet"],"\n\n")
            for element in item["snippet"].split():
                if "@" in element:
                    element = element.replace("http://","")
                    if element[-1] != "m" and "m" in element:
                        element = element[:len(element)-element[::-1].index("m")]
                    print("\n\n",element.strip(),"\n\n")
                    emails.append(element.strip())
                    url = item['link']
                    workshoppers.append([url[27:].split("-")[0], url, element.strip()])
                    break
    except: 
        boolean_talleristas = False
    # print(emails)
    emails = list(set(emails))
    print(emails)
    #ANTERIORMENTE 5
    # superprof = google_search('"@gmail.com" site:superprof.com/ ' + tallerista, 8)
    # try:
    #     for item in superprof:
    #         # print("\n\n",item["snippet"].split(),"\n\n")
    #         for element in item["snippet"].split():
    #             if "@" in element:
    #                 print("\n\n",element,"\n\n")
    #         url = item['link']
    #         page = requests.get(url)
    #         soup = BeautifulSoup(page.content, 'html.parser')
    #         elements_with_class = (soup.find_all(attrs={"class": "name"}))
    #         elements_with_class2 = (soup.find_all(attrs={"class": "landing-v4-ads-pic-firstname"}))
    #         try:
    #             if len(elements_with_class) != 0:
    #                 # print("\t",elements_with_class[0].text, url)
    #                 workshoppers.append([elements_with_class[0].text, url])
    #             elif len(elements_with_class2) != 0:
    #                 # print("\t",elements_with_class2[0].text, url)
    #                 workshoppers.append([elements_with_class2[0].text, url])
    #         except:
    #             # print(url)
    #             pass
    #         if boolean_talleristas == False:
    #             boolean_talleristas = True
    # except:
    #     pass
    if boolean_talleristas == False:
    #     print("No se han encontrado talleristas para la ocasión...")
        workshoppers.append("No se han encontrado talleristas para la ocasión")
    # print()
    return workshoppers

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
            ##########################
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
                        # print(f"\t {product_name} - {precio[3:]} - {shortener.tinyurl.short(url)}")
                        materials[1].append([product_name, precio[3:], shortener.tinyurl.short(url)])
                        presupuesto += int(precio[3:].replace(".", ""))
                    else:
                        print("\t No se encontró", implemento)
                except:
                    print("\t No se encontró", implemento)
            # elif implemento in SUPERMARKET:
            #     pass
            # elif implemento in CAKE_SHOP:
            #     pass
            # elif implemento in TECHNOLOGY_STORE:
            #     pass
            # else:
            #     pass
            ##########################
        if presupuesto != 0:
            print(f"PRESUPUESTO SUGERIDO: {presupuesto}")
        else:
            print("No se pudo calculcular el presupuesto")
    else:
        print("NO SE SUGIEREN MATERIALES")
    print()
    return materials

#KEYS
API_KEY = open("API_KEY").read()
SEARCH_ENGINE_ID = open('SEARCH_ENGINE_ID').read()
API_OPENAI_KEY = open("API_OPENAI_KEY").read()


def caller(mensaje):
    fine = False
    while fine == False:
        #Question to the user
        # mensaje = input("Que taller desea realizar?: ")
        # print()

        #formato = " | Clasificar en el formato. Tipo de taller: \nImplementos necesarios: (en caso de no indicarse, proponer los minimos necesarios en SINGULAR, solo poner cada implemento seguido de una coma)\nHabilidad tallerista: (lo que tiene que ser el encargado del taller en pocas palabras. oficio o profesion)\nRango de edad: (niños/adultos/tercera edad/adolecentes/etc)\nCiudad para el taller: \nSector de la ciudad: \nPresupuesto: . (Se debe seguir el anterior formato, en caso de no poder encontrar un punto en el prompt se debe indicar con FALTANTE. En caso de la busqueda ser insuficiente para clasificar poner FALTANTE"
        #role_system = "Recibes el prompt para la creación de un taller. Solo clasificar el mismo, sin palabras innecesarias"
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
                posibles_talleristas = search_tallerista(requeriments_list)
                # if "FALTANTE" not in requeriments_list[1]:
                #     materiales = search_material(requeriments_list)
                # else:
                #     materiales = [["No se sugieren materiales..."],["No se buscan materiales..."]]
                #     print("No se sugieren materiales...")
            else:
                print("No se cumplen con los minimos requerimientos para realizar la busqueda...\n")
                # return {"workshoppers": ["No se han encontrado talleristas para la ocasión"], "materials":[["No se sugieren materiales..."],["No se buscan materiales..."]]}
                return {"workshoppers": ["No se han encontrado talleristas para la ocasión"]}
        else:
            print("No se cumplen con los minimos requerimientos para realizar la busqueda...\n")
            # return {"workshoppers": ["No se han encontrado talleristas para la ocasión"], "materials":[["No se sugieren materiales..."],["No se buscan materiales..."]]}
            return {"workshoppers": ["No se han encontrado talleristas para la ocasión"]}
    
        # return {"workshoppers": posibles_talleristas, "materials":materiales}
        return {"workshoppers": posibles_talleristas}