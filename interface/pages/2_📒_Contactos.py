import streamlit as st
import pandas as pd
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

with open("./static/css/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_contacts():
    api_url = "http://127.0.0.1:8000/contacts"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        st.success("Contactos ☎️")
        contacts_data = response.json()
        for element in contacts_data:
            if element["state"] == 0:
                contacts_data[contacts_data.index(element)]["state"] = "🕯️ Esperando respuesta..."
            elif element["state"] == 1:
                contacts_data[contacts_data.index(element)]["state"] = "🔔 Respuesta recibida..."
            elif element["state"] == 2:
                contacts_data[contacts_data.index(element)]["state"] = "🔇 Sin respuesta..."

            if element["decision"] == 0:
                contacts_data[contacts_data.index(element)]["decision"] = "🗂️ Sin decisión..."
            elif element["decision"] == 1:
                contacts_data[contacts_data.index(element)]["decision"] = "✅ Aceptado."
            elif element["decision"] == 2:
                contacts_data[contacts_data.index(element)]["decision"] = "🚫 Rechazado"
        df = pd.DataFrame(contacts_data)
        
        if 'id' in df.columns:
            df = df.drop(columns=['id'])
        df = df.reindex(columns=['name', 'email', 'state', 'decision'])
        return df
    else:
        st.error(f"Error en la solicitud. Código de estado: {response.status_code}")
        st.write(response.text)
        return pd.DataFrame()  

df = get_contacts()

if not df.empty:
    edited_df = st.data_editor(
        df,
        column_config={
            "name": "Nombre",
            "email": "Correo electrónico",
            "state": "Estado de respuesta",
            "decision": "Decisión"},
        hide_index=True,
        disabled=["name", "email"],
    )
else:
    st.write("No hay datos para mostrar.")