import os
import requests
import csv
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

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
# CLASSIFICAÇÃO
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