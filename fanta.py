import pygame
import time
from config import NUM_PLAYERS, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_SIZE, TIMER_START, START_KEY

# Inizializza pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asta Fantacalcio")
font = pygame.font.SysFont(None, FONT_SIZE)
clock = pygame.time.Clock()

# Converte il nome del tasto START_KEY in codice pygame
START_KEY = getattr(pygame, f'K_{START_KEY.lower()}')

# Inizializza joystick (encoder USB)
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

# Stato asta
current_bid = 0
last_bidder = None
timer = TIMER_START
auction_active = False
last_bid_time = time.time()

# Stato precedente dei pulsanti
prev_buttons = [False] * (joystick.get_numbuttons() if joystick_connected else 0)

def draw_screen():
    screen.fill((30, 30, 30))

    title = font.render("Asta Fantacalcio", True, (255, 255, 0))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

    bid_text = font.render(f"Offerta: {current_bid}", True, (255, 255, 255))
    screen.blit(bid_text, (50, 100))

    bidder_text = font.render(
        f"Ultimo offerente: {last_bidder + 1 if last_bidder is not None else 'Nessuno'}",
        True, (255, 255, 255)
    )
    screen.blit(bidder_text, (50, 150))

    timer_text = font.render(f"Timer: {int(timer)}", True, (255, 100, 100))
    screen.blit(timer_text, (50, 200))

    if not joystick_connected:
        info = font.render("Nessun joystick connesso!", True, (255, 50, 50))
        screen.blit(info, (50, 300))
    elif not auction_active:
        info = font.render("Premi ENTER per iniziare", True, (100, 255, 100))
        screen.blit(info, (50, 300))

    pygame.display.flip()

def reset_auction():
    global current_bid, last_bidder, timer, auction_active, last_bid_time
    current_bid = 0
    last_bidder = None
    timer = TIMER_START
    auction_active = True
    last_bid_time = time.time()

def end_auction():
    global auction_active
    auction_active = False
    print(f"Asta conclusa! Vincitore: Giocatore {last_bidder + 1 if last_bidder is not None else 'Nessuno'} | Prezzo: {current_bid}")

def handle_bid(player_index):
    global current_bid, last_bidder, timer, last_bid_time
    now = time.time()
    if not auction_active:
        return
    # Regole di rilancio:
    # - Timer > 2: chiunque può rilanciare
    # - Timer <= 2: solo un giocatore diverso dall'ultimo offerente può rilanciare
    if timer > 2 or (timer <= 2 and last_bidder != player_index):
        current_bid += 1
        last_bidder = player_index
        timer = TIMER_START
        last_bid_time = now
        print(f"Giocatore {player_index + 1} rilancia a {current_bid}")

# Loop principale
running = True
while running:
    clock.tick(30)
    now = time.time()

    if auction_active:
        elapsed = now - last_bid_time
        timer = max(0, TIMER_START - elapsed)
        if timer == 0:
            end_auction()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == START_KEY and not auction_active and joystick_connected:
                reset_auction()

    if joystick_connected:
        for i in range(joystick.get_numbuttons()):
            current = joystick.get_button(i)
            if current and not prev_buttons[i]:
                handle_bid(i)
            prev_buttons[i] = current

    draw_screen()

pygame.quit()
