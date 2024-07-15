# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 12:15:28 2024

@author: maria
"""

# Importar bliblioteca requests
import requests


# Guardar la URL del api , en este caso son datos de la serie juego de tronos
URL = "https://api.gameofthronesquotes.xyz/v1/houses"

# guardar la respuesta de la url en una variable
respuesta = requests.get(URL)

#Validación
if respuesta.status_code == 200:
    print('Solicitud exitosa')
    print('Datos:', respuesta.json())
else:
    print('Error en la solicitud de recurso. Detalles: \n',
          respuesta.text)
    
datos = respuesta.json()

# Funcion para buscar una casa en especifico y extraer los nombres de los miembros de esta casa
def buscar_miembros_por_slug(datos, slug_casa):
    for casa in datos:
        if casa['slug'] == slug_casa:
            return casa.get('members', []) 
    return None

# Buscar miembros de la casa "targaryen"
slug_casa = "targaryen"
miembros_casa = buscar_miembros_por_slug(datos, slug_casa)