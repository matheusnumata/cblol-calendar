import requests
from datetime import datetime
from ics import Calendar, Event

# 1. Configurar os parâmetros da API da Leaguepedia
url = "https://lol.fandom.com/api.php"
params = {
    "action": "cargoquery",
    "tables": "MatchSchedule",
    "fields": "Team1, Team2, DateTime_UTC, OverviewPage",
    "where": 'OverviewPage LIKE "CBLOL/2026%"',
    "limit": "500",
    "format": "json"
}

# Definir um User-Agent limpo (obrigatório pela política da Fandom)
headers = {
    "User-Agent": "CBLOLCalendarGenerator/1.0 (matheus.numata@gmail.com)"
}

response = requests.get(url, params=params, headers=headers).json()
matches = response.get("cargoquery", [])

cal = Calendar()

# 2. Processar os jogos retornados
for item in matches:
    match_data = item.get("title", {})
    
    # Validar se o jogo possui data definida (evita partidas TBD)
    if not match_data.get("DateTime UTC"):
        continue
        
    team1 = match_data.get("Team1")
    team2 = match_data.get("Team2")
    start_time_raw = match_data.get("DateTime UTC")
    stage = match_data.get("OverviewPage").split("/")[-1] # Ex: Split 1 ou Split 2

    # Criar o evento no calendário
    event = Event()
    event.name = f"CBLOL: {team1} vs {team2}"
    
    # Converter a string de data UTC da API para objeto datetime
    event.begin = datetime.strptime(start_time_raw, "%Y-%m-%d %H:%M:%S")
    event.duration = {"hours": 1} # Duração aproximada por série/partida
    event.description = f"Torneio: CBLOL 2026 ({stage})\nDados obtidos via Leaguepedia."
    
    cal.events.add(event)

# 3. Salvar o arquivo iCal
with open("cblol_2026.ics", "w", encoding="utf-8") as f:
    f.writelines(cal.serialize_iter())

print(f"Sucesso! {len(cal.events)} jogos adicionados ao calendário.")