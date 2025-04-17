import os
from dotenv import load_dotenv
load_dotenv()

import requests
import csv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://v3.football.api-sports.io'

HEADERS = {
    'x-apisports-key': API_KEY
}

LEAGUE_ID = 71  # Brasileirão Série A
SEASON = 2023

# =====================
# JOGOS
# =====================
def get_fixtures():
    url = f"{BASE_URL}/fixtures"
    params = {'league': LEAGUE_ID, 'season': SEASON}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json().get('response', [])

def save_fixtures(data, filename='brasileirao_2023_jogos.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Match ID', 'Date', 'Home Team', 'Away Team', 'Score'])

        for match in data:
            fixture = match.get('fixture', {})
            teams = match.get('teams', {})
            goals = match.get('goals', {})

            writer.writerow([
                fixture.get('id', ''),
                fixture.get('date', ''),
                teams.get('home', {}).get('name', ''),
                teams.get('away', {}).get('name', ''),
                f"{goals.get('home', '')} - {goals.get('away', '')}"
            ])

# =====================
#  CLASSIFICAÇÃO
# =====================
def get_standings():
    url = f"{BASE_URL}/standings"
    params = {'league': LEAGUE_ID, 'season': SEASON}
    response = requests.get(url, headers=HEADERS, params=params)
    try:
        return response.json()['response'][0]['league']['standings'][0]
    except (KeyError, IndexError):
        return []

def save_standings(data, filename='brasileirao_2023_classificacao.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Posição', 'Time', 'Pontos', 'Jogos', 'Vitórias', 'Empates', 'Derrotas', 'Gols Pró', 'Gols Contra', 'Saldo'])

        for team in data:
            all_data = team['all']
            writer.writerow([
                team['rank'],
                team['team']['name'],
                team['points'],
                all_data['played'],
                all_data['win'],
                all_data['draw'],
                all_data['lose'],
                all_data['goals']['for'],
                all_data['goals']['against'],
                team['goalsDiff']
            ])

# =====================
# ARTILHARIA
# =====================
def get_topscorers():
    url = f"{BASE_URL}/players/topscorers"
    params = {'league': LEAGUE_ID, 'season': SEASON}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json().get('response', [])

def save_topscorers(data, filename='brasileirao_2023_artilharia.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Jogador', 'Time', 'Gols'])

        for player in data:
            player_data = player['player']
            stats = player['statistics'][0]
            writer.writerow([
                player_data['name'],
                stats['team']['name'],
                stats['goals']['total']
            ])

# =====================
# EXECUÇÃO
# =====================
if __name__ == "__main__":
    print("📅 Coletando jogos...")
    fixtures = get_fixtures()
    save_fixtures(fixtures)

    print("🏆 Coletando classificação...")
    standings = get_standings()
    save_standings(standings)

    print("⚽ Coletando artilharia...")
    topscorers = get_topscorers()
    save_topscorers(topscorers)

    print("✅ Todos os dados foram salvos com sucesso!")

    # =====================
    # DASHBOARD
    # =====================
    st.title("Dashboard Brasileirão 2023")

    # Carregar dados
    classificacao = pd.read_csv('brasileirao_2023_classificacao.csv')
    artilharia = pd.read_csv('brasileirao_2023_artilharia.csv')
    jogos = pd.read_csv('brasileirao_2023_jogos.csv')

    # Formatar datas para visualização amigável
    jogos['Date'] = pd.to_datetime(jogos['Date']).dt.strftime('%d/%m/%Y')

    # Filtros interativos
    st.sidebar.header("Filtros")
    times = classificacao['Time'].unique()
    time_selecionado = st.sidebar.selectbox("Selecione um time para ver os seus jogos", options=times)
    rodada_datas = jogos['Date'].unique()
    data_selecionada = st.sidebar.selectbox("Selecione uma data para ver os jogos do dia", options=rodada_datas)

    # Classificação
    st.header("Classificação")
    st.dataframe(classificacao)
    st.download_button("Baixar classificação", classificacao.to_csv(index=False), "classificacao.csv")

    # Gráfico de pontos por time
    fig1, ax1 = plt.subplots()
    ax1.bar(classificacao['Time'], classificacao['Pontos'], color='royalblue')
    plt.xticks(rotation=90)
    st.pyplot(fig1)

    # Saldo de gols por time
    st.subheader("Saldo de Gols por Time")
    fig_saldo, ax_saldo = plt.subplots()
    ax_saldo.bar(classificacao['Time'], classificacao['Saldo'], color='orange')
    plt.xticks(rotation=90)
    st.pyplot(fig_saldo)

    # Artilharia
    st.header("Top 10 Artilheiros")
    top10 = artilharia.sort_values('Gols', ascending=False).head(10)
    st.dataframe(top10)
    st.download_button("Baixar artilharia", artilharia.to_csv(index=False), "artilharia.csv")

    fig2, ax2 = plt.subplots()
    ax2.barh(top10['Jogador'], top10['Gols'], color='darkgreen')
    plt.gca().invert_yaxis()
    st.pyplot(fig2)

    # Jogos
    st.header("Jogos")
    st.dataframe(jogos)
    st.download_button("Baixar jogos", jogos.to_csv(index=False), "jogos.csv")

    # Filtro de jogos por time
    st.subheader(f"Jogos do {time_selecionado}")
    jogos_time = jogos[(jogos['Home Team'] == time_selecionado) | (jogos['Away Team'] == time_selecionado)]
    st.dataframe(jogos_time)

    # Filtro de jogos por data
    st.subheader(f"Jogos na data {data_selecionada}")
    jogos_data = jogos[jogos['Date'] == data_selecionada]
    st.dataframe(jogos_data)

    # Destaques
    st.header("Destaques")
    # Maior goleada
    jogos['Diff'] = jogos['Score'].apply(lambda x: abs(int(x.split('-')[0].strip()) - int(x.split('-')[1].strip())) if '-' in x else 0)
    maior_goleada = jogos.loc[jogos['Diff'].idxmax()]
    st.markdown(f"**Maior goleada:** {maior_goleada['Home Team']} {maior_goleada['Score']} {maior_goleada['Away Team']} em {maior_goleada['Date']}")
