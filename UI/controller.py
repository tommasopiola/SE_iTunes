import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        try:
            durata = float(self._view.txt_durata.value)
            if not durata:
                self._view.show_alert("Durata non valida")
                return

            self._model.build_graph(durata)

        except ValueError:
            self._view.show_alert("Durata non valida")

        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Numero di nodi: {self._model.get_num_of_nodes()} \n"
                    f"Numero di archi: {self._model.get_num_of_edges()}")
        )
        self.populate_dd()

        self._view.update()


    def populate_dd(self):
        self._view.dd_album.options.clear()
        lista_album = self._model.G.nodes()

        for album in lista_album:
            self._view.dd_album.options.append(
                ft.dropdown.Option(key=str(album.id), text=album.title))

        self._view.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        if e.control.value is None:
            return

        id_selez = int(e.control.value)
        album_selex = self._model.id_map[id_selez]

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO
        try:
            id_album = self._view.dd_album.value
        except ValueError:
            self._view.show_alert("Selezionare prima un album")
            return

        album = self._model.id_map[int(id_album)]
        dimensione, durata = self._model.get_analisi_componente(album)

        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Dimensione componente connessa a {album.title}: {dimensione}\n"
                    f"Durata totale: {durata:.2f} minuti")
        )

        self._view.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO
        try:
            durata_max = float(self._view.txt_durata_totale.value)
        except ValueError:
            self._view.show_alert("Durata non valida")
            return

        id_album1 = self._view.dd_album.value
        if id_album1 is None:
            self._view.show_alert("Selezionare prima un album")
            return

        album1 = self._model.id_map[int(id_album1)]

        risultato, durata = self._model.cerca_set_album(album1, durata_max)

        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(
            ft.Text(f"Set trovato: {len(risultato)} album, durata totale: {durata}\n" ))
        for album in risultato:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f"- {album.title} ({album.durata}) min\n")
            )

        self._view.update()