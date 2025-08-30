# Importa le librerie necessarie
import pygame
import time
from config import NUM_PLAYERS, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_SIZE, TIMER_START, START_KEY

# Inizializza la libreria pygame
pygame.init()

# Crea la finestra principale
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asta Fantacalcio")

# Imposta il font per il testo a schermo
font = pygame.font.SysFont(None, FONT_SIZE)

# Crea un oggetto clock per controllare il framerate
clock = pygame.time.Clock()

# Converte il nome del tasto START_KEY (es. 'RETURN') nel codice pygame corrispondente
START_KEY = getattr(pygame, f'K_{START_KEY.lower()}')

# Inizializza il modulo joystick
pygame.joystick.init()

# Variabili per gestire il joystick (encoder USB)
joystick = None
joystick_connected = False

# Verifica se è presente almeno un joystick
try:
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        joystick_connected = True
    else:
        print("⚠ Nessun joystick rilevato!")
except pygame.error as e:
    print(f"Errore inizializzazione joystick: {e}")

# Variabili di stato per l'asta
current_bid = 0         # Offerta corrente
last_bidder = None      # Ultimo offerente (indice del giocatore)
timer = TIMER_START     # Timer iniziale
auction_active = False  # Stato dell'asta (attiva o no)
last_bid_time = time.time()  # Tempo dell'ultimo rilancio

# Stato precedente dei pulsanti (per rilevare il "click" e non la pressione continua)
prev_buttons = [False] * (joystick.get_numbuttons() if joystick_connected else 0)

# Funzione per disegnare l'interfaccia grafica
def draw_screen():
    screen.fill((30, 30, 30))  # Sfondo scuro

    # Titolo
    title = font.render("Asta Fantacalcio", True, (255, 255, 0))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

    # Offerta corrente
    bid_text = font.render(f"Offerta: {current_bid}", True, (255, 255, 255))
    screen.blit(bid_text, (50, 100))

    # Ultimo offerente
    bidder_text = font.render(
        f"Ultimo offerente: {last_bidder + 1 if last_bidder is not None else 'Nessuno'}",
        True, (255, 255, 255)
    )
    screen.blit(bidder_text, (50, 150))

    # Timer
    timer_text = font.render(f"Timer: {int(timer)}", True, (255, 100, 100))
    screen.blit(timer_text, (50, 200))

    # Messaggio di stato
    if not joystick_connected:
        info = font.render("⚠ Nessun joystick connesso!", True, (255, 50, 50))
        screen.blit(info, (50, 300))
    elif not auction_active:
        info = font.render("Premi ENTER per iniziare", True, (100, 255, 100))
        screen.blit(info, (50, 300))

    pygame.display.flip()  # Aggiorna lo schermo

# Funzione per avviare una nuova asta
def reset_auction():
    global current_bid, last_bidder, timer, auction_active, last_bid_time
    current_bid = 0
    last_bidder = None
    timer = TIMER_START
    auction_active = True
    last_bid_time = time.time()

# Funzione per terminare l'asta e stampare il vincitore
def end_auction():
    global auction_active
    auction_active = False
    print(f"Asta conclusa! Vincitore: Giocatore {last_bidder + 1 if last_bidder is not None else 'Nessuno'} | Prezzo: {current_bid}")

# Funzione per gestire un rilancio da parte di un giocatore
def handle_bid(player_index):
    global current_bid, last_bidder, timer, last_bid_time
    now = time.time()
    if not auction_active:
        return

    # Regole di rilancio:
    # - Se il timer è > 2 secondi: chiunque può rilanciare, anche lo stesso giocatore
    # - Se il timer è ≤ 2 secondi: solo un giocatore diverso dall'ultimo offerente può rilanciare
    if timer > 2 or (timer <= 2 and last_bidder != player_index):
        current_bid += 1
        last_bidder = player_index
        timer = TIMER_START
        last_bid_time = now
        print(f"Giocatore {player_index + 1} rilancia a {current_bid}")

# Loop principale del programma
running = True
while running:
    clock.tick(30)  # Limita il framerate a 30 FPS
    now = time.time()

    # Aggiorna il timer se l'asta è attiva
    if auction_active:
        elapsed = now - last_bid_time
        timer = max(0, TIMER_START - elapsed)
        if timer == 0:
            end_auction()

    # Gestione degli eventi (tastiera, chiusura finestra)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Avvia l'asta se si preme ENTER e il joystick è connesso
            if event.key == START_KEY and not auction_active and joystick_connected:
                reset_auction()

    # Gestione dei pulsanti del joystick
    if joystick_connected:
        for i in range(joystick.get_numbuttons()):
            current = joystick.get_button(i)
            # Rileva il "click" (pressione nuova) e non la pressione continua
            if current and not prev_buttons[i]:
                handle_bid(i)
            prev_buttons[i] = current

    # Disegna l'interfaccia grafica
    draw_screen()

# Chiude pygame alla fine del programma
pygame.quit()
