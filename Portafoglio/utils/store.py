from utils.display import display, display_lines
from dotenv.main import dotenv_values
import datetime
import os
import mysql.connector as mysql

config = dotenv_values(os.path.abspath(os.path.join('./.env')))

today = datetime.datetime.today()
today_string = str(today.date())
rm = ["TOGLI", "RIMUOVI", "MENO", "TOGLIERE"]
add = ["AGGIUNGI", 'AGGIUNGERE', 'INSERIRE']


def store(text):
    #testo tipo :
    #1) Aggiungi 150 per aquisto amazon
    #2) Togli 150 per aquisto amazon
    try:
        arr = text.split()
    except Exception:
        return 300
    desc = False
    descrizione = ""
    for word in arr:
        if(desc):
            if(descrizione != ""):
                descrizione += " "
            descrizione += word
        if(word.upper() == "PER" or word == "*" or word.upper() == "X"):
            desc = True

    if not desc:
        print('Che minchia dici')
    elif(arr[0].upper() in rm):
        save((False, int(arr[1]), descrizione, today_string))
        return 200
    elif(arr[0].upper() in add):
        save((True, int(arr[1]), descrizione, today_string)) 
        return 200 
    else:
        print("Non ho capito bene")
        display("Non ho capito bene")


def save(obj):
    #vado a salvare in database
    conn = mysql.connect(user=config['DB_USERNAME'], password=config['DB_PASSWORD'], host=config['DB_HOST'], database=config['DB_NAME'])
    cursor = conn.cursor()
    add = ("INSERT INTO transazioni"
            "(tipo, euro, descrizione, created_at)"
            "VALUES (%s, %s, %s, %s)")

    cursor.execute(add, obj)

    if(obj[0]):
        print('Transazione: Aggiunta' + '\n' + 'Euro: ' + str(obj[1]) + '\n' + 'Descrizione: ' + obj[2] + '\n')
        display_lines(['Transazione: Aggiunta', 'Euro: ' + str(obj[1]), 'Descrizione: ' + obj[2]])
    else:
        print('Transazione: Togli' + '\n' + 'Euro: ' + str(obj[1]) + '\n' + 'Descrizione: ' + obj[2] + '\n')
        display_lines(['Transazione: Togli', 'Euro: ' + str(obj[1]), 'Descrizione: ' + obj[2]])
    
    conn.commit()
    cursor.close()
    conn.close()

