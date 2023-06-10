# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 15:03:27 2023

@author: garci
"""

import graph
import math
import dijkstra

# Funcions auxiliars Backtracking =======================================================================
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
    llista = list()
    
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
            if aresta not in llista:
                llista.append(aresta)
                       
        "Borrem el node trobat dels candidats i actualitzem el node actual"
        node_actual = node_candidat        
        candidats.remove(node_candidat)
    
    "Afegim l'aresta del últim node candidat al node destí"
    aresta_cami = dijkstra.DijkstraQueue_Greedy(g,node_actual)
    recorregut_fins_desti = aresta_cami[visits.Vertices[-1]]
    for aresta in recorregut_fins_desti:
        if aresta not in llista:
            llista.append(aresta)
            
    return llista

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

    
def Cost_Recorregut_Actual(llista_arestes):
    """
    Parameters
    ----------
    llista_arestes : List[Edges]
        Llista amb les arestes a calcular la longitud

    Returns
    -------
    cost_actual : Float
        Suma dels pesos de les arestes

    """
    
    cost_actual = 0
    for aresta in llista_arestes:
        cost_actual += aresta.Length
    return cost_actual

def Connexio_Final(visitats_arestes, node_inicial,node_desti,matriu):
    """
    Connecta l'últim punt amb el vèrtex destí

    Parameters
    ----------
    visitats_arestes : List[Edges]
        Llista del recorregut d'arestes final
    node_inicial : Class Vertex
        Punt actual de la recursió
    node_desti : Class Vertex
        Node destí del graf
    matriu : List[List]
        Matriu amb els camins òptims

    Returns
    -------
    visitats_arestes : List[Edges]
        LLista del recorregut modificat amb les arestes finals

    """
    for tupla in matriu[node_inicial.index]:
        if tupla[0] == node_desti:
            for aresta in tupla[2]:
                visitats_arestes.append(aresta)
            break
    
    return visitats_arestes
    
    

def Cota_Inicial(punts_visitar, matriu, node_desti):
    """
    Calcula la cota inferior global
    
    Parameters
    ----------
    matriu : List[List]
        Matriu de distàncies òptimes

    Returns
    -------
    cota: Float
    """
    
    "Iterem tots els vertex a visitar, on trobem en cada el camí més curt i el sumem per donar la cota inicial"
    cota_inferior = 0
    cota_superior = 0
    
    for vertex in punts_visitar:
        try:
            vertex.visitat
        except:
            minim = math.inf
            maxim = 0
            for index,fila in enumerate(matriu):
                if index != node_desti.index:
                    for tupla in fila:
                        if tupla[0] == vertex:
                            if tupla[1] < minim:
                                minim = tupla[1]
                            if tupla[1] > maxim:
                                maxim = tupla[1]
                            break
                            
            cota_inferior += minim
            cota_superior += maxim
            
    return cota_inferior, cota_superior


def Calcular_Cota_Actual(node_origen, matriu, cota_inferior, cota_superior, punt, diccionari_minims, diccionari_maxims):
    """
    Trobem la cota inferior del node actual (tenint en compte la cota anterior i la longitud entre nodes)

    Parameters
    ----------
    node_origen : Class Vertex
        Node actual de l'iteració
    punts_visitar : List[Vertex]
        DESCR
    matriu : List[List]
        Matriu de distàncies òptimes
    cota_actual : float
        Cota que hem de modificar 
    punt : Class Vertex
        Punt que encara hem de recorre al graf

    Returns
    -------
    cost : Float
        Cota mínima del punt calculat
    arestes : List[Edges]
        Llista amb les arestes que porten del node actual al punt

    """

    for tupla in matriu[node_origen.index]:
        if tupla[0] == punt:
            cost = tupla[1]
            arestes = tupla[2]
            break
            
    cota_inferior = cota_inferior - diccionari_minims[punt] + cost
    cota_superior = cota_superior - diccionari_maxims[punt] + cost
    
    # print("PUNT", punt.Name, "INFERIOR:", inferior, "SUPERIOR:", superior)

    return cost,cota_inferior,cota_superior,arestes
    
    
def Trobar_Minim_Maxim(punt, matriu, node_desti):
    """
    Mínim camí per cada columna de la matriu
    
    Parameters
    ----------
    punt : Class Vertex
        Punt en què hem de trobar el mínim camí
    matriu : List[List]
        Matriu amb les distàncies dels camins òptims
    node_desti : Class Vertex
        Vèrtex que volem arribar al final del programa

    Returns
    -------
    minim: float
    arestes: List[Edges] 
    """
    
    minim = math.inf
    maxim = 0
    for index,fila in enumerate(matriu):
        if index != node_desti.index:
            for tupla in fila:
                if tupla[0] == punt:
                    if tupla[1] < minim:
                        minim = tupla[1]
                    if tupla[1] > maxim:
                        maxim = tupla[1]
                    break
                    
    return minim, maxim
                
def Matriu_Camins_Optims(graf, punts_matriu):
    """
    Parameters
    ----------
    graf : Class Graf
        Graf amb un conjunt de nodes i arestes

    Returns
    -------
    matriu : List[List]
        Matriu que conté en cada fila els camins òptims per cada vèrtex del graf

    """
    matriu = []
    for punt in punts_matriu:
        llista = []
        cami_arestes = dijkstra.DijkstraQueue_Greedy(graf, punt)
        for vertex in cami_arestes:
            if vertex not in punts_matriu:
                continue
            pes = 0
            for aresta in cami_arestes[vertex]:
                pes += aresta.Length
            
            if pes != 0:
                llista.append((vertex,pes,cami_arestes[vertex]))
        
        # llista_ordenada = sorted(llista, key=lambda tupla: tupla[0])
        punt.index = len(matriu)
        matriu.append(llista)
    
    return matriu

def BranchAndBound(matriu, node_inicial, node_desti, punts_visitar, cota_inferior, cota_superior, diccionari_minims,diccionari_maxims):
    """
    Parameters
    ----------
    matriu : List[List]
        Matriu que conté en cada fila els camins òptims per cada vèrtex del graf
    node_inicial : Class Vertex
         Node inicial del graf
    node_desti : Class Vertex
        Vèrtex que volem arribar al final del programa
    punts_visitar : List[Vertex]
        Punts que hem de visitar en el graf.
    cota_inferior : Float
    cota_superior : Float
    diccionari_minims : Dict
    diccionari_maxims : Dict
        
    Returns
    -------
    cami_optim : List[Edges]
        Llista amb les arestes del camí òptim
    """
    
    "Paràmetres inicials"
    llista_heuristiques = [(node_inicial,cota_inferior,cota_superior,[],[],0)]

    "Comencem ja com exemple de cost_optim un camí Greedy que ja hem calculat"
    cami_optim = list()
    cost_optim = math.inf    
    
    while llista_heuristiques:
        "Seleccionem el node més prometedor actual"
        node_actual, ct_inferior, ct_superior, arestes, visitats, estimacio = llista_heuristiques.pop(0)

        "En cas que s'hagi visitat tots els nodes obligatòris, el comparem amb la solució òptima"
        if len(visitats) == len(punts_visitar):
            arestes_modificades = Connexio_Final(arestes, node_actual,node_desti,matriu)
            cost_cami = Cost_Recorregut_Actual(arestes_modificades)
            if cost_cami < cost_optim:
                cost_optim = cost_cami
                cami_optim = arestes_modificades
                
                # print("COTA INFERIOR:", ct_inferior)
                # print("COTA SUPERIOR:", ct_superior)
                # print("COST CAMI:", cost_optim)
                # print("ESTIMACIÓ:", estimacio)
                # print("##########################")
        
        "Recorrem tots els punts possibles que podem visitar"
        for punt in punts_visitar:
            if punt not in visitats:
                cost_aresta,cost_inf,cost_sup, arestes_punt = Calcular_Cota_Actual(node_actual,matriu,ct_inferior,ct_superior, punt, diccionari_minims, diccionari_maxims)
                visitats_temporal = visitats + [punt]
                arestes_visitades = arestes + arestes_punt
                
                cost_temporal = Cost_Recorregut_Actual(arestes_visitades)
                if cost_temporal < cost_optim: 
                    tupla = (punt,cost_inf,cost_sup, arestes_visitades,visitats_temporal, cost_sup - cost_inf + cost_temporal)
                    llista_heuristiques.append(tupla)
                            
        
        "Ordenem la llista per la cota inferior més baixa"
        llista_heuristiques.sort(key=lambda tupla: tupla[-1])
        
    return cami_optim
    
    
# SalesmanTrackBranchAndBound2 ===================================================
def SalesmanTrackBranchAndBound2(g, visits):
    """
    Solució del problema del viatjant de comerci amb un algorisme de Branch & Bound
    
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

    "Inicialització dels paràmetres"
    visits.Vertices[0].visitat = True
    
    punts_matriu = set(visits.Vertices)
    punts_visitar = set(visits.Vertices[1:-1])
    graf_retorn = graph.Track(g)
    
    diccionari_minims = dict()
    diccionari_maxims = dict()
    
    "Matriu amb les distàncies òptimes de cada vèrtex a visitar"
    matriu = Matriu_Camins_Optims(g, punts_matriu)
    cota_inferior, cota_superior = Cota_Inicial(punts_matriu,matriu,visits.Vertices[-1])
    
    # print("COTA INFERIOR:", cota_inferior)
    # print("COTA SUPERIOR:", cota_superior)
    # print("################################")

    for vertex in punts_visitar:
        minim,maxim = Trobar_Minim_Maxim(vertex, matriu, visits.Vertices[-1])
        diccionari_minims[vertex] = minim
        diccionari_maxims[vertex] = maxim
    
    "Fem l'algorisme BranchandBound"
    # cami_optim = SalesmanTrackGreedy(g, visits)
    recorregut = BranchAndBound(matriu, visits.Vertices[0], visits.Vertices[-1], punts_visitar, cota_inferior, cota_superior, diccionari_minims,diccionari_maxims)
    
    "Afegim al track el recorregut d'arestes"
    for aresta in recorregut:
        graf_retorn.AddLast(aresta)

    return graf_retorn

