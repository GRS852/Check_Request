import requests

url = "http://127.0.0.1:5000/domain"
response = requests.get(url)

if response.status_code == 200:
    print("Dados retornados pela API:")
    print(response.json())
else:
    print("Erro ao acessar a API:", response.status_code)
    print(response.text) 