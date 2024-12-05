import requests
import pandas as pd
import plotly.express as px

def buscar_dados_steam_spy(appid):
    url = "https://steamspy.com/api.php"
    params = {'request': 'appdetails', 'appid': appid}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Resposta inválida da API para AppID {appid}: {response.text}")
            return None
    else:
        print(f"Erro ao acessar Steam Spy para o AppID {appid}: {response.status_code}")
        return None

# IDs e nomes dos jogos para busca
jogos = [
    {"appid": 1091500, "nome": "Cyberpunk 2077"},
    {"appid": 271590, "nome": "GTA V"},
    {"appid": 730, "nome": "CS: GO"},
    {"appid": 578080, "nome": "PUBG"},
    {"appid": 440, "nome": "Team Fortress 2"},
    {"appid": 1174180, "nome": "Red Dead Redemption 2"},
    {"appid": 346110, "nome": "ARK: Survival Evolved"},
    {"appid": 413150, "nome": "Stardew Valley"},
    {"appid": 812140, "nome": "Assassin's Creed Odyssey"},
    {"appid": 552500, "nome": "Warhammer: Vermintide 2"},
    {"appid": 381210, "nome": "Dead by Daylight"},
    {"appid": 1085660, "nome": "Destiny 2"},
    {"appid": 292030, "nome": "The Witcher 3: Wild Hunt"},
    {"appid": 582010, "nome": "Monster Hunter: World"},
    {"appid": 1190460, "nome": "Halo Infinite"}
]

dados_jogos = []

# Buscar dados para cada jogo
for jogo in jogos:
    print(f"Buscando dados para {jogo['nome']}...")
    dados = buscar_dados_steam_spy(jogo["appid"])
    if dados:
        preco_atual = dados.get("price", 0)
        if isinstance(preco_atual, str):
            try:
                preco_atual = float(preco_atual)
            except ValueError:
                preco_atual = 0

        # Adicionar dados relevantes na lista
        dados_jogos.append({
            "Nome": dados.get("name", "N/A"),
            "Desenvolvedor": dados.get("developer", "N/A"),
            "Publicador": dados.get("publisher", "N/A"),
            "Gêneros": dados.get("genre", "N/A"),
            "Proprietários Estimados": dados.get("owners", "N/A"),
            "Pico Recente de Jogadores": dados.get("ccu", 0),
            "Preço Atual (USD)": round(preco_atual / 100, 2),
        })
    else:
        print(f"Não foi possível obter dados para {jogo['nome']}.")
    print("-" * 50)

# Adicionar manualmente as plataformas
for jogo in dados_jogos:
    if "Cyberpunk" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "PlayStation 4", "PlayStation 5", "Xbox One"]
    elif "GTA" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "PlayStation 3", "PlayStation 4", "PlayStation 5", "Xbox 360", "Xbox One"]
    elif "CS: GO" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "Linux", "Mac"]
    elif "PUBG" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "Xbox One", "PlayStation 4"]
    elif "Team Fortress 2" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "Mac", "Linux"]
    elif "Red Dead Redemption" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "PlayStation 4", "Xbox One"]
    elif "ARK" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "Mac", "Linux", "PlayStation 4", "Xbox One", "Nintendo Switch"]
    elif "Stardew" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "Mac", "Linux", "PlayStation 4", "Xbox One", "Nintendo Switch"]
    elif "Assassin's Creed Odyssey" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "PlayStation 4", "Xbox One"]
    elif "Warhammer: Vermintide 2" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "Xbox One", "PlayStation 4"]
    elif "Dead by Daylight" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "PlayStation 4", "PlayStation 5", "Xbox One", "Nintendo Switch"]
    elif "Destiny 2" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "PlayStation 4", "PlayStation 5", "Xbox One"]
    elif "The Witcher 3" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "PlayStation 4", "PlayStation 5", "Xbox One", "Nintendo Switch"]
    elif "Monster Hunter: World" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "PlayStation 4", "Xbox One"]
    elif "Halo Infinite" in jogo["Nome"]:
        jogo["Plataformas"] = ["Windows", "Xbox One"]
    else:
        jogo["Plataformas"] = ["Windows"]


# Converter dados para DataFrame
df = pd.DataFrame(dados_jogos)

# Limpar dados de proprietários estimados
df['Proprietários Estimados'] = df['Proprietários Estimados'].apply(
    lambda x: int(x.split()[0].replace(',', '')) if isinstance(x, str) else 0
)

df['Nota Crítica Especializada'] = [
    86, 96, 83, 85, 92, 93, 70, 89, 83, 82, 78, 87, 93, 88, 80
]
df['Avaliação Jogadores'] = [
    78, 96, 87, 84, 90, 91, 65, 96, 86, 80, 75, 88, 94, 89, 79
]

# Gráfico 1: Comparando o preço dos jogos
grafico1 = px.bar(
    df,
    x="Nome",
    y="Preço Atual (USD)",
    title="Preço Atual dos Jogos (em USD)",
    labels={"Preço Atual (USD)": "Preço (USD)", "Nome": "Jogos"},
    text="Preço Atual (USD)"
)
grafico1.update_traces(textposition="outside")

# Gráfico 2: Distribuição de Proprietários Estimados por Gênero
df_generos = df.explode("Gêneros")
generos_proprietarios = df_generos.groupby("Gêneros")["Proprietários Estimados"].sum().reset_index()
grafico2 = px.pie(
    generos_proprietarios,
    values="Proprietários Estimados",
    names="Gêneros",
    title="Distribuição de Proprietários Estimados por Gênero"
)

# Gráfico 3: Relação entre Preço e Pico Recente de Jogadores
grafico3 = px.line(
    df,
    x="Preço Atual (USD)",
    y="Pico Recente de Jogadores",
    text="Nome",
    title="Preço vs Pico Recente de Jogadores",
    labels={"Preço Atual (USD)": "Preço (USD)", "Pico Recente de Jogadores": "Pico de Jogadores"}
)
grafico3.update_traces(mode="markers+text", textposition="top center")

# Gráfico 4: Comparação de Proprietários Estimados por Jogo
grafico4 = px.bar(
    df,
    x="Nome",
    y="Proprietários Estimados",
    title="Proprietários Estimados por Jogo",
    labels={"Proprietários Estimados": "Proprietários Estimados", "Nome": "Jogos"},
    text="Proprietários Estimados"
)

# Gráfico 5: Distribuição de Jogos por Plataforma
df_plataformas = df.explode("Plataformas")
plataformas_jogos = df_plataformas.groupby("Plataformas")["Nome"].count().reset_index()
plataformas_jogos.rename(columns={"Nome": "Quantidade de Jogos"}, inplace=True)

grafico5 = px.bar(
    plataformas_jogos,
    x="Plataformas",
    y="Quantidade de Jogos",
    title="Distribuição de Jogos por Plataforma",
    labels={"Quantidade de Jogos": "Quantidade de Jogos", "Plataformas": "Plataformas"},
    text="Quantidade de Jogos"
)
grafico5.update_traces(textposition="outside")

# Gráfico 6: Relação entre Pico de Jogadores e Lucro Estimado
df['Lucro Estimado (USD)'] = df['Proprietários Estimados'] * df['Preço Atual (USD)']
grafico6 = px.scatter(
    df,
    x="Pico Recente de Jogadores",
    y="Lucro Estimado (USD)",
    size="Lucro Estimado (USD)",
    color="Nome",
    title="Relação entre Pico de Jogadores e Lucro Estimado",
    labels={
        "Pico Recente de Jogadores": "Pico Recente de Jogadores",
        "Lucro Estimado (USD)": "Lucro Estimado (USD)"
    },
    hover_name="Nome",
    text="Nome"
)
grafico6.update_traces(textposition="top center")

# Gráfico 7: Relação entre Nota de Críticas Especializadas e Avaliações dos Jogadores
grafico7 = px.scatter(
    df,
    x="Nota Crítica Especializada",
    y="Avaliação Jogadores",
    text="Nome",
    title="Relação entre Nota de Críticas Especializadas e Avaliações dos Jogadores",
    labels={
        "Nota Crítica Especializada": "Nota de Críticas Especializadas",
        "Avaliação Jogadores": "Avaliação dos Jogadores"
    },
    hover_name="Nome",
    trendline="ols"  # Adiciona uma linha de tendência
)
grafico7.update_traces(textposition="top center")

# Mostrar os gráficos
grafico1.show()
grafico2.show()
grafico3.show()
grafico4.show()
grafico5.show()
grafico6.show()
grafico7.show()
