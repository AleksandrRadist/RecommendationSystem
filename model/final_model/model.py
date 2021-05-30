import psycopg2
import pandas as pd
import pandas.io.sql as sqlio

db_connect = psycopg2.connect(
    host='127.0.0.1',
    port='5432',
    database='reccomendation_system',
    user='aleks',
    password='qweasd'
)

# cursor = db_connect.cursor()

select_transactions_data = 'SELECT * FROM analytics_transaction'
# cursor.execute(select_transactions_data)
# transaction_data = cursor.fetchall()
transaction_data = sqlio.read_sql_query(select_transactions_data, db_connect)

print(transaction_data)
