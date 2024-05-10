import streamlit as st
import pandas as pd
import requests

import typing
from bs4 import BeautifulSoup

# def scrapeDataFromSpreadsheet() -> typing.List[typing.List[str]]:
#     html = requests.get('https://docs.google.com/spreadsheets/u/2/d/1zqEIMnOyAdTvUi1h63vaIlmPlvygIV0haxU23a9ei9c/edit?usp=drive_web&ouid=101818999536615962160').text
#     soup = BeautifulSoup(html, 'lxml')
#     table = soup.find_all('table')[0]
#     # rows = [[td.text for td in row.find_all("td")] for row in table.find_all('tr')]
#     lista = []
#     for element in table.find_all('tr'):
#         i = 0
#         aux = []
#         if element.text != "":
#             while i < len(element.find_all("td")):
#                 if len(aux) != 6:
#                     aux.append(element.find_all("td")[i].text)
#                 else:
#                     if aux[0] != '':
#                         lista.append(aux)
#                     aux = []
#                 i += 1
#     return lista

# responses_received = scrapeDataFromSpreadsheet()

st.set_page_config(page_title="Apprende Browser", page_icon=":grapes:", layout="wide")

hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

with st.spinner("Contactando con la API..."):
    # print("ENTROOOOOOOOOOOo")
    api_url = "http://127.0.0.1:8000/scrape_form"
    responses_received = requests.get(api_url).json()["results"]
    # print(responses_received, "djadsfds")

with open("./static/css/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_contacts():
    api_url = "http://127.0.0.1:8000/contacts"
    response = requests.get(api_url)
    # responses_received = scrapeDataFromSpreadsheet()
    if response.status_code == 200:
        contacts_data = response.json()
        for element in contacts_data:
            # Si el email está en las respuestas recibidas
            if any(element["email"] in lista for lista in responses_received):
                element["state"] = "🔔 Respuesta recibida..."
            else:
                element["state"] = "🕯️ Esperando respuesta..."
            if element["decision"] == 0:
                element["decision"] = "🗂️ Sin decisión..."
            elif element["decision"] == 1:
                element["decision"] = "✅ Aceptado."
            elif element["decision"] == 2:
                element["decision"] = "🚫 Rechazado"
        return contacts_data
    else:
        st.error(f"Error en la solicitud. Código de estado: {response.status_code}")
        st.write(response.text)
        return []

contacts_data = get_contacts()

# Muestra los datos uno debajo de otro
if contacts_data:
    st.title("Contactados")
    for idx, element in enumerate(contacts_data):
        # st.write(f"**Nombre**: {element['name']}")
        # st.write(f"**Correo electrónico**: {element['email']}")
        # st.write(f"**Estado de respuesta**: {element['state']}")
        # st.write(f"**Decisión**: {element['decision']}")
        st.write(f"{element['name']}")
        st.write(f"{element['type_of']}")
        st.write(f"{element['email']}")
        st.write(f"{element['state']}")
        if element["state"] == "🔔 Respuesta recibida...":
            with st.popover("Ver más"):
                for index, lista in enumerate(responses_received):
                    if element["email"] in lista:
                        st.write("**Número telefonico**")
                        st.write(responses_received[index][4])
                        st.write("**Región en la que puede trabajar**")
                        st.write(responses_received[index][3])
                        st.write("**Cuentas algo sobre ti**")
                        if responses_received[index][6] != "":
                            st.write(responses_received[index][6])
                        else:
                            st.write("No añadió nada")
                        st.write("**Sugiere un taller**")
                        if responses_received[index][5] != "":
                            st.write(responses_received[index][5])
                        else:
                            st.write("No añadió nada")
                # if element["state"] == "🕯️ Esperando respuesta...":
                #     st.write("Esperando respuesta...")
        st.write(f"{element['decision']}")
        # with st.popover("Tomar desición"):
        #     if st.button("Aceptar", key=f"aceptar_{idx}"):
        #         print("Entro")
        #         api_url = f"http://127.0.0.1:8000/contact_decision"
        #         data = {
        #                 "name": "",
        #                 "email": element["email"],
        #                 "state": 0,
        #                 "decision":1
        #             }
        #         print(element["email"])
        #         response = requests.patch(api_url, json=data)
        #         # refresh()
        #     if st.button("Rechazar", key=f"rechazar_{idx}"):
        #         api_url = f"http://127.0.0.1:8000/contact_decision"
        #         data = {
        #                 "name": "",
        #                 "email": element["email"],
        #                 "state": 0,
        #                 "decision":2
        #             }
        #         print(element["email"])
        #         response = requests.patch(api_url, json=data)
        st.write("**Tomar desición**")
        if st.button("Aceptar", key=f"aceptar_{idx}"):
            print("Entro")
            api_url = f"http://127.0.0.1:8000/contact_decision"
            data = {
                    "name": "",
                    "email": element["email"],
                    "type_of": "",
                    "state": 0,
                    "decision":1
                }
            print(element["email"])
            response = requests.patch(api_url, json=data)
        if st.button("Rechazar", key=f"rechazar_{idx}"):
            api_url = f"http://127.0.0.1:8000/contact_decision"
            data = {
                    "name": "",
                    "email": element["email"],
                    "type_of": "",
                    "state": 0,
                    "decision":2
                }
            print(element["email"])
            response = requests.patch(api_url, json=data)
        st.write("-----------------------------")
else:
    st.write("No hay datos para mostrar.")
