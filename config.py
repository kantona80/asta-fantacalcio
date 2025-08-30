# config.py

# Numero di giocatori partecipanti all'asta
NUM_PLAYERS = 8  # Modificabile da 4 a 12

# Validazione del numero di giocatori
if not (4 <= NUM_PLAYERS <= 12):
    raise ValueError("NUM_PLAYERS deve essere compreso tra 4 e 12.")

# Dimensioni della finestra
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Dimensione del font
FONT_SIZE = 48

# Durata iniziale del timer in secondi
TIMER_START = 6  # Modificabile

# Tasto per avviare l'asta (ENTER)
START_KEY = 'RETURN'  # Puoi usare 'SPACE', 'TAB', ecc.
