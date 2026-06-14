import psycopg2

conn = psycopg2.connect(
    "postgresql://postgres:Alice%4016051983%40poa@db.zfpvfljmnlgsqiqdxmka.supabase.co:5432/postgres"
)

cursor = conn.cursor()

cursor.execute("SELECT version();")

print(cursor.fetchone())

cursor.close()
conn.close()