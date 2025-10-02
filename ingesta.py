import mysql.connector
import csv
import boto3
import os

# Conectar a la base de datos MySQL
def get_mysql_connection():
    connection = mysql.connector.connect(
        host='localhost',  # Cambiar por la IP o nombre del host de la base de datos si no es local
        user='tu_usuario', # Usuario de MySQL
        password='tu_contraseña', # Contraseña de MySQL
        database='tu_base_de_datos' # Nombre de la base de datos
    )
    return connection

# Función para leer los registros de la tabla
def fetch_data_from_mysql():
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tu_tabla")  # Cambiar "tu_tabla" por el nombre de tu tabla
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

# Función para guardar los datos en un archivo CSV
def save_to_csv(data):
    with open('registros.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Escribir los nombres de las columnas
        writer.writerows(data)

# Función para subir el archivo CSV a S3
def upload_to_s3(bucket_name, file_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket_name, file_name)

# Función principal
def main():
    data = fetch_data_from_mysql()
    save_to_csv(data)
    upload_to_s3('tu-bucket-s3', 'registros.csv')  # Cambiar 'tu-bucket-s3' por el nombre de tu bucket S3
    print("Archivo CSV subido a S3 correctamente.")

if __name__ == "__main__":
    main()
