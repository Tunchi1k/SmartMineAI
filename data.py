import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector

#Connecting to MySQL database
def connect_to_mysql():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password ='Chintu@2003',
        database = 'predictions'
    )
#Uploading my CSV file to MYSQL
def upload_csv_to_mysql(csv_path):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    df = pd.read_csv(csv_path)
    for index, row in df.iterrows():
        cursor.execute(
            """INSERT INTO predictions (equipment_id, temperature, vibration, pressure, runtime_hours, fuel_rate, last_maintenance,failure) 
            VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
            """, (
                row['equipment_id'],
                row['temperature'],
                row['vibration'],
                row['pressure'],
                row['runtime_hours'],
                row['fuel_rate'],
                row['last_maintenance'],
                row['failure']
            ))

    conn.commit()
    conn.close()

#upload_csv_to_mysql('path_to_your_csv_file.csv')
upload_csv_to_mysql("equipment_data.csv")

print("Successfully Uploaded the data into the table")




