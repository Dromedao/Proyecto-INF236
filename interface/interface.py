import streamlit as st
from PIL import Image

import requests

st.set_page_config(page_title="Apprende Browser", page_icon=":grapes:", layout="wide")

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

def send_to_api(texto):
    total = 0
    with st.spinner("Realizando busqueda..."):
        api_url = "http://127.0.0.1:8000/search"
        data = {"prompt": texto}
        
        # Enviar la solicitud POST a la API
        response = requests.post(api_url, json=data)
        
        # Manejar la respuesta de la API
        if response.status_code == 200 or response.status_code == 201:
            st.success("Resultados :mag:")
            # st.header("Resultados :mag:")
            st.subheader("Talleristas")
            if isinstance(response.json()["workshoppers"][0], str):
                print("ENTRO")
                st.write("No se han encontrado talleristas...")
            else:
                # print(type(response.json()["workshoppers"][0]))
                for whorshopper in response.json()["workshoppers"]:
                    st.write(f"{whorshopper[0]}: {whorshopper[1]}")
            st.subheader("Materiales sugeridos")
            for material in response.json()["materials"][0]:
                st.write(f"{material}")
            st.subheader("Materiales encontrados")
            for material in response.json()["materials"][1]:
                if isinstance(material, str):
                    st.write(material)
                else:
                    st.write(f"{material[0]}, {material[1]}, {material[2]}")
                    total += int(material[1].replace(".","").replace("$",""))
            st.subheader("Presupuesto estimado")
            st.write(f"${total}")
            # st.write(response.json())
        else:
            st.error(f"Error en la solicitud. Código de estado: {response.status_code}")
            st.write(response.text)

def budget(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["budget"]
    else:
        return "No se ha podido calcular el presupuesto..."

def history():
    with st.spinner("Realizando consulta..."):
        api_url = "http://127.0.0.1:8000/searchs"
        
        # Enviar la solicitud POST a la API
        response = requests.get(api_url)
        # Manejar la respuesta de la API
        if response.status_code == 200:
            st.success("Historial :floppy_disk:")
            results = list(reversed(response.json()))
            try:
                for element in results:
                    st.subheader("Prompt")
                    st.write(element["prompt"])
                    st.subheader("Materiales sugeridos")
                    for material in element["materials"][0]:
                        st.write(material)
                    st.subheader("Materiales encontrados")
                    for material in element["materials"][1]:
                        if isinstance(material, str):
                            st.write(material)
                        else:
                            st.write(f"{material[0]}, {material[1]}, {material[2]}")
                    # aux = budget(element["budget"])
                    # st.subheader("Presupuesto estimado")
                    # if isinstance(aux, int):
                    #     st.write("$"+str(aux))
                    # else:
                    #     st.write(aux)
                    st.write("----------------")   
            except:
                st.write("No se ha podido acceder al historial...")    
        else:
            st.error(f"Error en la solicitud. Código de estado: {response.status_code}")
            st.write(response.text)

with open("static/css/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
image = Image.open('static/img/logo.jpeg')
st.image(image, width=120)
st.title("Apprende: Crear un taller")
search = st.text_input('Ingresa la descripción del taller')

if st.button("Enviar a API", key="enviar_a_api_button"):
    send_to_api(search)

if st.button("Historial de busquedas"):
    history()