import mysql.connector
import random

# Database connection details
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Renu-9694",
    database="opcua"
)

cursor = db.cursor()

status_options = ["idle", "runing", "error"]

total_records = 50  # Number of records you want to insert

for _ in range(total_records):
    temp = round(random.uniform(20.0, 100.0), 2)
    spindle_speed = round(random.uniform(500.0, 5000.0), 2)
    status = random.choice(status_options)

    sql = "INSERT INTO machine_data (temp, spindle_speed, status) VALUES (%s, %s, %s)"
    val = (temp, spindle_speed, status)
    cursor.execute(sql, val)

db.commit()
print(f"{total_records} records inserted.")

cursor.close()
db.close()
