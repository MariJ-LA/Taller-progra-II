
#---------------------------------Proyecto Final---------------------------------

""" María José Leiva Abarca"""

#Primera Parte : Web Scraping

# Importar las librerias nesesarias

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inicializar el driver de Chrome
driver = webdriver.Chrome()

# URL de la pagina
url = "https://www.scrapethissite.com/pages/forms"

#Navegar a la pagina
driver.get(url)

# Crear una lista vacia para guardar los datos
datos = []

# Obtener fila
equipos = driver.find_elements(By.CLASS_NAME, "team")

#Definir una función para la extraccion de datos
def extraer_datos() :
 equipos = driver.find_elements(By.CLASS_NAME, "team")
 for equipo in equipos:
     nombre = equipo.find_element(By.CLASS_NAME, "name").text
     anio = equipo.find_element(By.CLASS_NAME, "year").text
     victorias = equipo.find_element(By.CLASS_NAME, "wins").text
     derrotas = equipo.find_element(By.CLASS_NAME, "losses").text
     derrotas_tiempo_extra = equipo.find_element(By.CLASS_NAME, "ot-losses").text
     porcentaje_victorias = equipo.find_element(By.CLASS_NAME, "pct").text
     goles_favor = equipo.find_element(By.CLASS_NAME, "gf").text
     goles_contra = equipo.find_element(By.CLASS_NAME, "ga").text
     gol_diferencia = equipo.find_element(By.CLASS_NAME, "diff").text

     datos.append({
         "Nombre": nombre,
         "Año": anio,
         "Victorias": victorias,
         "Derrotas": derrotas,
         "Derrotas tiempo extra": derrotas_tiempo_extra,
         "% Victorias": porcentaje_victorias,
         "Goles a favor": goles_favor,
         "Goles en contra": goles_contra,
         "Gol diferencia": gol_diferencia
     })
 

#Extraer datos de todas las paginas


while True:
    # Esperar a que la tabla se cargue completamente
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "team")))

   

    # Intentar ir a la siguiente página
    try:
        next_button = driver.find_element(By.XPATH, "//a[@aria-label='Next']")
        if "disabled" in next_button.get_attribute("class"):
            break
        
        next_button.click()

    except: 
        
       break
   
    # Extraer datos de la página actual
    extraer_datos()

# Agregar los datos al DataFrame
df = pd.DataFrame(datos)

# Pasar el dataframe a un archivo tipo .csv
df.to_csv("hockey_teams_data.csv", index=False)




#-----------------------------Segunda Parte-----------------------------------

# Desarrollo de API

import sqlite3
from flask import Flask, jsonify
import os
import sys

app = Flask(__name__)
def inicializar_bd():
    """
    Inicializa la base de datos leyendo un archivo CSV y creando una tabla SQL.
    """
    try:
        directorio_actual = os.path.abspath(sys.argv[0])
        os.chdir(directorio_actual)
        # Lee el archivo CSV
        df = pd.read_csv('hockey_teams_data.csv')
        # Conecta a la base de datos SQLite
        conn = sqlite3.connect('hockey.db')
        # Crea la tabla 'Teams' a partir del DataFrame
        df.to_sql('Teams', conn, if_exists='replace', index=False)
        conn.close()
        print("Base de datos inicializada exitosamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")

# Inicializa la base de datos al inicio
inicializar_bd()

def obtener_conexion_bd():
    """
    Establece y retorna una conexión a la base de datos.
    """
    return sqlite3.connect('hockey.db')


@app.route('/year/<year>', methods=['GET'])
def obtener_por_anio(year):
    """
    Maneja la solicitud GET para obtener la información de todos los equipos del año indicado.
    """
    conn = obtener_conexion_bd()
    try:
        # Ejecuta la consulta SQL para obtener los equipos por año
        resultado = conn.execute("SELECT * FROM Teams WHERE [Año] = ?", (year,)).fetchall()
        if resultado: 
            # Obtiene los nombres de las columnas
            columnas = [description[0] for description in conn.execute("SELECT * FROM Teams LIMIT 1").description]
            # Convierte cada fila en un diccionario
            equipos = [dict(zip(columnas, row)) for row in resultado]
            return jsonify(equipos)
        else:
            return jsonify({"error": "No se encontraron equipos para el año indicado"}), 404
    finally:
        conn.close()

if __name__ == '__main__':
    # Inicia la aplicación Flask
    app.run(debug=False, port=5000)


