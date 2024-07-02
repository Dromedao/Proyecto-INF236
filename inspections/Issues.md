Para la realización de la inspección del código utilizamos "sonarcloud" como se nos recomendó, y la sección de codigo a analizar será el "browser" que es parte de la "API", dicho archivo declara funciones que serán utilizadas para la búsqueda de talleristas y de materiales (aunque está ultima por petición del cliente, fue dejada de lado).

Sonarcloud nos señaló errores principalmente relacionados con la mantenibilidad del código, de los cuales nos vamos a centrar en lo que creemos más relevantes, como lo son los siguientes:

## Error 1
En la presente "issue" se nos indica que debemos refactorizar la función "search_tallerista" la cual debido a la anidación de múltiples estructuras tiene una complejidad cognitiva alta, por lo que debe ser refactorizada. Esta "issue" está etiquetada como de alta prioridad, por lo que debe ser solucionada a la brevedad, antes de que el problema sea mayor.

### Como será abordado


Sonarcloud nos comenta que para poder abordar este problema debemos seguir los siguientes consejos:
* Extraer las condiciones complejas en nuevas funciones
* En caso de que sea necesario, dividir la función en funciones más pequeñas.
* Evitar el anidamiento

El código antiguo es:
```python
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
```
El nuevo refactorizado es:
```python
def extract_email(text):
    for element in text.split():
        if "@" in element:
            email = element.strip().replace("http://", "")
            if "m" in email:
                return email[:email.index("m")]
    return None

def search_tallerista(requeriments):
    tallerista = requeriments[2]
    workshoppers = []
    emails = set()
    email_domains = ["@gmail.com", "@outlook.com", "@hotmail.com", "@yahoo.com"]

    for domain in email_domains:
        search_query = f'"{domain}" site:cl.linkedin.com/in/ {tallerista}'
        linkedin_results = google_search(search_query, 10)
        found = False
        for result in linkedin_results:
            email = extract_email(result["snippet"])
            if email:
                emails.add(email)
                url = result['link']
                workshoppers.append([url[27:].split("-")[0], url, email])
                found = True
                break
        if found:
            break

    if not workshoppers:
        workshoppers.append("No se han encontrado talleristas para la ocasión")

    return workshoppers, tallerista
```
Como se puede ver, el nuevo código es mucho más simple de entender que el primero, además de mucho más eficiente

### Error 2
Similar a la "issue" anterior, nuevamente se nos indica que debemos refactorizar una función, pero en este caso se nos indica que existe un bucle que de la forma en la que fue diseñado, solo iterará una vez, finalizando por los "return" que están dentro del mismo, por lo que se debe buscar una estructura más adecuada. La presente "issue" está etiquetada como de media prioridad, pero fue escogida ya que es utilizada múltiples veces para el funcionamiento del programa, además de que su solución es más compleja que las demás "issues" que aparecen.
Para este "issue" sonarcloud no nos sugirió una forma de solucionarlo, por lo que tuvimos que verlo nosotros, pero luego de inspeccionar el código pudimos darnos cuenta de que la solución era más simple de lo que habíamos pensado.
El código antiguo es:
```python
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
```
El nuevo refactorizado es:
```python
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
```
El cual es más fácil de entender que la primera versión, además de que ya está corregido el fallo lógico indicado.
