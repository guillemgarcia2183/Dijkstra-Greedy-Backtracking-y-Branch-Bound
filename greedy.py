import math
import sys
import queue

sys.path.append('PythonSalesMan')
import graph
import dijkstra

# SalesmanTrackGreedy ==========================================================
def SalesmanTrackGreedy(g,visits):
    """
    Solució Greedy al problema del viatjant de comerci
    
    Parameters
    ----------
    g : Class Graph
        Graf d'entrada    
    
    visits : Class Visits
        Llista de nodes que es visiten d'entrada
    Returns
    -------
    Class Track 
    """
    
    "IMPLEMENTACIÓ"
    "Precondicions de l'algorisme --> Veiem si el graf està buit o les visites està buida"
    if len(g.Vertices) > 0 and len(visits.Vertices) > 0:
        "Obtenim el node inicial i tots els candidats a partir de la llista de visitats"
        node_actual = visits.Vertices[0]
        candidats = visits.Vertices[1:-1]
        graf_retorn = graph.Track(g) #Track de retorn   
        
        "Mentre la llista de candidats sigui major a zero, farem el següent procediment"
        while candidats:
            "Apliquem l'algorisme Dijkstra pel node actual i busquem el candidat amb distància mínima"
            aresta_cami, aresta_print = dijkstra.DijkstraQueue(g,node_actual)
            node_candidat,aresta_candidat = Cerca_Candidat_Minim(aresta_cami, candidats)
            
            "Si no hi ha més candidats, s'acaba el recorregut"
            if node_candidat == None:
                break

            # print("DIJKSTRA:", aresta_print)
            # print("NODE ACTUAL:", node_actual.Name)
            # print("NODE CANDIDAT:", node_candidat.Name)
            # print("ARESTA_CANDIDAT:", aresta_candidat)
            # print("#######################################")
            
            "Afegim el recorregut d'arestes al Track"
            for aresta in aresta_candidat:
                if aresta not in graf_retorn.Edges:
                    graf_retorn.AddLast(aresta)
            
            "Borrem el node trobat dels candidats i actualitzem el node actual"
            candidats.remove(node_candidat)
            node_actual = node_candidat        
        
        "Afegim l'aresta del últim node candidat al node destí"
        Afegir_ultima_aresta(visits.Vertices[-1], node_actual, graf_retorn)
        
        "Retornem el Track amb el recorregut de les arestes"
        return graf_retorn
    "En cas que no es compleixi les precondicions, retorna un track buit"
    return graph.Track(g)



# Funcions auxiliars ===========================================================
def Cerca_Candidat_Minim(cami_arestes, candidats):
    """
    Troba el candidat de distància mínima de l'iteració actual
    Parameters
    ----------
    cami_arestes: Dict
        Diccionari amb el camí d'arestes del Dijkstra
    candidats : List
        Llista dels vertex candidats de la classe Visits
    
    Returns
    -------
    aresta_retorn : Class Vertex
        Node amb la distància mínima
    """
    
    "IMPLEMENTACIÓ"
    minim = math.inf
    node_retorn = None
    for vertex in cami_arestes:
        "Anem actualitzant iterativament el node amb mínima distància"
        if vertex in candidats:
            if vertex.DijkstraDistance < minim:
                minim = vertex.DijkstraDistance
                node_retorn = vertex

    return node_retorn, cami_arestes[node_retorn]


def Afegir_ultima_aresta(desti, ultim_candidat, track):
    """
    Troba l'aresta que connecta el vertex destí i l'últim candidat i l'afegeix al Track
    Parameters
    ----------
    desti : Class Vertex
        Vertex destí
    ultim_candidat : Class Vertex
        Vertex últim en fer el bucle while
    track : Class Track
        Track amb els camí que ha fet l'algorisme Greedy
    Returns
    -------
    None.
    """
    "IMPLEMENTACIÓ"
    arestes_candidat = ultim_candidat.Edges
    "Recorrem les arestes del candidat iterativament fins trobar l'aresta destí"
    for aresta in arestes_candidat:
        if aresta.Destination == desti:
            track.AddLast(aresta)
            return 