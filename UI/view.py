import flet as ft
from UI.alert import AlertManager

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "SE_iTunes"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # Intestazione
        self.txt_titolo = ft.Text(value="Gestione Album Musicali", size=38, weight=ft.FontWeight.BOLD)

        # Riga 1
        self.txt_durata = ft.TextField(label="Durata (in min)")
        self.pulsante_crea_grafo = ft.ElevatedButton(text="Crea Grafo",
                                                    on_click=self.controller.handle_crea_grafo)
        row1 = ft.Row([
            ft.Container(self.txt_durata, width=200),
            ft.Container(self.pulsante_crea_grafo, width=200)
        ], alignment=ft.MainAxisAlignment.CENTER)

        self.lista_visualizzazione_1 = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # Riga 2
        self.dd_album = ft.Dropdown(label="Album", width=200, on_change=self.controller.get_selected_album)
        self.pulsante_analisi_comp = ft.ElevatedButton(text="Analisi Componente",
                                                 on_click=self.controller.handle_analisi_comp)
        row2 = ft.Row([
            ft.Container(self.dd_album, width=200),
            ft.Container(self.pulsante_analisi_comp, width=200)
        ], alignment=ft.MainAxisAlignment.CENTER)

        self.lista_visualizzazione_2 = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # Riga 3
        self.txt_durata_totale = ft.TextField(label="Durata Totale")
        self.pulsante_set_album = ft.ElevatedButton(text="Set di Album",
                                                    on_click=self.controller.handle_get_set_album)
        row3 = ft.Row([
            ft.Container(self.txt_durata_totale, width=200),
            ft.Container(self.pulsante_set_album, width=200)
        ], alignment=ft.MainAxisAlignment.CENTER)

        self.lista_visualizzazione_3 = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # --- Toggle Tema ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        # --- Layout della pagina ---
        self.page.add(
            self.toggle_cambia_tema,

            # Sezione 1
            self.txt_titolo,
            ft.Divider(),

            row1,
            self.lista_visualizzazione_1,
            ft.Divider(),

            row2,
            self.lista_visualizzazione_2,
            ft.Divider(),

            row3,
            self.lista_visualizzazione_3
        )

        self.page.scroll = "adaptive"
        self.page.update()

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()
