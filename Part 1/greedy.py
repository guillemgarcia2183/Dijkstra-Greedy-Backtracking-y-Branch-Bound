import math
# import sys
# import queue

# sys.path.append('PythonSalesMan')
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
    "Obtenim el node inicial i tots els candidats a partir de la llista de visitats"
    node_actual = visits.Vertices[0]
    candidats = visits.Vertices[1:-1]
    graf_retorn = graph.Track(g) #Track de retorn   
    
    "Mentre la llista de candidats sigui major a zero, farem el següent procediment"
    while candidats:
        "Apliquem l'algorisme Dijkstra pel node actual i busquem el candidat amb distància mínima"
        aresta_cami = dijkstra.DijkstraQueue_Greedy(g,node_actual)
        node_candidat,aresta_candidat = Cerca_Candidat_Minim(aresta_cami, candidats)
        
        "Si no hi ha més candidats, s'acaba el recorregut"
        if node_candidat == None:
            break

        # print("DIJKSTRA:", aresta_cami)
        # print("NODE ACTUAL:", node_actual.Name)
        # print("NODE CANDIDAT:", node_candidat.Name)
        # print("ARESTA_CANDIDAT:", aresta_candidat)
        # print("#######################################")
        
        "Afegim el recorregut d'arestes al Track"
        for aresta in aresta_candidat:
            if aresta not in graf_retorn.Edges:
                graf_retorn.AddLast(aresta)
                       
        "Borrem el node trobat dels candidats i actualitzem el node actual"
        node_actual = node_candidat        
        candidats.remove(node_candidat)
    
    "Afegim l'aresta del últim node candidat al node destí"
    aresta_cami = dijkstra.DijkstraQueue_Greedy(g,node_actual)
    recorregut_fins_desti = aresta_cami[visits.Vertices[-1]]
    for aresta in recorregut_fins_desti:
        if aresta not in graf_retorn.Edges:
            graf_retorn.AddLast(aresta)
    
    "Retornem el Track amb el recorregut de les arestes"
    return graf_retorn

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
    node_retorn : Class Vertex
        Node amb la distància mínima
    arestes_node: List
        Llista amb els vèrtex dels node mínim
    """
    
    "IMPLEMENTACIÓ"
    minim = math.inf
    node_retorn = None
    for vertex in cami_arestes:
        "Anem actualitzant iterativament el node amb mínima distància"
        if vertex.DijkstraDistance < minim:
            if vertex in candidats:
                    minim = vertex.DijkstraDistance
                    node_retorn = vertex
    
    try:
        return node_retorn, cami_arestes[node_retorn]
    except:
        return None,None


 