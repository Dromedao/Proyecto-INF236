#Error 1 refactorizada
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

#Error 2 Refactorizada
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