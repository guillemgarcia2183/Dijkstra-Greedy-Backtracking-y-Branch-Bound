import subprocess
import sys
import time

sys.path.append('PythonSalesMan')
import graph
import dijkstra
import greedy
import backtracking
import branchAndBound


# ==============================================================================
# IDENTIFICACIO DELS ALUMNES ===================================================
# ==============================================================================
"""
Guillem Garcia Dausà: 1636279
Martí Llinés Viñals: 1637804
"""

graph.NomAlumne1 = "Guillem"
graph.CognomsAlumne1 = "Garcia Dausà"
graph.NIUAlumne1 = "1000000" 

# No modificar si nomes grup d'un alumne

graph.NomAlumne2 = "Martí"
graph.CognomsAlumne2 = "Llinés Viñals"
graph.NIUAlumne2 = "1000000" 

# VERIFICAR ALUMNES =============================================================

graph.TestNIU(graph.NIUAlumne1)
if graph.NIUAlumne2!="": graph.TestNIU(graph.NIUAlumne2)


# EXECUCIO EN PROCESS DE CORRECCIO ==============================================
    
if graph.CorrectionProcess(): sys.exit(0)

# ==============================================================================
# PROVES =======================================================================
# ==============================================================================

# g=graph.Graph()                     					# crear un graf
# g.Load("TestDijkstra/Desconectat.GR")     					# llegir el graf
# g.SetDistancesToEdgeLength()        					# Posar les longituts de les arestes a la distancia entre vertexs
# start=g.GetVertex("Start");         					# Obtenir el vertex origien de les distancies (distancia 0)
# t0 = time.time()                    					# temps inicial
# dijkstra.Dijkstra(g,start)          					# Calcular les distancies
# t1 = time.time()                    					# Temps final
# print("temps: ",t1-t0)              					# imprimir el temps d'execució
# g.DisplayDistances()                					# Visualitza el graf i les distancies

g=graph.Graph()                     					# crear un graf
g.Load("TestSalesMan/RepeatVertex.GR")  				# llegir el graf
g.SetDistancesToEdgeLength()        					# Posar les longituts de les arestes a la distancia entre vertexs
vis=graph.Visits(g);									# Crear visites
vis.Load("TestSalesMan/RepeatVertex.VIS")				# Llegir les vistes
t0 = time.time()                    					# temps inicial
trk=backtracking.SalesmanTrackBacktracking(g,vis)       #Cerca cami que pasi per les visites
t1 = time.time()                    					# Temps final
print("temps: ",t1-t0)              					# imprimir el temps d'execució
trk.Display(vis)                    					# Visualitza el track i les visites sobre el graf el graf