#Error 1
def search_tallerista(requeriments):
    tallerista = requeriments[2]
    boolean_talleristas = True

    workshoppers = []
    emails = []
    print("TALLERISTAS SUGERIDOS")

    linkedin = google_search('"@gmail.com" site:cl.linkedin.com/in/ ' + tallerista , 10)
    try:
        for item in linkedin:
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
    try:
        for item in linkedin:
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
    try:
        for item in linkedin:
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
    try:
        for item in linkedin:
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
    emails = list(set(emails))
    print(emails)
    
    if boolean_talleristas == False:
        workshoppers.append("No se han encontrado talleristas para la ocasión")
    print(tallerista, "TALLERISTATALLERISTATALLERISTA")
    return workshoppers, tallerista

#Error 2
def caller(mensaje):
    fine = False
    while fine == False:
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
                print(type_of, "TYPE_OFTYPE_OFTYPE_OFTYPE_OFTYPE_OF")
            else:
                print("No se cumplen con los minimos requerimientos para realizar la busqueda...\n")
                return {"workshoppers": ["No se han encontrado talleristas para la ocasión"]}
        else:
            print("No se cumplen con los minimos requerimientos para realizar la busqueda...\n")
            return {"workshoppers": ["No se han encontrado talleristas para la ocasión"]}
    
        return {"workshoppers": posibles_talleristas, "type_of": type_of}