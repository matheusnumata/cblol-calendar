import requests
from datetime import datetime
from ics import Calendar, Event

url = "https://lol.fandom.com/api.php"
params = {
    "action": "cargoquery",
    "tables": "MatchSchedule",
    "fields": "Team1, Team2, DateTime_UTC, OverviewPage",
    "where": 'OverviewPage LIKE "CBLOL/2026%"',
    "limit": "500",
    "format": "json"
}

headers = {
    "User-Agent": "MeuCalendarioCBLOL/1.0 (matheus.numata@gmail.com)"
}

response = requests.get(url, params=params, headers=headers).json()
matches = response.get("cargoquery", [])

cal = Calendar()

for item in matches:
    match_data = item.get("title", {})
    
    # A API mapeia internamente o campo 'DateTime_UTC' com um espaço no JSON retornado
    start_time_raw = match_data.get("DateTime UTC")
    
    if not start_time_raw:
        continue
        
    team1 = match_data.get("Team1")
    team2 = match_data.get("Team2")
    overview_page = match_data.get("OverviewPage")

    # Pular jogos vazios ou não definidos (TBD)
    if not team1 or team1 == "TBD" or team2 == "TBD":
        continue

    event = Event()
    event.name = f"CBLOL: {team1} vs {team2}"
    
    try:
        # Converte a string UTC para objeto datetime nativo
        event.begin = datetime.strptime(start_time_raw, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        continue
        
    event.duration = {"hours": 1}
    event.description = f"Torneio: {overview_page}\nAssista ao vivo no YouTube/Twitch do CBLOL."
    
    cal.events.add(event)

# Salvar o arquivo iCal
with open("cblol_2026.ics", "w", encoding="utf-8") as f:
    f.writelines(cal.serialize_iter())

print(f"Sucesso! {len(cal.events)} jogos adicionados ao calendário.")