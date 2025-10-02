import mysql.connector
import csv
import boto3
import os

# Conectar a la base de datos MySQL
def get_mysql_connection():
    connection = mysql.connector.connect(
        host='mysql_c',
        user='root', # Usuario de MySQL
        password='utec', # Contraseña de MySQL
        database='bd_api_employees' # Nombre de la base de datos
    )
    return connection

# Función para leer los registros de la tabla
def fetch_data_from_mysql():
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]  # Obtener los nombres de las columnas
    cursor.close()
    connection.close()
    return rows, columns

# Función para guardar los datos en un archivo CSV
def save_to_csv(data, columns):
    with open('registros.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Escribir los nombres de las columnas
        writer.writerows(data)    # Escribir los datos

# Función para subir el archivo CSV a S3
def upload_to_s3(bucket_name, file_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket_name, "ingesta/" + file_name)

# Función principal
def main():
    data = fetch_data_from_mysql()
    save_to_csv(data)
    upload_to_s3('joseph-s2-data', 'registros.csv') 
    print("Archivo CSV subido a S3 correctamente.")

if __name__ == "__main__":
    main()
