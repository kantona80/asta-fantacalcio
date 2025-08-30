import pygame
import time

# =========================
# CONFIGURAZIONE DI GIOCO
# =========================
NUM_PLAYERS = 8
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FONT_SIZE = 48
TIMER_START = 6

# =========================
# INIZIALIZZAZIONE PYGAME
# =========================
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asta Fantacalcio")
font = pygame.font.SysFont(None, FONT_SIZE)
clock = pygame.time.Clock()

# =========================
# INIZIALIZZAZIONE JOYSTICK
# =========================
pygame.joystick.init()

joystick = None
joystick_connected = False

try:
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        joystick_connected = True
    else:
        print("Nessun joystick rilevato!")
except pygame.error as e:
    print(f"Errore inizializzazione joystick: {e}")

# =========================
# VARIABILI DI STATO ASTA
# =========================
current_bid = 0
last_bidder = None
timer = TIMER_START
auction_active = False
last_bid_time = time.time()

START_KEY = pygame.K_RETURN

# Stato precedente dei pulsanti (solo se joystick connesso)
prev_buttons = [False] * (joystick.get_numbuttons() if joystick_connected else 0)

# =========================
# FUNZIONI DI GESTIONE GRAFICA
# =========================
def draw_screen():
    """Disegna tutti gli elementi sullo schermo."""
    screen.fill((30, 30, 30))

    # Titolo
    title = font.render("Asta Fantacalcio", True, (255, 255, 0))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))

    # Offerta corrente
    bid_text = font.render(f"Offerta: {current_bid}", True, (255, 255, 255))
    screen.blit(bid_text, (50, 100))

    # Ultimo offerente
    bidder_text = font.render(f"Ultimo offerente: {last_bidder + 1 if last_bidder is not None else 'Nessuno'}", True, (255, 255, 255))
    screen.blit(bidder_text, (50, 150))

    # Timer
    timer_text = font.render(f"Timer: {int(timer)}", True, (255, 100, 100))
    screen.blit(timer_text, (50, 200))

    # Messaggi di stato
    if not joystick_connected:
        info = font.render("Nessun joystick connesso!", True, (255, 50, 50))
        screen.blit(info, (50, 300))
    elif not auction_active:
        info = font.render("Premi ENTER per iniziare", True, (100, 255, 100))
        screen.blit(info, (50, 300))

    pygame.display.flip()

# =========================
# FUNZIONI DI LOGICA ASTA
# =========================
def reset_auction():
    """Resetta i valori per iniziare una nuova asta."""
    global current_bid, last_bidder, timer, auction_active, last_bid_time
    current_bid = 0
    last_bidder = None
    timer = TIMER_START
    auction_active = True
    last_bid_time = time.time()

def end_auction():
    """Termina l'asta e mostra il vincitore."""
    global auction_active
    auction_active = False
    print(f"Asta conclusa! Vincitore: Giocatore {last_bidder + 1 if last_bidder is not None else 'Nessuno'} | Prezzo: {current_bid}")

def handle_bid(player_index):
    """Gestisce un rilancio da parte di un giocatore."""
    global current_bid, last_bidder, timer, last_bid_time
    now = time.time()
    if not auction_active:
        return
    if timer > 3 or (timer <= 2 and last_bidder != player_index):
        current_bid += 1
        last_bidder = player_index
        timer = TIMER_START
        last_bid_time = now
        print(f"Giocatore {player_index + 1} rilancia a {current_bid}")

# =========================
# LOOP PRINCIPALE DI GIOCO
# =========================
running = True
while running:
    clock.tick(30)
    now = time.time()

    # Aggiorna timer se asta attiva
    if auction_active:
        elapsed = now - last_bid_time
        timer = max(0, TIMER_START - elapsed)
        if timer == 0:
            end_auction()

    # Gestione eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == START_KEY and not auction_active and joystick_connected:
                reset_auction()

    # Gestione input joystick solo se connesso
    if joystick_connected:
        for i in range(joystick.get_numbuttons()):
            current = joystick.get_button(i)
            if current and not prev_buttons[i]:
                handle_bid(i)
            prev_buttons[i] = current

    # Disegna la schermata
    draw_screen()

pygame.quit()