# Classes per la representació de grafs i altres estructures per la pràctica
import math
import sys
import subprocess
import time

# sys.path.append('PythonSalesMan')
import dijkstra
import greedy
import backtracking
import branchAndBound

# VERTEX =======================================================================

class Vertex:
    def __init__(self, name, x, y):
        self.Name = name
        self.x = x
        self.y = y
        self.Edges = []
        self.DijkstraDistance = 0
# EDGE =========================================================================

class Edge:
    def __init__(self,name,length,origin,destination):
        self.Name = name
        self.Length = length
        self.Origin = origin
        self.Destination = destination
        self.ReverseEdge = []
        self.Saved=False

# GRAPH =======================================================================

class Graph:
    def __init__(self):
        self.Vertices = []
        self.Edges = []

    def NewVertex(self, name, x, y):
        v=Vertex(name, x, y)
        self.Vertices.append(v)
        return v

    def GetVertex(self,name):
        for v in self.Vertices:
            if v.Name==name: return v
        else: raise Exception('el vertex ', name,' no existeix')

    def FindVertex(self,name,notFound):
        for v in self.Vertices:
            if v.Name==name: return v
        return notFound

    def NewEdge(self,name,value,origin,destination):
        e=Edge(name,value,origin,destination)
        r=Edge(name+"$Reverse",value,destination,origin)
        e.ReverseEdge=r
        r.ReverseEdge=e
        self.Edges.append(e)
        origin.Edges.append(e)
        self.Edges.append(r)
        destination.Edges.append(r)
        return e

    def GetEdge(self,name):
        for e in self.Edges:
            if e.Name==name: return e
        else: raise Exception('l\'aresta ', name,' no existeix')

    def SetDistancesToEdgeLength(self):
        for e in self.Edges:
            dx=e.Destination.x-e.Origin.x
            dy=e.Destination.y-e.Origin.y
            e.Length=math.sqrt(dx*dx+dy*dy)

    def Load(self,filename):
        f=open(filename,'r')
        l=f.readline()
        if l!='GRAPH 1.0\n': raise Exception(filename, 'no es un fitxer de graph')
        l = f.readline()
        if l[0:11]=='BACKGROUND ' : l=f.readline()
        if l!='UNDIRECTED\n': raise Exception('nomes es poden llegir grafs no dirigits')
        l = f.readline()
        if l != 'VERTICES\n': raise Exception('no es troba la llista de vertexs')
        self.Vertices=[]
        self.Edges=[]
        l=f.readline()
        while l!='EDGES\n':
            l=l.split()
            v=self.NewVertex(l[0],float(l[1]),float(l[2]))
            l = f.readline()
        l = f.readline()
        while l!='':
            l = l.split()
            v1=self.GetVertex(l[2])
            v2=self.GetVertex(l[3])
            e = self.NewEdge(l[0], float(l[1]), v1, v2)
            l = f.readline()
        f.close()

    def Save(self,filename):
        f=open(filename,'w')
        f.write('GRAPH 1.0\n')
        f.write('UNDIRECTED\n')
        f.write('VERTICES\n')
        for v in self.Vertices:
            f.write(str(v.Name)+' '+str(v.x)+' '+str(v.y)+'\n')
        f.write('EDGES\n')
        for e in self.Edges: e.Saved=False
        for e in self.Edges:
            if not e.Saved:
                f.write(str(e.Name)+' '+str(e.Length)+' '+str(e.Origin.Name)+' '+str(e.Destination.Name)+'\n')
                e.ReverseEdge.Saved=True
        f.close()

    def Display(self):
        self.Save("Display.gr")
        subprocess.Popen(["GraphApplicationProf.exe", "display", "Display.GR"])

    def LoadDistances(self,filename):
        f=open(filename,'r')
        l=f.readline()
        if l!='DISTANCES 1.0\n': raise Exception(filename, 'no es un fitxer de distancies')
        l = f.readline()
        while l:
            l=l.split()
            self.GetVertex(l[0]).DijkstraDistance=float(l[1])
            l = f.readline()
        f.close()

    def SaveDistances(self,filename):
        f=open(filename,'w')
        f.write('DISTANCES 1.0\n')
        for v in self.Vertices:
            f.write(str(v.Name)+' '+str(v.DijkstraDistance)+'\n')
        f.close()

    def DisplayDistances(self):
        self.Save("Display.gr")
        self.SaveDistances("Display.dis")
        subprocess.Popen(["GraphApplicationProf.exe", "display", "Display.GR", "Display.dis"])

# Visits ======================================================================

class Visits:
    def __init__(self,g):
        self.Graph=g
        self.Vertices=[]

    def Load(self,filename):
        f=open(filename,'r')
        l=f.readline()
        if l!='VISITS 1.0\n': raise Exception(filename, 'no es un fitxer de visites')
        l = f.readline()
        self.Vertices=[]
        while l:
            l=l.rstrip('\n')
            self.Vertices.append(self.Graph.GetVertex(l))
            l = f.readline()
        f.close()

    def Save(self,filename):
        f=open(filename,'w')
        f.write('VISITS 1.0\n')
        for v in self.Vertices: f.write(str(v.Name)+'\n')
        f.close()

    def Display(self):
        self.Graph.Save("Display.gr")
        self.Save("Display.vis")
        subprocess.Popen(["GraphApplicationProf.exe", "display", "Display.gr", "Display.vis"])

# Track ========================================================================

class Track:
    def __init__(self,g):
        self.Graph=g
        self.Edges=[]

    def AddFirst(self,edge):
        self.Edges.insert(0,edge)

    def AddLast(self,edge):
        self.Edges.append(edge)

    def Append(self,trk):
        self.Edges.extend(trk.Edges)

    def AppendBefore(self,trk):
        self.Edges[0:0]=trk.Edges

    def Load(self,filename):
        f=open(filename,'r')
        l=f.readline()
        if l!='TRACK 1.0\n': raise Exception(filename, 'no es un fitxer de track')
        l = f.readline()
        self.Edges=[]
        while l:
            l=l.rstrip('\n')
            self.Edges.append(self.Graph.GetEdge(l))
            l = f.readline()
        f.close()

    def Save(self,filename):
        f=open(filename,'w')
        f.write('TRACK 1.0\n')
        for e in self.Edges: f.write(str(e.Name)+'\n')
        f.close()

    def Display(self,visits=False):
        self.Graph.Save("Display.gr")
        self.Save("Display.trk")
        if visits:
            visits.Save("Display.vis")
            subprocess.Popen(["GraphApplicationProf.exe", "display", "Display.gr", "Display.trk", "Display.vis"])
        else: subprocess.Popen(["GraphApplicationProf.exe", "display", "Display.gr", "Display.trk"])

# TestNIU ======================================================================

def TestNIU(niu):
    f = open('NIUSAlumnes.csv', 'r')
    l = f.readline()
    while l:
        l=l.rstrip('\n')
        if l==niu:
            f.close()
            return
        l = f.readline()
    f.close()
    raise Exception('el NIU no correspon a un alumne', niu)

# CorrectionProcess ============================================================

def CorrectionProcess():
    args=sys.argv
    # print(args)
    if len(args)<3: return False
    print("Nom Alumne 1.....:",NomAlumne1)
    print("Cognoms Alumne 1.:",CognomsAlumne1 )
    print("NIU Alumne 1.....:",NIUAlumne1)
    print()
    if NIUAlumne2 != "":
        print("Nom Alumne 2.....:",NomAlumne2)
        print("Cognoms Alumne 2.:",CognomsAlumne2)
        print("NIU Alumne 2.....:",NIUAlumne2)
        print()
    if len(args)==4 and args[1]=="DIJKSTRA":
        print("Algoritmo..:",args[1])
        print("Grafo......:",args[2])
        print("Distancias.:",args[3])
        g=Graph()
        g.Load(args[2])
        g.SetDistancesToEdgeLength()
        start=g.FindVertex("Start",g.Vertices[0])
        t0=time.time()
        dijkstra.Dijkstra(g,start)
        t1=time.time()
        print("TIEMPO DE EJECUCION:",t1-t0)
        g.SaveDistances(args[3])
        return True
    elif len(args)==4 and args[1]=="DIJKSTRAQUEUE":
        print("Algoritmo..:",args[1])
        print("Grafo......:",args[2])
        print("Distancias.:",args[3])
        g=Graph()
        g.Load(args[2])
        g.SetDistancesToEdgeLength()
        start=g.FindVertex("Start",g.Vertices[0])
        t0=time.time()
        dijkstra.DijkstraQueue(g,start)
        t1=time.time()
        print("TIEMPO DE EJECUCION:",t1-t0)
        g.SaveDistances(args[3])
        return True
    elif len(args)==5 and args[1]=="GREEDY":
        print("Algoritmo..:",args[1])
        print("Grafo......:",args[2])
        print("Visitas....:",args[3])
        print("Track......:",args[4])
        g=Graph()
        g.Load(args[2])
        g.SetDistancesToEdgeLength()
        vis=Visits(g)
        vis.Load(args[3])
        t0=time.time()
        trk = greedy.SalesmanTrackGreedy(g, vis)
        t1=time.time()
        print("TIEMPO DE EJECUCION:",t1-t0)
        trk.Save(args[4])
        return True
    elif len(args)==5 and args[1]=="BACKTRACKING":
        print("Algoritmo..:",args[1])
        print("Grafo......:",args[2])
        print("Visitas....:",args[3])
        print("Track......:",args[4])
        g=Graph()
        g.Load(args[2])
        g.SetDistancesToEdgeLength()
        vis=Visits(g)
        vis.Load(args[3])
        t0=time.time()
        trk = backtracking.SalesmanTrackBacktracking(g, vis)
        t1=time.time()
        print("TIEMPO DE EJECUCION:",t1-t0)
        trk.Save(args[4])
        return True
    elif len(args)==5 and args[1]=="BACKTRACKINGGREEDY":
        print("Algoritmo..:",args[1])
        print("Grafo......:",args[2])
        print("Visitas....:",args[3])
        print("Track......:",args[4])
        g=Graph()
        g.Load(args[2])
        g.SetDistancesToEdgeLength()
        vis=Visits(g)
        vis.Load(args[3])
        t0=time.time()
        trk = backtracking.SalesmanTrackBacktrackingGreedy(g, vis)
        t1=time.time()
        print("TIEMPO DE EJECUCION:",t1-t0)
        trk.Save(args[4])
        return True
    elif len(args)==5 and args[1]=="BRANCHANDBOUND1":
        print("Algoritmo..:",args[1])
        print("Grafo......:",args[2])
        print("Visitas....:",args[3])
        print("Track......:",args[4])
        g=Graph()
        g.Load(args[2])
        g.SetDistancesToEdgeLength()
        vis=Visits(g)
        vis.Load(args[3])
        t0=time.time()
        trk = branchAndBound.SalesmanTrackBranchAndBound1(g, vis)
        t1=time.time()
        print("TIEMPO DE EJECUCION:",t1-t0)
        trk.Save(args[4])
        return True
    elif len(args)==5 and args[1]=="BRANCHANDBOUND2":
        print("Algoritmo..:",args[1])
        print("Grafo......:",args[2])
        print("Visitas....:",args[3])
        print("Track......:",args[4])
        g=Graph()
        g.Load(args[2])
        g.SetDistancesToEdgeLength()
        vis=Visits(g)
        vis.Load(args[3])
        t0=time.time()
        trk = branchAndBound.SalesmanTrackBranchAndBound2(g, vis)
        t1=time.time()
        print("TIEMPO DE EJECUCION:",t1-t0)
        trk.Save(args[4])
        return True
    elif len(args)==5 and args[1]=="BRANCHANDBOUND3":
        print("Algoritmo..:",args[1])
        print("Grafo......:",args[2])
        print("Visitas....:",args[3])
        print("Track......:",args[4])
        g=Graph()
        g.Load(args[2])
        g.SetDistancesToEdgeLength()
        vis=Visits(g)
        vis.Load(args[3])
        t0=time.time()
        trk = branchAndBound.SalesmanTrackBranchAndBound3(g, vis)
        t1=time.time()
        print("TIEMPO DE EJECUCION:",t1-t0)
        trk.Save(args[4])
        return True
    return False

# Display ======================================================================

def DisplayDistances(graf):
    graf.Save("Display.gr")
    graf.SaveDistances("Display.dis")
    subprocess.Popen(["GraphApplicationProf.exe", "display", "Display.GR", "Display.dis"])