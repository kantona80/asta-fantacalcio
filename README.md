# 🎮 Asta Fantacalcio con Encoder USB

## 📌 Descrizione
Questo programma consente di gestire un'**asta di fantacalcio tra amici in presenza**, con un sistema di offerte e rilanci tramite **pulsanti fisici collegati a un encoder USB**.  
Ogni giocatore ha un pulsante dedicato: premendolo prima che il **timer** arrivi a zero, può effettuare un rilancio sull'offerta corrente.

L'interfaccia grafica mostra in tempo reale:
- L'offerta corrente
- L'ultimo offerente
- Il tempo rimanente
- Lo stato dell'asta (attiva o conclusa)

L'obiettivo è rendere l'asta più **coinvolgente, rapida e automatizzata**, eliminando la gestione manuale delle offerte.

---

## 🕹️ Requisiti hardware
- Un **encoder USB** (es. tipo Zero Delay o simili) riconosciuto dal sistema come joystick.
- Da **4 a 12 pulsanti fisici** collegati all'encoder, uno per ciascun giocatore.
- Schermo o proiettore per visualizzare l'interfaccia dell'asta.

⚠️ **Nota importante:**  
Il programma rileva l'encoder USB come un joystick. Se non è connesso, viene mostrato un messaggio di avviso e non sarà possibile effettuare rilanci.

---

## 👥 Numero di giocatori
- Il numero di giocatori è **configurabile** nel codice tramite la variabile `NUM_PLAYERS`.
- Di default, il programma è impostato per **8 giocatori**.
- Può essere modificato facilmente da **4 fino a 12**, in base al numero di pulsanti disponibili sull'encoder.

---

## ⚙️ Funzionalità principali
- Gestione di rilanci tramite pulsanti fisici.
- Timer per rilanci automatici.
- Visualizzazione grafica dell'asta.
- Messaggio di avviso se l'encoder non è rilevato.
- Log a console dei rilanci e del vincitore.

---

## 🎮 Flusso di gioco

1. Premi il tasto **ENTER** sulla tastiera per avviare una nuova asta.
2. Una volta avviata, ogni giocatore può effettuare rilanci premendo il proprio pulsante collegato all'encoder USB.
3. Ogni pressione del pulsante aumenta l'offerta di **+1** e riporta il timer al valore iniziale.
4. Il giocatore può premere **più volte il pulsante** per rilanciare di più rispetto all'offerta precedente (es. se l'offerta corrente è 5 e vuole offrire 10, deve premere 5 volte).
5. Il comportamento dei rilanci è regolato dal **timer**:
   - ⏱️ Se il timer è **maggiore di 2 secondi**, **qualsiasi giocatore** può rilanciare, anche lo stesso offerente più volte di seguito al fine di alzare la sua offerta iniziale.
   - ⏱️ Se il timer è **uguale o inferiore a 2 secondi**, **solo un altro giocatore** (diverso dall'ultimo offerente) può effettuare un rilancio.
6. Se il timer arriva a **0**, l'asta si chiude e viene dichiarato il vincitore con l'offerta più alta.

---

## 📦 Librerie e ambiente richiesto

### ✅ Versione minima di Python
- **Python 3.6 o superiore**  
  (necessaria per la compatibilità con la libreria `pygame`)

### 📚 Librerie necessarie
- [pygame](https://www.pygame.org/) – per la gestione di grafica, eventi e input da joystick.

Installa pygame con:
```bash
pip3 install pygame


## 🚀 Come eseguire

1. Clona il repository:
   ```bash
   git clone https://github.com/kantona80/asta-fantacalcio/
2. Entra nella cartella di progetto:
  cd asta-fantacalcio
3. Installa le dipendenze
  pip3 install -r requirements.txt
4. Avvia il programma
  python3 asta_fantacalcio.py
