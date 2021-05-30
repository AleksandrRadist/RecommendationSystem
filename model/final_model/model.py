import psycopg2
import pandas as pd

db_connect = psycopg2.connect(
    host='127.0.0.1',
    port='5432',
    database='reccomendation_system',
    user='aleks',
    password='qweasd'
)

cursor = db_connect.cursor()

select_transactions_data = 'SELECT * FROM analytics_transaction'
cursor.execute(select_transactions_data)
transaction_data = cursor.fetchall()
print(transaction_data)
