import psycopg2

print('Connecting to the PostgreSQL database...')
db_connect = psycopg2.connect(
    host='localhost',
    database='reccomendation_system',
    user='Aleksandr',
    password='qweasd'
)

cursor = db_connect.cursor()

print('PostgreSQL database version:')
cursor.execute('SELECT version()')


