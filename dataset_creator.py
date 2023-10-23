import os
import requests
from bs4 import BeautifulSoup
import random
import re

# URL de Google Images
google_image = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&"

# Agrega un encabezado de usuario para evitar bloqueos
user_agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

# Directorio de salida para guardar las imágenes y etiquetas
output_dataset_folder = 'movie_dataset'

# Función principal
def main():
    if not os.path.exists(output_dataset_folder):
        os.mkdir(output_dataset_folder)
    if not os.path.exists(os.path.join(output_dataset_folder, 'train')):
        os.mkdir(os.path.join(output_dataset_folder, 'train'))
    if not os.path.exists(os.path.join(output_dataset_folder, 'test')):
        os.mkdir(os.path.join(output_dataset_folder, 'test'))

    # Leer los nombres de las películas desde un archivo de texto con codificación utf-8
    with open('movies.txt', 'r', encoding='utf-8') as file:
        movie_names = [line.strip() for line in file]

    for movie_name in movie_names:
        download_movie_images(movie_name)

# Función para organizar imágenes en train y test
def organize_images_for_train_test(movie_name, links):
    # Eliminar caracteres no válidos del nombre de la película
    movie_name_cleaned = re.sub(r'[<>:"/\\|?*]', '', movie_name)

    # Dividir aleatoriamente los índices de imágenes en train y test
    random.shuffle(links)
    n_total = len(links)
    n_train = n_total // 2

    for i, link in enumerate(links):
        folder = 'train' if i < n_train else 'test'

        # Crear la carpeta si no existe
        folder_path = os.path.join(output_dataset_folder, folder, movie_name_cleaned)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        image_name = os.path.join(folder_path, str(i + 1) + '.jpg')

        with open(image_name, 'wb') as fh:
            response = requests.get(link)
            fh.write(response.content)


# Función para descargar imágenes
def download_movie_images(movie_name):
    n_images = 500

    # Formatear el nombre de la película para la URL
    formatted_movie_name = movie_name.replace(" ", "+")
    
    # URL de búsqueda en IMDb
    imdb_search_url = f"https://www.imdb.com/find?q={formatted_movie_name}"
    print(imdb_search_url)
    # Realizar una solicitud HTTP para obtener la página de resultados
    response = requests.get(imdb_search_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = response.text
    # Crear un objeto BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    if movie_name == "El señor de los anillos: El retorno del rey":
        a_tag = soup.find_all('a', {'class': 'ipc-metadata-list-summary-item__t'})[1]
    elif movie_name == "El padrino":     
        a_tag = soup.find_all('a', {'class': 'ipc-metadata-list-summary-item__t'})[0]
    elif movie_name == "Titanic":     
        a_tag = soup.find_all('a', {'class': 'ipc-metadata-list-summary-item__t'})[0]
    elif movie_name == "El caballero oscuro":
        a_tag = soup.find_all('a', {'class': 'ipc-metadata-list-summary-item__t'})[0]

    # Verificar si se encontró una etiqueta <a>
    if a_tag:
        # Obtener el enlace IMDb
        imdb_link = "https://www.imdb.com" + a_tag['href']
        print(imdb_link)
        response = requests.get(imdb_link, headers={'User-Agent': 'Mozilla/5.0'})
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        a_tag = soup.find('a', {'data-testid': 'hero__photo-link'})
        print(a_tag)
        imdb_film = "https://www.imdb.com" + a_tag['href']

        # Ahora vamos a la galería de imágenes
        response = requests.get(imdb_film, headers={'User-Agent': 'Mozilla/5.0'})
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        a_tag = soup.find('a', {'data-testid': 'mv-gallery-button'})
        imdb_film_gallery = "https://www.imdb.com" + a_tag['href']
        print(imdb_film_gallery)

        # Realizar una solicitud HTTP para acceder a la página de la galería de IMDb
        gallery_page = requests.get(imdb_film_gallery, headers={'User-Agent': 'Mozilla/5.0'})
        gallery_html = gallery_page.text

        gallery_soup = BeautifulSoup(gallery_html, 'html.parser')

        # Obtenemos en numero de paginas de la galeria. La longitud de items de <span> es igual al numero de paginas
        pages = gallery_soup.find_all('span', {'class': 'page_list'})
        # Buscar las <a> de las paginas
        pages = pages[0].find_all('a')
        # El numero de paginas es igual a la longitud de items de <a>
        pages = len(pages)+1
        print(pages)
        image_tags = gallery_soup.find('div', class_='media_index_thumb_list').find_all('img')

        # Por cada pagina, buscamos las imagenes
        for i in range(2, pages + 1):
            url = imdb_film_gallery + '?page=' + str(i)
            gallery_page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            gallery_html = gallery_page.text
            gallery_soup = BeautifulSoup(gallery_html, 'html.parser')
            image_tags += gallery_soup.find('div', class_='media_index_thumb_list').find_all('img')

    count = 1
    links = []

    # Descargar las imágenes
    for image_tag in image_tags:
        if count <= n_images:
            try:
                link = image_tag['src']
                links.append(link)
                count += 1
            except KeyError:
                pass

    print(f"Descargando {len(links)} imágenes para '{movie_name}'...")

    # Crear carpetas para cada película en 'train' y 'test'
    organize_images_for_train_test(movie_name, links)

# Ejecutar el código
if __name__ == "__main__":
    main()