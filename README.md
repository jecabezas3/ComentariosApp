# Herramienta para Análisis de Emociones en Comentarios de Facebook

Esta herramienta está diseñada para realizar un análisis de emociones en los comentarios de publicaciones de Facebook. A continuación, se detalla el proceso de desarrollo y los componentes utilizados.

## Instalación de Dependencias de Python

Para instalar las dependencias de Python necesarias, puedes ejecutar el siguiente comando:
```bash
cd ComentariosApp
```
```bash
pip install -r requirements.txt 
```

Este comando instalará las bibliotecas necesarias, incluyendo Selenium, Beautiful Soup y otras dependencias utilizadas en el proyecto.

Para iniciar la herramienta:
```bash
python inicio.py
```
## Desarrollo de la Herramienta para Análisis de Emociones

La herramienta se desarrolló en Python debido a su versatilidad, facilidad de uso y una amplia comunidad de desarrolladores. Las bibliotecas clave utilizadas en el proyecto son:

- **Selenium:** Utilizado para realizar web scraping de forma automatizada.
- **Beautiful Soup:** Facilita la extracción de datos de documentos HTML.
- **XML Path Language:** Ofrece herramientas para la manipulación de archivos XML.

### Metodología de Extracción

La metodología de extracción se divide en los siguientes pasos:

1. **Obtención del código HTML:** Se utiliza Selenium para obtener el código HTML de la página de Facebook que se desea analizar.
2. **Localización de los elementos:** Beautiful Soup se emplea para identificar y localizar los elementos HTML que contienen la información deseada, como publicaciones y comentarios.
3. **Extracción de datos:** XML Path Language se utiliza para extraer información específica de cada elemento HTML, como texto de publicaciones, fechas, nombres de autores y comentarios.

### Automatización del Proceso

La herramienta implementa un algoritmo que automatiza la extracción de información. Este algoritmo utiliza Selenium para desplazarse por la página web de Facebook, identificar y seleccionar cada publicación, y extraer la URL de cada una. Luego, se visita cada URL para obtener detalles adicionales, como comentarios.

### Creación de la Interfaz de Usuario con Flet

Para la interfaz de usuario, se optó por el uso de Flet, un framework que facilita la creación de aplicaciones web o desktop. Se organizó el proyecto siguiendo la documentación oficial de Flet, lo que resultó en una interfaz limpia y fácil de usar. La interfaz permite ingresar la URL del grupo público de Facebook que se desea analizar.

### Análisis de Sentimientos con API de Vertex AI

Una vez que se obtienen los comentarios, la herramienta realiza un análisis de sentimientos utilizando la API de Vertex AI. Cada comentario se envía a un modelo previamente entrenado para determinar el sentimiento asociado.
