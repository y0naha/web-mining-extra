# Atividade extra Web Mining
Este é um projeto simples que utiliza a API do ViaCEP para obter os dados de endereço de um CEP e, em seguida, usa a API do Google Maps para obter as coordenadas do endereço e exibir em um mapa usando a biblioteca Plotly.

## Configurando o projeto
Antes de executar o projeto, é necessário configurar as [chaves de acesso às APIs do Google Maps](https://developers.google.com/maps/documentation/geocoding/cloud-setup?hl=pt-br#console_1) e do ViaCEP. Para isso, siga os seguintes passos:

1. Crie um arquivo .env na raiz do projeto.
2. Adicione as seguintes linhas ao arquivo .env:
```makefile
API_KEY_MAPS=SUA_CHAVE_DO_GOOGLE_MAPS_AQUI
```
3. Substitua SUA_CHAVE_DO_GOOGLE_MAPS_AQUI pela sua chave de acesso à API do Google Maps.

## Executando o projeto
Para executar o projeto, siga os seguintes passos:

1. Instale as dependências:

```python
pip install -r requirements.txt
```

2. Execute o servidor Flask que disponibiliza o endpoint da API ViaCEP:

```shell
streamlit api-flask.py
```

3. Em outro terminal, execute a aplicação Streamlit:

```shell
python script-extra.py
```

4. Digite o CEP desejado na caixa de texto e clique em "Enter" para buscar as informações de endereço e plotar a localização no mapa.
## Tecnologias usadas

- Python
- Streamlit
- Plotly
- Requests
- Google Maps API