import graph
import math
import sys
import queue
import dijkstra
import copy

# Funcions auxiliars Backtracking =======================================================================

def es_Cami_Correcte(n_punts_visitats, llista_punts_visitar):
    if n_punts_visitats == len(llista_punts_visitar):
        return True
    return False
    
def es_Cami_Optim(cost_actual, cost_optim):
    if cost_actual < cost_optim:
        return True
    return False

def Backtracking_Recursiu(node_inicial, node_desti, n_punts_visitats, recorregut_arestes, llista_punts_visitar, cost, cost_optim, cami_optim):    
    "Cas base de la recursió"
    if node_inicial == node_desti: #Si hem arribat del node origen al destí
        if n_punts_visitats == len(llista_punts_visitar): #Comprovem que s'han visitats tots els punts intermitjos
            return n_punts_visitats,recorregut_arestes, cost #Retorna el recorregut en cas de ser una solució possible
        else:
            return None, None, None #Retorna None en cas de no ser solució
    
    "Recorrem els veins del node actual"
    for aresta in node_inicial.Edges:
        try:
            aresta.visitat
        except:
            aresta.visitat = False
            
        "Saltem al següent veí si s'ha visitat"
        if aresta.visitat:
            continue
        
        "Afegim al recorregut i llista de visitats"
        recorregut_arestes.append(aresta)
        aresta.visitat = True
        
        "En cas de ser el node destí un punt intermig, sumem el comptador"
        if aresta.Destination in llista_punts_visitar:
            n_punts_visitats += 1
        
        "Fem la recursió a partir del vei fins arribar al node destí en cas que el camí sigui òptim"
        if cost + aresta.Length < cost_optim:
            new_punts_visitats, new_recorregut_arestes, new_cost = Backtracking_Recursiu(aresta.Destination, node_desti, n_punts_visitats, recorregut_arestes, llista_punts_visitar, cost + aresta.Length, cost_optim, cami_optim)
            "Si troba una solució"
            if new_recorregut_arestes:
                if es_Cami_Optim(new_cost, cost_optim):
                    cost_optim = new_cost
                    cami_optim = new_recorregut_arestes
                else:
                    recorregut_arestes.remove(aresta)
                    aresta.visitat = False
            else:
                recorregut_arestes.remove(aresta)
                aresta.visitat = False
        else:
            recorregut_arestes.remove(aresta)
            aresta.visitat = False
            
    return n_punts_visitats, recorregut_arestes, cost
    

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
    """
    
    "IMPLEMENTACIÓ"
    visits.Vertices[0].visitat = True
    recorregut_arestes = list()
    llista_punts_visitar = visits.Vertices[1:-1]
    print("PUNTS A VISITAR:", llista_punts_visitar)
    print("######################")

    graf_retorn = graph.Track(g)
    nodes,recorregut, cost = Backtracking_Recursiu(visits.Vertices[0], visits.Vertices[-1], 0, recorregut_arestes, llista_punts_visitar, 0, math.inf, [])
    
    print("RECORREGUT/COST:", recorregut, cost)
    print("######################")

    for aresta in recorregut:
         graf_retorn.AddLast(aresta)
        
    return graf_retorn

# ==============================================================================

def SalesmanTrackBacktrackingGreedy(g, visits):
    return graph.Track(g)

