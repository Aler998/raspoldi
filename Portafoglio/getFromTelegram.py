import json
import time
from dotenv.main import dotenv_values
import os
import datetime
from mysql.connector import cursor
from mysql.connector.errors import Error
import requests
import mysql.connector as mysql

config = dotenv_values(os.path.abspath(os.path.join('.env')))


today = datetime.datetime.today()
add = ["/a", "/A", "/Add", "/ADD", "/add"]
rm = ["/r", "/R", "/rm", "/RM"]
dl = ["/d", "/delete", "/dl", "/del"]

def TGactive():
    url = "https://api.telegram.org/bot" + config["BOT_TOKEN"] + "/getUpdates"
    out = requests.get(url)
    dec = out.json()

    for update in dec['result']:
        if str(update["message"]["chat"]["id"]) == config["CHAT_ID"]:
            #split della string
            try:
                arr = update["message"]["text"].split()
            except KeyError:
                continue
            # print(arr)
            #controllo se c'è la descrizione
            desc = False
            descrizione = ""
            for word in arr:
                if(desc):
                    if(descrizione != ""):
                        descrizione += " "
                    descrizione += word
                if(word.upper() == "PER" or word == "*" or word.upper() == "X"):
                    desc = True
            
            if desc:
                if arr[0] in add:
                    try:
                        record = (update["update_id"], update["message"]["message_id"], update["message"]["from"]["username"], str(today.date()), True, int(arr[1]), descrizione)
                    except ValueError:
                        saveERR(update["update_id"], "ValueError", "Messaggio formattato male, probabilmente non hai messo il valore al secondo posto")
                        continue
                    tr = saveTGtransaction(record)
                elif arr[0] in rm:
                    try:
                        record = (update["update_id"], update["message"]["message_id"], update["message"]["from"]["username"], str(today.date()), False, int(arr[1]), descrizione)
                    except ValueError:
                        saveERR(update["update_id"], "ValueError", "Messaggio formattato male, probabilmente non hai messo il valore al secondo posto")
                        continue
                    tr = saveTGtransaction(record)
                else:
                    #invia un messaggio al bot di non ho capito
                    saveERR(update["update_id"], "Unknown command", "Comando Sconosciuto")
            else:
                saveERR(update["update_id"], "Missing Description", "Descrizione mancante")

    time.sleep(1)
    return tr
        

def TGinactive():
    time.sleep(1)


def saveTGtransaction(record):
    conn = mysql.connect(user=config['DB_USERNAME'], password=config['DB_PASSWORD'], host=config['DB_HOST'], database=config['DB_NAME'])
    cursor = conn.cursor()
    second = conn.cursor()
    exist = False
    #verifica che il record non sia già in db
    query = "SELECT update_id, message_id FROM transazioni_telegram ORDER BY id DESC LIMIT 50"
    cursor.execute(query)
    

    for r in cursor:
        if str(r[0]) == str(record[0]) or r[1] == str(record[1]):
            exist = True

    query = "SELECT update_id FROM telegram_errors ORDER BY id DESC LIMIT 15"
    second.execute(query)

    for r in second:
        if str(r[0]) == str(record[0]):
            exist = True

    #vado a salvare in database
    if not exist:
        add = ("INSERT INTO transazioni_telegram"
                "(update_id, message_id, username, date, tipo, euro, descrizione)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(add, record)
        conn.commit()
        #messaggio a telegram della transazione salvata
        if record[4]:
            txt = "Transazione\nTipo: Guadagno \nEuro: " + str(record[5]) + "\nDescrizione: " + record[6]
        else:
            txt = "Transazione\nTipo: Spesa \nEuro: " + str(record[5]) + "\nDescrizione: " + record[6]
        sendMSG(txt)
        
        
        cursor.close()
        conn.close()
        return True
    else:
        return

def sendMSG(txt):
    url = "https://api.telegram.org/bot" + config["BOT_TOKEN"] + "/sendMessage?chat_id=" + config["CHAT_ID"] + "&text=" + txt
    requests.get(url)

def saveERR(update_id, error_type, msg):
    conn = mysql.connect(user=config['DB_USERNAME'], password=config['DB_PASSWORD'], host=config['DB_HOST'], database=config['DB_NAME'])
    cursor = conn.cursor()

    exist = False
    query = "SELECT update_id FROM telegram_errors ORDER BY id DESC LIMIT 20"
    cursor.execute(query)

    for r in cursor:
        if str(r[0]) == str(update_id) :
            exist = True

    if not exist:
        err = (str(today.date()), error_type, update_id)
        add = ("INSERT INTO telegram_errors"
            "(date, error_type, update_id)"
            "VALUES (%s, %s, %s)")
        cursor.execute(add, err)
        conn.commit()
        sendMSG(msg)