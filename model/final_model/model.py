import psycopg2
import pandas.io.sql as sqlio
from data_processing import data_processing
import warnings
warnings.filterwarnings('ignore')

db_connect = psycopg2.connect(
    host='127.0.0.1',
    port='5432',
    database='reccomendation_system',
    user='aleks',
    password='qweasd'
)

# cursor = db_connect.cursor()

select_clients_data = 'SELECT * FROM analytics_client'
select_categories_data = 'SELECT * FROM analytics_category'
select_transactions_data = 'SELECT * FROM analytics_transaction'

# cursor.execute(select_transactions_data)
# transaction_data = cursor.fetchall()
clients_data = sqlio.read_sql_query(select_clients_data, db_connect)
categories_data = sqlio.read_sql_query(select_categories_data, db_connect)
transaction_data = sqlio.read_sql_query(select_transactions_data, db_connect)

data = data_processing(clients_data, categories_data, transaction_data)
print(data)

db_connect = None
