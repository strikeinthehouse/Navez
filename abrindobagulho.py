import requests
from bs4 import BeautifulSoup

# URL que queremos acessar
url = 'https://www.twitch.tv/search?term=gran%20hermano'

# Cabeçalho para simular um navegador Firefox
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
}

# Enviar a requisição HTTP
response = requests.get(url, headers=headers)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parsing do HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar os primeiros dois elementos
    elements = soup.find_all('a', class_='ScCoreLink-sc-16kq0mq-0 fPPzLm tw-link')[:2]
    
    # Abrir arquivo para escrita
    with open('channel_info.txt', 'w', encoding='utf-8') as file:
        for element in elements:
            # Extrair informações
            channel_name = element.text.strip()
            channel_url = f"https://twitch.tv{element['href']}"
            
            # Escrever no arquivo no formato especificado
            file.write(f"{channel_name} | | {channel_url}\n")
else:
    print(f'Falha ao acessar a URL. Código de status: {response.status_code}')
