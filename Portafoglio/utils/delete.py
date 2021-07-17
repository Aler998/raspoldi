from time import sleep
from utils.loadNumber import loadNumber
import mysql.connector as mysql
from dotenv.main import dotenv_values
import os

config = dotenv_values(os.path.abspath(os.path.join('./.env')))


def deleteRecord():
    conn = mysql.connect(user=config['DB_USERNAME'], password=config['DB_PASSWORD'], host=config['DB_HOST'], database=config['DB_NAME'])
    cursor = conn.cursor()

    todel = ("SELECT * FROM transazioni ORDER BY id DESC LIMIT 1")
    cursor.execute(todel)

    for record in cursor:
        id = record[0]
        print("This row will be deleted:\nDescrizione: " + record[3] + "\nEuro: " + str(record[2]))

    cursor.close()

    c = conn.cursor()
    query = ("DELETE FROM transazioni WHERE id=" + str(id))
    c.execute(query)
    conn.commit()
    print('Deleted successfull')
    c.close()
    conn.close()
    loadNumber()