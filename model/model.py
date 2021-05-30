import psycopg2

print('Connecting to the PostgreSQL database...')
db_connect = psycopg2.connect(
    host='127.0.0.1',
    port='5432',
    database='reccomendation_system',
    user='aleks',
    password='qweasd'
)

cursor = db_connect.cursor()

print('hi')
print('PostgreSQL database version:')
cursor.execute('SELECT version()')

db_version = cursor.fetchone()
print(db_version)

