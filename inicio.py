import flet as ft
from flet import Page
from analisis_sentimiento.controles import ComentariosApp

def create_app(page: Page):
    page.title = "Análisis de Emociones"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"

    # Crear la Instancia de ComentariosApp:
    instance = ComentariosApp(page)
    page.add(instance.initialize_ui())

def main():
    ft.app(target=create_app)

if __name__ == "__main__":
    main()