from utils.display import display_string
from getFromTelegram import TGinactive, TGactive, sendMSG
import threading
from utils.loadNumber import loadNumber
from gpiozero import Button
from utils.speech import hearing
from utils.store import store
from utils.delete import deleteRecord
from gpiozero import LED

led = LED(23)
tg_btn = Button(22)
delete = Button(27)
button = Button(17)
buttonPressed = False
stop_threads = False
telegram_is_active = False

#funzione del thread di telegram
def getTG():
    while True:
        if telegram_is_active:
            #pin di telegram acceso
            #e effetuo chiamate API
            led.on()
            check = TGactive()
            if check is True:
                loadNumber()
        else:
            #pin telegram spento
            led.off()
            TGinactive()

#cambia lo stato di telegram quando 
#viene schiacciato il pulsante
def changeTG():
    global telegram_is_active
    if telegram_is_active:
        telegram_is_active = False
        sendMSG("Bot disattivato")
    else:
        telegram_is_active = True
        sendMSG("Bot Attivato")
  
#thread di telegram
tg_thread = threading.Thread(target=getTG)
tg_thread.daemon = True
tg_thread.start() 


while True:
    
    #Se il pulsante viene premuto allora fai qualcosa e alla fine 
    #emetti il segnale per far scattare l'evento
    if(buttonPressed):
        #pulsante che cancella l'ultimo inserimento vocale
        delete.when_pressed = deleteRecord
        #pulsante che cambia lo stato del thread di telegram
        tg_btn.when_pressed = changeTG
        #avvio dell'assistente vocale per farsi dire le spese o i guadagni
        button.wait_for_press()
        text = hearing()
        #manipolazione dei dati
        cod = store(text)
        if(cod == 300):
            print('Non ho capito')
            display_string("Non ho capito")
        #alla fine emetto l'evento che è stato schiacciato il bottone
        buttonPressed = False
    else:
        #Se il pulsante non viene premuto get dei dati e print del numero
        #get dei dati
        loadNumber()
        buttonPressed = True
