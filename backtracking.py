import graph
import math
import sys
import queue
import dijkstra

# Funcions auxiliars Backtracking =======================================================================
def es_Cami_Correcte(recorregut, punts_visitar):
    """

    Parameters
    ----------
    recorregut : List
        Camí d'arestes del node origen al node destí
    punts_visitar : Set
        Nodes que s'han de visitar obligatòriament abans d'arribar el destí

    Returns
    -------
    bool
        Retorna si el camí és correcte
    """
    
    recorregut = [n.Destination for n in recorregut] #Passem les aresta a nodes
    for punt in punts_visitar:
        "Busquem si el recorregut conté tots els punts intermitjos"
        if punt not in recorregut:
            return False
    return True

def Backtracking_Pur(node_inicial, node_desti, recorregut, punts_visitar, cost, cost_optim, cami_optim):
    """

    Parameters
    ----------
    node_inicial : Class Node
        Node actual en la recursió
    node_desti : Class Node
        Node al que volem arribar en cada camí
    recorregut : List
        Recorregut d'arestes durant la recursió
    punts_visitar : Set
        Punts intermitjos que ha de tenir el recorregut
    cost : Float
        Cost del camí
    cost_optim : Float
        Cost del camí més òptim
    cami_optim : List
        Llista d'arestes amb el camí més òptim

    Returns
    -------
    cost_optim : Float
        Cost del camí més òptim
    cami_optim : List
        Llista d'arestes amb el camí més òptim


    """
    "Cas base de la recursió: Mirem si el node ha arribat al destí i si aquest camí és una possible solució"
    if node_inicial == node_desti and es_Cami_Correcte(recorregut, punts_visitar): #set(llista_punts_visitar).issubset(set([n.Destination for n in recorregut]))
        return recorregut, cost

    "Visitem els veïns del node actual"
    for aresta in node_inicial.Edges:
        "Mira si hi ha estat visitada l'aresta, en cas positiu passem a la següent iteració"
        try:
            aresta.visitat
        except:
            aresta.visitat = False

        if aresta.visitat or aresta in recorregut:
            continue

        "Fem el pas endevant en cas de ser un punt intermig"
        if aresta.Destination in punts_visitar:
            aresta.visitat = True
        
        "Afegim l'aresta al recorregut i calculem el nou cost del camí"
        nou_recorregut = recorregut + [aresta]
        nou_cost = cost + aresta.Length
        
        "Comprovem si el camí actual està sent més eficient (podar si no compleix)"
        if nou_cost < cost_optim:
            "En cas de ser més eficient, continuem fent la recursió amb els veïns"
            res_recorregut, res_cost = Backtracking_Pur(aresta.Destination, node_desti, nou_recorregut, punts_visitar, nou_cost, cost_optim, cami_optim)
            
            "Si ha retornat un camí i és òptim l'actualitzem"
            if res_recorregut and res_cost < cost_optim:
                cost_optim = res_cost
                cami_optim = res_recorregut

        "Fem el pas enrere en cas de ser un punt intermig"
        if aresta.Destination in punts_visitar:
            aresta.visitat = False
    
    "Si es visita tots els veïns, comprovem si hem obtingut un camí òptim i el retornem"
    if cami_optim:
        return cami_optim, cost_optim
    else:
        return None, None


def SalesmanTrackBacktracking(g,visits):
    """
    Solució del problema del viatjant de comerci amb un algorisme de Backtracking Pur
    
    Parameters
    ----------
    g : Class Graph
        Graf d'entrada
    visits : Class Visits
        Llista de nodes que es visiten d'entrada

    Returns
    -------
    Class Track
        Track de sortida
    """
    
    "IMPLEMENTACIÓ"
    visits.Vertices[0].visitat = True
    recorregut = list()
    punts_visitar = set(visits.Vertices[1:-1])
    graf_retorn = graph.Track(g)

    "Fem l'algorisme Backtracking Recursiu"
    recorregut, cost = Backtracking_Pur(visits.Vertices[0], visits.Vertices[-1],recorregut, punts_visitar, 0, math.inf, [])
    
    "Afegim al track el recorregut òptim d'arestes"
    for aresta in recorregut:
        graf_retorn.AddLast(aresta)

    
    return graf_retorn

# ==============================================================================

def SalesmanTrackBacktrackingGreedy(g, visits):
    return graph.Track(g)

