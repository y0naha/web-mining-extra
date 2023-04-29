import requests
import streamlit as st
import os
from dotenv import load_dotenv
import folium
from streamlit_folium import folium_static
import plotly.graph_objs as go
import pandas as pd

# Inicio da sidebar
st.sidebar.title("Atividade extra Web Mining")
st.sidebar.caption("Atividade extra para a faculdade Impacta.")
st.sidebar.caption("Veja o código base deste projeto [aqui](https://github.com/y0naha/web-mining-extra).")
st.sidebar.markdown("---")

st.sidebar.write(f"Made in <img src='https://streamlit.io/images/brand/streamlit-mark-color.png' width='25px'> by [Larissa Ionafa](https://www.linkedin.com/in/larissa-ionafa/)", unsafe_allow_html=True)
# Fim da sidebar


# VIA CEP
st.title("API Via CEP 🔎")
st.subheader("Localizador")
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
    m = folium.Map(location=[lat, lng], zoom_start=15)
    tooltip = "Aqui está a localização digitada"
    folium.Marker(
        [lat, lng], tooltip=tooltip
    ).add_to(m)
    folium_static(m)

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

st.divider()

# COTAÇÃO DE MOEDAS

st.title("API de Cotações 💰")
st.subheader("Cotação de moedas")

API_URL_MOEDA = "http://localhost:5000/cotacao/"

def get_currency_data(currency):
    url = API_URL_MOEDA + currency
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data

def get_currency_data_days(currency, days):
    url = API_URL_MOEDA + f"{currency}/{days}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data

def search_currency(currency_from, currency_to, amount):
    url = API_URL_MOEDA + f"{currency}"
    response = requests.get(url)
    data = response.json()
    rate = data['rates'][currency_to]
    converted_amount = amount * rate
    return f"{amount} {currency_from} = {converted_amount} {currency_to}"


currency = st.selectbox(
    "Selecione a moeda desejada:",
    ["USD-BRL", "EUR-BRL", "BTC-BRL", "ETH-BRL"]
)

if currency:
    try:
        currency_data = get_currency_data(currency)
        st.write("Moeda:", currency_data["currency_name"])
        st.write("Cotação máxima:", currency_data["max_value"])
        st.write("Cotação mínima:", currency_data["min_value"])
        st.write("Data:", currency_data["currency_date"])

        days = st.slider(
            "Selecione o número de dias para visualizar o histórico:",
            min_value=1,
            max_value=30,
            value=15,
        )

        currency_data_days = get_currency_data_days(currency, days)

        df = pd.DataFrame(currency_data_days)
        df["date"] = pd.to_datetime(df["date"])
        fig = go.Figure(data=go.Scatter(x=df["date"], y=df["value"]))
        fig.update_layout(title=f"Histórico de cotação da moeda {currency_data['currency_name']} nos últimos {days} dias")
        st.plotly_chart(fig)

    except ValueError as e:
        st.error(str(e))