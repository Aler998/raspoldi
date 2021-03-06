from utils.loadNumber import loadNumber
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

    if(type(text) != str):
        return 300

    if(text.upper() == "REPORT"):
        loadNumber()
        return

    try:
        arr = text.split()
    except Exception:
        return 300

    desc, end = False
    descrizione = ""
    for word in arr:
        if(desc):
            if(descrizione != ""):
                descrizione += " "
            if(word.upper() == "IN"):
                end = True
            if not end:
                descrizione += word
        if(word.upper() == "PER" or word == "*" or word.upper() == "X"):
            desc = True

    cat = False
    categoria = ""
    for word in arr:
        if(cat):
            if(categoria != ""):
                categoria += " "
            categoria += word
        if(word.upper() == "IN"):
            cat = True

    if not desc:
        print('Descrizione mancante')
    elif not cat:
        print('Categoria mancante')
    elif(arr[0].upper() in rm):
        save((False, int(arr[1]), descrizione, today_string, categoria))
        return 200
    elif(arr[0].upper() in add):
        save((True, int(arr[1]), descrizione, today_string, categoria)) 
        return 200 
    else:
        print("Non ho capito bene")
        display("Non ho capito bene")


def save(obj):
    #vado a salvare in database
    conn = mysql.connect(user=config['DB_USERNAME'], password=config['DB_PASSWORD'], host=config['DB_HOST'], database=config['DB_NAME'])
    cursor = conn.cursor()
    add = ("INSERT INTO transazioni"
            "(tipo, euro, descrizione, created_at, categoria)"
            "VALUES (%s, %s, %s, %s, %s)")

    cursor.execute(add, obj)

    if(obj[0]):
        print('Transazione: Aggiunta' + '\n' + 'Euro: ' + str(obj[1]) + '\n' + 'Categoria: ' + obj[4] + '\n')
        display_lines(['Transazione: Aggiunta', 'Euro: ' + str(obj[1]), 'Categoria: ' + obj[4]])
    else:
        print('Transazione: Togli' + '\n' + 'Euro: ' + str(obj[1]) + '\n' + 'Categoria: ' + obj[4] + '\n')
        display_lines(['Transazione: Togli', 'Euro: ' + str(obj[1]), 'Categoria: ' + obj[4]])
    
    conn.commit()
    cursor.close()
    conn.close()

