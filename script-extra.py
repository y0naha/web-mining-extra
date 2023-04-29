import requests
import streamlit as st
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_MAPS = os.getenv("API_KEY_MAPS")
API_URL_CEP = "http://localhost:5000/cep/"


def get_address_data(cep):
    url = API_URL_CEP + cep
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if "erro" in data:
        raise ValueError("CEP inválido.")
    return data

def get_coordinates(address_str):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address_str}&key={API_KEY_MAPS}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if data["status"] != "OK":
        raise ValueError("Não foi possível obter as coordenadas.")
    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]

def plot_location_on_map(lat, lng):
    df = px.data.gapminder().query("year == 2007")
    df = df.drop(columns=["year", "pop", "continent"])
    df = df.rename(columns={"country": "Localidade"})
    df["lat"] = lat
    df["lon"] = lng
    fig = px.scatter_geo(df, lat="lat", lon="lon", hover_name="Localidade")
    st.plotly_chart(fig)

cep = st.text_input("Digite o CEP:")
if cep:
    try:
        address_data = get_address_data(cep)
        address_str = f"{address_data['logradouro']}, {address_data['bairro']}, {address_data['localidade']}, {address_data['uf']}"
        lat, lng = get_coordinates(address_str)
        plot_location_on_map(lat, lng)
        st.write("Endereço:", address_data["logradouro"])
        st.write("Bairro:", address_data["bairro"])
        st.write("Cidade:", address_data["localidade"])
        st.write("Estado:", address_data["uf"])
    except ValueError as e:
        st.error(str(e))
