from datetime import datetime, timedelta

# Constantes pour les jours de la semaine et les mois de l'année
DAYS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", 
          "août", "septembre", "octobre", "novembre", "décembre"]

# Liste d'alternance : 0 = entreprise, 1 = lycée
ALTERNANCE = [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 
              0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 
              1, 0, 0, 1, 1, 2, 2]  # 2: indicatif pour "no data" si besoin

# Date de référence pour l'alternance (par exemple, 1er septembre 2024)
START_DATE = datetime(2024, 9, 1)

# Fonction pour obtenir le jour et le mois en format "Jour, Mois"

# TODO RAJOUTER LE FORMAT ISO 8601 ?

def what_day_month(date):
    day_of_week = DAYS[date.weekday()]  # Récupère le jour de la semaine
    month = MONTHS[date.month - 1]  # Récupère le mois
    return f'{day_of_week} {date.day} {month}'

# Fonction pour calculer la semaine du mois
def week_of_month(date):
    first_day = date.replace(day=1)  # Premier jour du mois
    first_day_weekday = first_day.weekday()  # Jour de la semaine du premier jour
    return (date.day + first_day_weekday - 1) // 7 + 1

# Fonction pour compter le nombre de semaines écoulées depuis le 1er septembre 2024
def weeks_since_start(date):
    delta = date - START_DATE  # Différence en jours
    return delta.days // 7  # Convertir en semaines écoulées

# Fonction pour déterminer l'alternance de cette semaine et de la semaine suivante
def alternance_day():
    today = datetime.today()  # Date actuelle
    current_week_number = weeks_since_start(today)  # Semaines écoulées depuis le début de l'alternance
    current_alternance = ALTERNANCE[current_week_number % len(ALTERNANCE)]  # Alternance de cette semaine
    next_alternance = ALTERNANCE[(current_week_number + 1) % len(ALTERNANCE)]  # Alternance de la semaine suivante
    return current_alternance, next_alternance

# Exécution
today = datetime.today()  # Récupère la date actuelle
start_of_week = today - timedelta(days=today.weekday())  # Lundi de la semaine
end_of_week = start_of_week + timedelta(days=6)  # Dimanche de la semaine

# Test de la fonction
current_alternance, next_alternance = alternance_day()
print(f"Alternance (cette semaine, semaine suivante) : {current_alternance}, {next_alternance}")
