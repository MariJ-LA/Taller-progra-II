# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 15:23:25 2024

@author: maria
"""
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

