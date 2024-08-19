
#---------------------------------Proyecto Final---------------------------------
 
#Puntos 1 y 2 de la tercera parte

 
#Consumir el endpoint y transformarlos a formato pandas

import pandas as pd
import requests

# URL del endpoint de la API
url = 'http://localhost:5000/year/2011'

# Realizar la solicitud GET
response = requests.get(url)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    # Convertir los datos JSON a un DataFrame de Pandas
    data = response.json()
    df = pd.DataFrame(data)
    
    # Guardar el DataFrame como un archivo CSV
    df.to_csv('hockey_teams_2011.csv', index=False)
    
    # Mostrar las primeras filas del DataFrame
    print(df.head())
