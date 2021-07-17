import os
import datetime
import mysql.connector as mysql
from dotenv.main import dotenv_values


config = dotenv_values(os.path.abspath(os.path.join('./.env')))

today = datetime.datetime.today()
filename = os.path.abspath(os.path.join('./datas/transactions/' + str(today.year) + '-' + str(today.month) + '.json'))


def getdatas():
    conn = mysql.connect(user=config['DB_USERNAME'], password=config['DB_PASSWORD'], host=config['DB_HOST'], database=config['DB_NAME'])
    cursor = conn.cursor()
    total = 0
    query = "SELECT tipo, euro FROM transazioni"
    cursor.execute(query)

    for row in cursor:
        if(row[0]):
            total += row[1]
        else:
            total -= row[1]

    query = "SELECT tipo, euro FROM transazioni_telegram"
    cursor.execute(query)

    for row in cursor:
        if(row[0]):
            total += row[1]
        else:
            total -= row[1]

    cursor.close()
    conn.close()
    return total