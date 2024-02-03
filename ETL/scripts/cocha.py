#!/usr/bin/env python
# coding: utf-8

# In[2]:


##pip install folium


# In[8]:


import folium
import os
import sys
sys.path.append("C:\\Users\\idaas\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\site-packages")

sys.stderr = open('error_log.txt', 'w')
# Coordenadas aproximadas del centro de Cochabamba
cochabamba_coords = [-17.3935, -66.1568]

# Crear un mapa centrado en Cochabamba
cochabamba_map = folium.Map(location=cochabamba_coords, zoom_start=10)

# Lista de coordenadas aproximadas de los departamentos en Cochabamba
departamentos_coords = {
    "Cochabamba": [-17.3935, -66.1568],
    "Arani": [-17.5669, -65.7553],
    "Arque": [-17.4386, -66.2606],
    "Ayopaya": [-17.5994, -65.7619],
    # Agrega el resto de los departamentos aquí
}

# Añadir marcadores para cada departamento
for departamento, coords in departamentos_coords.items():
    folium.Marker(location=coords, popup=departamento).add_to(cochabamba_map)

# Guardar el mapa como un archivo HTML en el directorio actual
map_filename = "cochabamba_map.html"
cochabamba_map.save(map_filename)

# Imprimir en la consola un mensaje y la ruta del mapa guardado
print(f"Mapa de Cochabamba creado con éxito. Guardado en: {os.path.abspath(map_filename)}")


# In[ ]: