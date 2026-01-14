import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G= nx.Graph()
        self.nodes = []
        self._edges = []
        self._lista_album = []
        self._lista_connessioni = []
        self.id_map = {}

        self._rimanente = 0
        self._durata_rimanente = 0


    def build_graph(self, durata):

        self._lista_album = DAO.get_album(durata)

        self.G.clear()
        self.G = nx.Graph()

        for album in self._lista_album:
            self.nodes.append(album)

        self.G.add_nodes_from(self.nodes)

        self.id_map = {}
        for node in self.nodes:
            self.id_map[node.id] = node

        self._lista_connessioni = DAO.get_connessioni()
        self._edges.clear()

        for e in self._lista_connessioni:
            id_album1 = e[0]
            id_album2 = e[1]

            if id_album1 in self.id_map and id_album2 in self.id_map:
                nodo_a1 = self.id_map[id_album1]
                nodo_a2 = self.id_map[id_album2]
                self._edges.append((nodo_a1, nodo_a2))

        self.G.add_edges_from(self._edges)

    def get_num_of_nodes(self):
        return self.G.number_of_nodes()

    def get_num_of_edges(self):
        return self.G.number_of_edges()

    def get_analisi_componente(self, album_partenza):

        componente = nx.node_connected_component(self.G, album_partenza)

        dimensione = len(componente)

        durata_ms = sum(album.durata for album in componente)
        durata_minuti = durata_ms

        return dimensione, durata_minuti

    """ Metodo 2:
    def get_componente_bfs(grafo, nodo_partenza):
    visited = set()      # Nodi già esplorati
    queue = [nodo_partenza]  # Coda per la visita
    visited.add(nodo_partenza)

    while queue:
        u = queue.pop(0) # Estraggo il primo elemento (FIFO)
        
        # Esploro i vicini del nodo corrente
        for v in grafo.neighbors(u):
            if v not in visited:
                visited.add(v)
                queue.append(v)
                
    return visited # Questo set contiene la componente connessa """

    """ Metodo 3:
    def get_componente_dfs(grafo, nodo_partenza):
    visited = set()

    def recursive_visit(u):
        visited.add(u)
        for v in grafo.neighbors(u):
            if v not in visited:
                recursive_visit(v)

    recursive_visit(nodo_partenza)
    return visited """

    """ Metodo 4:
    def get_analisi_componente_con_bfs(self, album_partenza):
    # Genera l'albero di visita in ampiezza
    tree = nx.bfs_tree(self.G, source=album_partenza)
    
    # I nodi dell'albero sono esattamente i nodi della componente connessa
    nodi_componente = list(tree.nodes())
    
    dimensione = len(nodi_componente)
    durata_totale = sum(a.tot_durata for a in nodi_componente)
    
    return dimensione """

    def cerca_set_album(self, album1, d_tot):
        componente = list(nx.node_connected_component(self.G, album1))
        componente.sort(key=lambda x: x.durata)
        componente.remove(album1)

        self._best_sol = [album1]

        rimanente = float(d_tot) - float(album1.durata)

        if rimanente < 0:
            return [album1], float(album1.durata)

        self._ricorsione([album1], componente, rimanente)

        durata_totale = float(sum(a.durata for a in self._best_sol))

        return self._best_sol, durata_totale

    def _ricorsione(self, parziale, candidati, durata_residua):

        if len(parziale) > len(self._best_sol):
            self._best_sol = parziale[:]

        if len(candidati) == 0 or durata_residua == 0:
            return

        for i in range(len(candidati)):
            album_corrente = candidati[i]

            # pruning
            if album_corrente.durata > durata_residua:
                break

            elif album_corrente.durata <= durata_residua:
                parziale.append(album_corrente)

                nuovi_candidati = candidati[i + 1:]
                self._ricorsione(parziale, nuovi_candidati, float(durata_residua) - float(album_corrente.durata))

                parziale.pop()
