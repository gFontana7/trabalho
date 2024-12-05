import requests
from bs4 import BeautifulSoup
import re
import plotly.express as px

# Taxa de conversão de libras (£) para dólares ($) 
GBP_TO_USD = 1.25

def buscar_dados_wikipedia(jogo):
    url = f"https://en.wikipedia.org/wiki/{jogo.replace(' ', '_')}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        texto_completo = soup.get_text()  # Pega todo o texto da página

        # Tenta procurar por diferentes formas de expressar orçamento
        padrao = r"(Budget|Orçamento|budget|cost|estimated).*?([\$£€]\s?\d+[,\d]*)"
        correspondencias = re.findall(padrao, texto_completo)

        valores = []
        for _, valor in correspondencias:
            valor = valor.replace(',', '').strip()
            if '£' in valor:
                # Converte libras para dólares
                valor_em_dolares = round(float(valor.replace('£', '')) * GBP_TO_USD, 2)
                valores.append(valor_em_dolares)
            elif '$' in valor:
                valores.append(float(valor.replace('$', '').strip()))


        if valores:
            return valores[0]
    return None  

# Dicionário de valores complementares (Em Milhões)
dados_complementares = {
    "Cyberpunk 2077": 174,
    "counter strike go": 15, 
    "team fortress 2": 40, 
    "ark: survival evolved": 50,  
    "Assassin's Creed Odyssey": 100, 
    "Warhammer: Vermintide 2": 25, 
    "Dead by Daylight": 10,  
    "Destiny 2": 500, 
    "Monster Hunter: World": 200,  
    "Halo Infinite": 500
}

# Lista de jogos
jogos = [
    "Cyberpunk 2077", "Grand Theft Auto V", "Red Dead Redemption 2", "counter strike go", "pubg", "team fortress 2",
    "ark: survival evolved", "Stardew valley", "Assassin's Creed Odyssey", "Warhammer: Vermintide 2", "Dead by Daylight",
    "Destiny 2", "The Witcher 3", "Monster Hunter: World", "Halo Infinite"
]


valores_producao = []

for jogo in jogos:
    valor_producao = buscar_dados_wikipedia(jogo)
    
    # Usa valores complementares, se necessário
    if valor_producao is None and jogo in dados_complementares:
        valor_producao = dados_complementares[jogo]
    
    valores_producao.append(valor_producao)
    print(f"Jogo: {jogo}, Valor de Produção: {valor_producao}")



df = {
    "Jogo": jogos,
    "Valor de Produção (milhões de dólares)": valores_producao
}

fig = px.bar(df, 
             x="Valor de Produção (milhões de dólares)", 
             y="Jogo", 
             orientation='h', 
             title="Valor de Produção dos Jogos (em milhões de dólares)",
             labels={"Valor de Produção (milhões de dólares)": "Valor de Produção (em milhões de dólares)", "Jogo": "Nome do Jogo"},
             color="Valor de Produção (milhões de dólares)",
             color_continuous_scale="Viridis")


fig.show()
