from flet import (TextField, ProgressBar, ElevatedButton, Column, UserControl, Text, ListView, Divider, Row)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import requests
class ComentariosApp(UserControl):
    
    def __init__(self,page):
        self.url_input = TextField(hint_text="Ingresa el nombre de la página de Facebook")
        self.analyze_button = ElevatedButton(text="Obtener Comentarios", on_click=self.analyze_data)
        self.comentarios_area = ListView(expand=1)
        self.page = page
        self.texto = Text(value="Verificando Post", weight="bold",visible=False)
        self.nombre_progreso = Text(value="Comenzado Web Scraping......", weight="bold",visible=False)
        self.progress_bar = ProgressBar(width=400, visible=False)
        self.progress_bar.value = 0
    def initialize_ui(self):
        return Column(
                    width=600,
                    spacing=25,
                    controls=[
                        Row([Text(value="Analisis de Sentimientos en Entornos Virtuales", style="headlineMedium")], alignment="center"),
                        self.url_input,
                        self.texto,
                        Divider(),
                        self.analyze_button,
                        self.progress_bar,
                        self.nombre_progreso,
                        Divider(),
                        self.comentarios_area,
                    ],
                )
    def predecir_emocion(self, texto):
        project_id = "143198414809"
        endpoint_id = "5518978824412332032"
        token = "ya29.a0AfB_byC4VFq985Mh-M8ZdMxer5xCDEtJ7akOEE2FIN5ap9t8LiefdFnkuaZcLxlbTk4U0FKvUYnvJAXiY1c4AjpVR5nvp9xLqv7YLZfGTdnK0oADGs4CYmgB9SRT32DuK2hNMAV8Mum6V5xLrm847AnghT321SjTxuNepVcyKH-lCCzveGZBuSKKXMvmvGRcQ5PoRh5BWoqrv7NRqITVbTmRLSBB_FZvs5Dxy0eCsA8rUK-Hor13UIU8Zc8O5l12eWVg8zExp9yHPNEdaTCqJBfavIxPUviZIUR5NYZWyQqCyrOMywKzmKJaaQXMgqoL0xVV2Gpsp9LWEjmlUEqAFQ9LyqzzjbvDidfyZdW-eB89LV9HHJv3-hFb2Vgd_Gs48lue8yYAdhVaLuOcJzq5ACb4uSfBi3IdaCgYKAd8SARISFQHGX2Miigc5fnKf46GnlRyAB0zXRA0423"
        url = "https://us-central1-aiplatform.googleapis.com/ui/projects/{}/locations/us-central1/endpoints/{}:predict".format(project_id, endpoint_id)
        headers = {
            "Authorization": "Bearer {}".format(token),
            "Content-Type": "application/json"
        }
        payload = {
            "instances": {
                "mimeType": "text/plain",
                "content": texto
            }
        }
        respuesta = requests.post(url, headers=headers, json=payload)
        if respuesta.status_code == 200:
            resultado = respuesta.json()
            result = resultado['predictions']

            # Variables para almacenar el valor máximo y su displayName correspondiente
            max_confidence = float('-inf')  # Inicializar con un valor muy pequeño
            max_displayName = None

            # Variables para almacenar la suma de emociones intensas
            suma_emociones_intensas = 0

            # Iterar sobre los elementos de la lista
            for item in result:
                # Acceder a los valores del diccionario
                confidences = item['confidences']
                displayNames = item['displayNames']

                # Encontrar el índice del valor máximo en confidences, excluyendo ciertos displayNames
                max_index = max(
                    range(len(confidences)),
                    key=lambda i: confidences[i] if displayNames[i] not in ['Amor nulo', 'Miedo nulo', 'Sorpresa nula', 'Tristeza nula', 'Dolor nulo', 'Vergüenza nula', 'Alegría nula', 'Neutral nulo', 'Enojo nulo', 'Decepción nula'] else float('-inf')
                )

                # Obtener el valor máximo de confidences y su respectivo displayName
                confidence = confidences[max_index]
                displayName = displayNames[max_index]

                # Actualizar los valores máximos si el valor actual es mayor
                if confidence > max_confidence:
                    max_confidence = confidence
                    max_displayName = displayName

                # Sumar los valores de emociones intensas específicas
                for name, conf in zip(displayNames, confidences):
                    if name in ['Miedo intenso', 'Sorpresa intensa', 'Tristeza intensa', 'Dolor intenso', 'Vergüenza intensa', 'Enojo intenso', 'Decepción intensa']:
                        suma_emociones_intensas += conf

            # Preparar los mensajes a imprimir
            intensity_message = f"Intensidad Emocional: {max_displayName}"
            depression_message = "Sufre depresión" if suma_emociones_intensas > 2 else "No sufre depresión"
            neutral_message = "No refleja emoción clara" if max_displayName == "Neutral intenso" else ""

            # Filtrar mensajes vacíos
            messages = " - ".join([message for message in [intensity_message, depression_message, neutral_message] if message])

            # Retornar los mensajes
            return messages
        else:
            raise Exception("Error al realizar la predicción: {}".format(respuesta.status_code))
    
    def get_comentarios(self, url):
        self.nombre_progreso.visible = True
        self.nombre_progreso.update()
        self.texto.visible = False
        self.texto.update()
        
        # Configuración para Firefox con la ruta al geckodriver
        firefox_options = Options()
        firefox_options.headless = True
        firefox_options.set_preference("intl.accept_languages", "en-US")

        # Iniciar el navegador web
        driver = webdriver.Firefox(options=firefox_options)
        time.sleep(3)
        driver.set_window_position(-10000, -10000)

        # Acceder a la publicación
        try:
            driver.get(url)
            post = driver.find_element(By.XPATH, "//div[contains(@class,'x6s0dn4 x78zum5 xvrxa7q x9w375v xxfedj9 x1roke11 x1es02x0')]")
        except:
            self.texto.visible = True
            self.texto.update()
            self.texto.value = "No existe el Post - Verifique que sea una Pagina Publica de Facebook"
            self.texto.update()
            self.nombre_progreso.visible = False
            self.nombre_progreso.update()
            self.progress_bar.visible = False
            self.progress_bar.update()
            driver.quit()
            return
        self.nombre_progreso.value = "Obteniendo publicaciones......"
        self.nombre_progreso.update()
        time.sleep(2)
        try:
            login = driver.find_element(By.XPATH, "//div[contains(@class,'x92rtbv x10l6tqk x1tk7jg1 x1vjfegm')]")
        except:
            login = None
        if login is not None:
            login.click()
        time.sleep(4)
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(2)
        
        #Obtener los post
        publicaciones = []
        numero_post = 1
        omit = 0
        self.nombre_progreso.value = "Obteniendo publicaciones......"
        self.nombre_progreso.update()
        # Obtener la cantidad total de publicaciones
        while len(publicaciones) != numero_post:
            publicacion = driver.find_element(By.XPATH, "//span[contains(@class,'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xi81zsa x1yc453h')]")
            link = publicacion.find_element(By.XPATH, ".//a[contains(@class,'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm')]").get_attribute('href')
            if link in publicaciones:
                omit+=1
            else:
                publicaciones.append(link)
                self.progress_bar.value = (len(publicaciones) / numero_post)
                self.progress_bar.update()
                print(f"Procesando publicación {len(publicaciones)}")

            driver.execute_script("window.scrollBy(0, 750);")
            time.sleep(4)
        # Imprime la cantidad de publicaciones encontradas
        print("Se encontraron", len(publicaciones), "publicaciones.")
        print("Se omitieron", omit, "publicaciones")
        self.nombre_progreso.value = "Analizando Comentarios......"
        self.nombre_progreso.update()
        self.progress_bar.value = 0
        self.progress_bar.update()
        contador = 1
        matriz_comentarios = []
        for link in publicaciones:
            # Acceder a la publicación
            driver.get(link)
            try:
                login = driver.find_element(By.XPATH, "//div[contains(@class,'x92rtbv x10l6tqk x1tk7jg1 x1vjfegm')]")
            except:
                login = None
            if login is not None:
                login.click()
            # Desplazarse hasta la sección de comentarios
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Obtener los elementos de los comentarios
            comentarios = driver.find_elements(By.XPATH, "//div[contains(@class,'x169t7cy x19f6ikt')]")

            # Verificar si hay comentarios
            if len(comentarios) == 0:
                print(f"No se encontraron comentarios en la publicación: {link}")
            else:
                print(f"Se encontraron {len(comentarios)} comentarios en la publicación: {link}")
            self.progress_bar.value = (contador / len(publicaciones) )
            self.progress_bar.update()
            # Almacenar los comentarios en una matriz
            comentarios_omitidos = 0
            for comentario in comentarios:
                soup = BeautifulSoup(comentario.get_attribute("innerHTML"), "html.parser")
                see_more_button = soup.find("div", class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f", text="See more")
                try:
                    imagen = comentario.find_element(By.XPATH, ".//div[@class='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs']").text
                except:
                    imagen = None
                if imagen is not None:
                    nombre = comentario.find_element(By.XPATH, ".//span[contains(@class,'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa x1s688f xzsf02u')]").text
                    texto_comentario = comentario.find_element(By.XPATH, ".//div[@class='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs']").text
                    sentimiento = self.predecir_emocion(texto_comentario)
                    if see_more_button:
                        try:
                            ventana = driver.find_element(By.XPATH, ".//div[@class= 'x78zum5 xdt5ytf x2lah0s x193iq5w x2bj2ny x1ey2m1c xayqjjm x9f619 xds687c x1xy6bms xn6708d x1s14bel x1ye3gou xixxii4 x17qophe x1u8a7rm']")
                        except:
                            ventana = None
                        if ventana is not None:
                            driver.execute_script("arguments[0].style.display = 'none';", ventana)
                        ver_mas = comentario.find_element(By.XPATH, ".//div[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f']")
                        ver_mas.click()
                        texto_comentario = comentario.find_element(By.XPATH, ".//div[@class='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs']").text
                        sentimiento = self.predecir_emocion(texto_comentario)
                    matriz_comentarios.append((nombre, texto_comentario,sentimiento))
                else:
                    comentarios_omitidos += 1
            # Imprimir comentarios omitidos
            print(f"Comentarios omitidos: {comentarios_omitidos}")
            contador += 1
        # Cerrar el navegador web
        driver.quit()
        self.nombre_progreso.value = "Finalizando......"
        self.nombre_progreso.update()
        time.sleep(2)
        return matriz_comentarios
        
        
    def analyze_data(self, url):
        self.progress_bar.visible = True
        self.progress_bar.update()
        url = self.url_input.value
        comentarios = self.get_comentarios(url)
        comentarios_area = self.comentarios_area
        comentarios_area.controls = []
        if not comentarios:
            comentarios_area.controls = [Text("No se encontraron comentarios en la publicación")]
            return

        matriz_comentarios = []
        for comentario in comentarios:
            matriz_comentarios.append((comentario[0], comentario[1], comentario[2]))

        # Crear la lista de comentarios dentro de analyze_data
        lista_comentarios = []
        for nombre, comentario, sentimiento in matriz_comentarios:

            lista_comentarios.append(
                Column(
                    [
                        Text(nombre, size=16, weight="bold"),
                        Text(comentario),
                        Text(sentimiento, weight="bold",size=14),
                        Divider(),
                    ]
                )
                
            )
        # Asignar la lista al ListView
        comentarios_area.controls = lista_comentarios
        self.nombre_progreso.visible = False
        self.nombre_progreso.update()
        self.progress_bar.visible = False
        self.progress_bar.update()
        # Actualizar la interfaz
        self.page.update()