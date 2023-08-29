import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Función para obtener la cantidad de apariciones de una palabra clave en una plataforma
def obtener_cantidad(palabra_clave, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            texto = soup.get_text().lower()
            return texto.count(palabra_clave)
        else:
            print(f"No se pudo acceder a {url}")
            return 0
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return 0

# Obtener ubicación y fecha del usuario
ubicacion = input("Ingresa la ubicación (ciudad, país): ")
#fecha = input("Ingresa la fecha en formato YYYY-MM-DD: ")

# Palabras clave preconfiguradas relacionadas con desastres naturales
palabras_clave = input("Ingresa la(s) palabra(s) clave(s): ")

# URLs de búsqueda para diferentes plataformas
urls = {
    "Twitter": f"https://twitter.com/search?q={palabras_clave}%20near%3A%22{ubicacion}",
    "Facebook": f"https://www.facebook.com/search/posts/?q={palabras_clave}%20near%3A%22{ubicacion}",
    "TikTok": f"https://www.tiktok.com/tag/{palabras_clave}?lang=en",
    "Instagram": f"https://www.instagram.com/explore/tags/{palabras_clave}/",
    "YouTube": f"https://www.youtube.com/results?search_query={palabras_clave}%20{ubicacion}"
}

# Obtener cantidad de la palabra clave en diferentes plataformas
cantidades = {plataforma: sum(obtener_cantidad(palabra, url) for palabra in palabras_clave) for plataforma, url in urls.items()}

# Crear DataFrame con resultados
data = {"Plataforma": list(cantidades.keys()), "Cantidad": list(cantidades.values())}
df = pd.DataFrame(data)

# Crear subgráficos
fig, axs = plt.subplots(2, 2, figsize=(15, 12))

# Gráfico de barras
bar_chart = axs[0, 0].bar(cantidades.keys(), cantidades.values())
axs[0, 0].set_title(f"Artículos relacionados con {palabras_clave} en {ubicacion}")
axs[0, 0].set_xlabel("Plataforma")
axs[0, 0].set_ylabel("Cantidad")
axs[0, 0].tick_params(axis='x', rotation=45)

for bar in bar_chart:
    height = bar.get_height()
    axs[0, 0].annotate(f"{height}",
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom')

# Gráfico de torta
pie_chart = axs[0, 1].pie(cantidades.values(), labels=cantidades.keys(), autopct='%1.1f%%', startangle=140)
axs[0, 1].axis('equal')

for i, pie_slice in enumerate(pie_chart[0]):
    angle = (pie_slice.theta2 - pie_slice.theta1) / 2.0 + pie_slice.theta1
    x = pie_slice.r * 0.75 * np.cos(np.deg2rad(angle))
    y = pie_slice.r * 0.75 * np.sin(np.deg2rad(angle))
    axs[0, 1].text(x, y, f"{cantidades[list(cantidades.keys())[i]]}",
                   ha='center', va='center')

# Gráfico de líneas
line_chart = axs[1, 0].plot(list(cantidades.keys()), list(cantidades.values()), marker='o')
axs[1, 0].set_xlabel("Plataforma")
axs[1, 0].set_ylabel("Cantidad")
axs[1, 0].tick_params(axis='x', rotation=45)

for x, y in zip(list(cantidades.keys()), list(cantidades.values())):
    axs[1, 0].annotate(f"{y}",
                       xy=(x, y),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom')

# Mostrar tabla con resultados
axs[1, 1].axis('off')
tabla = axs[1, 1].table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1.2, 1.2)

# Ajustar espaciado entre subgráficos
plt.tight_layout()

# Mostrar todos los subgráficos
plt.show()