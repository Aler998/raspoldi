from utils.display import display
import speech_recognition as sr
import time
from gpiozero import LED

led = LED(24)
red = LED(25)

def hearing():
    # print(bcolors.OKGREEN + out)

    r = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            print("Sto ascoltando...")
            # display("In Ascolto...")
            led.on()
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, 3)
        
        print('Ho finito di ascoltare')
        led.off()
        # display("Finito")
        time.sleep(1)
    except sr.WaitTimeoutError:
        red.on()
        led.off()
        time.sleep(2)
        red.off()
        return 300

    if audio:
        try:
            response = r.recognize_google(audio, language="it-IT")
            if response is None:
                return 303
            print(response)
            return response
        except sr.UnknownValueError:
            return 304
        
