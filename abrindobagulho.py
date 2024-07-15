import requests
from bs4 import BeautifulSoup

def obter_links_twitch(termo_busca):
    url = f"https://www.twitch.tv/search?term={termo_busca}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Fazendo a requisição HTTP GET
    response = requests.get(url, headers=headers)
    
    # Verifica se a requisição foi bem sucedida
    if response.status_code != 200:
        print(f"Erro ao acessar a página: Status code {response.status_code}")
        return []
    
    # Parseando o conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrando todos os elementos <a> que contêm links para transmissões ao vivo
    links = []
    for link in soup.find_all('a', {'data-a-target': 'preview-card-image-link'}):
        href = link.get('href')
        if href and '/live_' in href:
            links.append(f"https://www.twitch.tv{href}")
    
    return links

# Termo de busca para transmissões de "gran hermano"
termo_busca = "gran%20hermano"
links = obter_links_twitch(termo_busca)

# Exibindo os links encontrados
if links:
    print("Links das transmissões ao vivo:")
    for link in links:
        print(link)
else:
    print("Nenhuma transmissão ao vivo encontrada.")


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
