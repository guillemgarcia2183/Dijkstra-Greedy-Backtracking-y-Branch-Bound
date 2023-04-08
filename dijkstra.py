import math
import sys
import queue

sys.path.append('PythonSalesMan')
import graph


# Funcions auxiliars ===========================================================
def Cerca_Node_Minim(distancies,visitats):
    """
    Troba el node de distància mínima de l'iteració actual
    Parameters
    ----------
    distancies : Dict
        Diccionari de distàncies
    visitats : Dict
        Diccionari dels nodes visitats
    Returns
    -------
    node : Class Vertex
        Node amb la distància mínima
    """
    
    "IMPLEMENTACIÓ"
    minim = math.inf
    node = None
    for n,pes in distancies.items():
        "Anem actualitzant iterativament el node amb mínima distància"
        if n not in visitats and pes < minim:
            minim = pes
            node = n
    return node

# Dijkstra =====================================================================
def Dijkstra(g,start):
    """
    La funció es basarà en posar els pesos en els nodes sense la llibreria queue.
    
    Parameters
    ----------
    g : Class Graph
        Graf en què farem l'algorisme Dijkstra. 
        
    start : Class Node
        Node en què es començarà a col·locar distàncies
    Returns
    -------
    None.
    """ 
    
    "IMPLEMENTACIÓ"
    # print("###############################")
    # print("ALGORISME DIJKSTRA....")
    
    "Precondicions de l'algorisme --> Si el vertex està en el graf i el graf no està buit, continua"
    if start in g.Vertices and len(g.Vertices) > 0:
        "Inicialitzem les següents variables"
        visitats = dict() #Controla els nodes que estan visitats
        distancies = {x:x.DijkstraDistance for x in g.Vertices} #Controla les distancies mínimes d'aquests nodes
        distancies[start] = 0 
        start.DijkstraDistance = 0
        comptador = 0
        
        "Iterem tantes vegades com nodes hi hagi en el graf"
        while comptador < len(g.Vertices)-1:
            "Busquem el node que en l'iteració actual té distància més baixa i el posa en visitats"
            node_actual = Cerca_Node_Minim(distancies, visitats)
            
            "En cas de no trobar un node mínim, trenquem el bucle i s'acaba l'algorisme"
            if node_actual == None:
                break
            
            visitats[node_actual] = True
            
            "Veiem els veins del node actual, comprovem si es troba en visitats, i en cas negatiu comparem les distàncies per actualitzar-les"
            for aresta in node_actual.Edges:
                if aresta.Destination not in visitats:
                    distancia_comparar = aresta.Length + distancies[aresta.Origin]
                    if distancies[aresta.Destination] > distancia_comparar:
                        distancies[aresta.Destination] = distancia_comparar
                        aresta.Destination.DijkstraDistance = distancia_comparar 
                        
            comptador += 1
    
    # print("ALGORISME DIJKSTRA FINALITZAT!")
    # print("###############################")

# DijkstraQueue ================================================================

def DijkstraQueue(g,start):
    """
    La funció iniciarà els pesos dels nodes amb l'ajuda de la llibreria queue
    Parameters
    ----------
    g : Class Graph
        Graf en què farem l'algorisme Dijkstra.
    start : Class Node
        Node en què es començarà a col·locar distàncies
    Returns
    -------
    cami_arestes: Diccionari per veure les arestes per arribar al camí mínim
                  Clau: Node_precedent, Valor: Aresta 
    """
    
    "IMPLEMENTACIÓ"
    # print("###############################")
    # print("ALGORISME DIJKSTRA_QUEUE....")
    
    "Precondicions de l'algorisme --> Si el vertex està en el graf i el graf no està buit, continua"
    if start in g.Vertices and len(g.Vertices) > 0:
        "Per tal de fer l'algorisme Greedy, necessitem una variable que guardi les arestes precedents"
        cami_arestes = {x: [] for x in g.Vertices}
        cami_print = {x.Name: [] for x in g.Vertices}

        "Creem una cua de prioritat per poder fer l'algorisme. La prioritat serà la distància més curta"
        cua = queue.PriorityQueue()
        visitats = dict() #Controla els nodes que estan visitats
        
        distancies = {x:x.DijkstraDistance for x in g.Vertices} #Controla les distancies mínimes d'aquests nodes
        
        distancies[start] = 0
        start.DijkstraDistance = 0
        
        cua.put((0, start))
        
        "Mentre la cua no sigui buida, repetirem el mateix procediment de la funció anterior"
        while not cua.empty():
            distancia_node, node_actual = cua.get()
            visitats[node_actual] = True
            "Veiem els veins del node actual, comprovem si es troba en visitats, i en cas negatiu comparem les distàncies per actualitzar-les"
            for aresta in node_actual.Edges:            
                if aresta.Destination not in visitats:
                    distancia_comparar = distancia_node + aresta.Length
                    if distancia_comparar < distancies[aresta.Destination]:
                        distancies[aresta.Destination] = distancia_comparar
                        aresta.Destination.DijkstraDistance = distancia_comparar
                        cua.put((aresta.Destination.DijkstraDistance, aresta.Destination))
                        
                        "Cada vegada que s'actualitza la distància, s'actualitza l'aresta precedent"
                        for conn in cami_arestes[node_actual]:
                            cami_arestes[aresta.Destination].append(conn)
                            cami_print[aresta.Destination.Name].append(conn.Name)

                        cami_arestes[aresta.Destination].append(aresta)
                        cami_print[aresta.Destination.Name].append(aresta.Name)

            
        "Return de la llista per aplicar-la en l'algorisme Greedy"
        return cami_arestes, cami_print
    
    # print("ALGORISME DIJKSTRA_QUEUE FINALITZAT!")
    # print("###############################")