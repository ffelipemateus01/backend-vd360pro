import psycopg2

connection = psycopg2.connect(
    dbname="vd360",
    user="postgres",
    password="Sivec@20",
    host="localhost",
    port="5432"
)

print("Connected successfully")