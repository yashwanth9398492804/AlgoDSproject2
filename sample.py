
#Name : SATYA SAI RAJESH PARVATAREDDY
#ID: 801328224


import sys
from sys import argv
from queue import *

class Edge(object):                             #The class Edge is used to create objects that represent edges in a graph
    def __init__(self, source_v, destination_v, cost, status):
        self.source_v = source_v              
        self.destination_v = destination_v   #source_v and destination_v are the vertices connected by the edge
        self.status = status                           #status represents the state of the edge
        self.cost = float(cost)                 #cost represents the weight of the edge. The cost is converted to a float data type in the initializer method.


class Priority_Queue(object):       # using binary heap implimenting priority queue
    def __init__(self):
        self.v_List = [] 
       
    def left_ele(self, i):              # Finding left element 
        return (2*i)+1
    
    def right_ele(self, i):              # Finding right element 
        return (2*i)+2

    def Parent_1(self, i):               # finding parent node.
        if i % 2 == 0 and i != 0:
            return int((i/2)-1)
        elif i % 2 != 0:
            return int(i/2)
        else:
            return 0

    # AB will be the list to be heapified,i will be index # n is the length of list AB.
    def minHeapify(self, AB, i, n):                  # Implimentation of  minHeapify function. 
        le = self.left_ele(i)
        ri = self.right_ele(i)
        if le <= n and AB[le][0] < AB[i][0]:
            small = le
        else:
            small = i
        if ri <= n and AB[ri][0] < AB[small][0]:
            small = ri
        if small != i:
            AB[i], AB[small] = AB[small], AB[i]
            self.minHeapify(AB, small, n)

    def dec_Priority(self, AB, i, key):         #here the function is written for decreasing priority key of an element in heap.
        AB[i] = key
        while i > 0 and AB[self.Parent_1(i)][0] > AB[i][0]:
            AB[i], AB[self.Parent_1(i)] = AB[self.Parent_1(i)], AB[i]
            i = self.Parent_1(i)

    def insert_ele(self, AB, ele):        #Inserting an element to the priority queue.
        AB.insert_ele(len(AB), ele)
        self.build_Min_Heap(AB, len(AB))

    def build_Min_Heap(self, AB, n):         #Here building a min heap function
        for i in range(int(n/2)-1, -1, -1):
            self.minHeapify(AB, i, n-1)


    

    

    
    def finding_Min(self, AB):      #here  the function is written to find minimum value from priority queue
        min = AB[0]
        AB[0] = AB[len(AB)-1]
        del AB[len(AB)-1]
        self.minHeapify(AB, 0, (len(AB) - 1))
        return min[1]

class Vertex(object):                              #  Here the Vertex function stores information of all vertices
    def __init__(self, vertex_n, status):
        self.name = vertex_n     
        self.status = status       
        self.Parent_1 = None          
        self.cost = float('inf')    
        self.adj = []              

   
    def resetting(self):                             #here function is for resetting the information 
        self.dist = float('inf')
        self.prev = None
        

       
class Graph(object):    #the Graph class provides a convenient way to store and access information about vertices, edges and the adjacency list of a graph.
   
    def __init__(self):
        self.vertices = {}         
        self.edges = {}            
        self.adjlist = {}     


    def vertexup(self, vertex):              #here function makes the vertex status as up
        self.vertices[vertex].status = True      

    
    def vertexdown(self, vertex):             #here the function makes vertex status as down
        self.vertices[vertex].status = False

    

    def addvertex(self, name, vertex):     #function that adds a new vertex to the graph
        self.vertices[name] = vertex
  
    
   
    def addAdjVertex(self, v1, v2):     #add the vertex in adjacency list
        if v2 == None:
            self.adjlist.setdefault(v1,[])
        else:
            self.adjlist.setdefault(v1,[]).append(v2)    
    
    
    def edgedown(self, v1, v2):            # function makes edge status to down 
        self.edges[(v1, v2)].status = False

    
    def edgeup(self, v1, v2):             # function makes edge status to up.
        self.edges[v1, v2].status = True

    def addedge(self, from_v1_to_v2, edge):        
        if from_v1_to_v2[0] not in self.vertices:          # If source vertex is not already present in the graph, add it.
            self.addvertex(from_v1_to_v2[0], Vertex(from_v1_to_v2[0], True))  
        
        if from_v1_to_v2[1] not in self.vertices:          # If destination vertex is not already present in the graph, add it.
            self.addvertex(from_v1_to_v2[1], Vertex(from_v1_to_v2[1], True))
        
        if (from_v1_to_v2[0], from_v1_to_v2[1]) in self.edges:  # If the edge between the source and destination vertices already exists, update the edge weight.
            self.edges[(from_v1_to_v2[0],from_v1_to_v2[1  ])].cost = float(edge.cost)
        else:
            self.addAdjVertex(from_v1_to_v2[0], from_v1_to_v2[1])     # If the edge doesn't exist, add it to the graph.
            self.addAdjVertex(from_v1_to_v2[1], None)
            self.edges[from_v1_to_v2] = edge
    
    

   
    def deleteEdge(self, v1, v2):      #here the function delete edge from v1 to v2
        del self.edges[(v1,v2)]
        self.adjlist[v1].remove(v2)

    
    
    
    
    def print_Reachable(self):             # Function to print all the reachable vertices from each vertex in the graph.
        for vertex in (sorted(self.vertices.keys())):
            if self.vertices[vertex].status == True:
                self.reachable(vertex)

    def print_Graph(self):            #function prints out the graph with each vertex and its adjacent vertices and the corresponding edge weights
        for v in sorted(self.vertices.keys()):
            if self.vertices[v].status == False:
                print(self.vertices[v].name, "DOWN")
            else:
                print(self.vertices[v].name) 

            for adj_vertex in sorted(self.adjlist[v]):
                if (self.edges[(v,adj_vertex)].status == False): 
                    print(" ", adj_vertex,self.edges[(v,adj_vertex)].cost, "DOWN")  
                else:
                    print(" ", adj_vertex,self.edges[(v,adj_vertex)].cost)  

   #This function implements a BFS algorithm to find all reachable vertices from a given vertex in the graph.
   #The time complexity of this function is O(V+E) 
   #for the worst-case scenario, where all vertices and edges are up, the time complexity would be O(V*(V + E)).

    def reachable(self, vertex):        
        discovered_vertices = {}
        reachable_vertices = {}
        for ver in self.vertices.keys():
            discovered_vertices[ver] = "white" 
        discovered_vertices[vertex] = "gray"        
        queue = Queue()
        queue.put(vertex)
        while not queue.empty():
            get = queue.get()
            for v in sorted(self.adjlist[get]):
                if discovered_vertices[v] == "white" and self.vertices[v].status == True and self.edges[(get,v)].status == True:
                    discovered_vertices[v] == "gray"
                    queue.put(v)
                    reachable_vertices[v] = v
            discovered_vertices[get] = "black"
        print(vertex)
        for vert in sorted(reachable_vertices):
            print(" ", vert)
        
    
    

   #shortest path from source to destination will be calculated 
    #This function implements Dijkstra's algorithm using a priority queue based on a binary min heap.
    # The time complexity of this algorithm is O((|V|+|E|)lnV), where |V| is the number of vertices and |E| is the number of edges in the graph.
    def path(self, source, destination):
        pq = Priority_Queue()
        for vertex in self.vertices.keys():
            self.vertices[vertex].Parent_1 = None
            self.vertices[vertex].cost = float('inf')
        self.vertices[source].cost = 0.0
        dist = []
        for w in self.vertices:
            dist.insert(len(dist), (self.vertices[w].cost, self.vertices[w]))
        pq.build_Min_Heap(dist, len(dist))  
        s = []  
        while dist:
            v = pq.finding_Min(dist)  
            if v.status == False:  
                continue
            else:
                s.insert(len(s), v)  
                for ele in self.adjlist[v.name]:  
                    if self.vertices[ele].status == True and self.edges[(v.name, ele)].status == True:
                        prevDistance = self.vertices[ele].cost
                        if self.vertices[ele].cost > (self.vertices[v.name].cost + self.edges[(v.name,ele)].cost) :
                            self.vertices[ele].cost = self.vertices[v.name].cost + self.edges[(v.name,ele)].cost
                            self.vertices[ele].Parent_1 = v
                            index = dist.index((prevDistance, self.vertices[ele]))
                            pq.dec_Priority(dist, index, (self.vertices[ele].cost, self.vertices[ele]))
        node = self.vertices[destination]
        while node.Parent_1 is not None:   #Displaying vertices in correct order
            dist.append(node.name)
            node = node.Parent_1
        dist.append(node.name)
        dist.reverse()
        print(" ".join([str(vert) for vert in dist]),"%.2f" % self.vertices[destination].cost)

    def clear_All(self):    #This function is used to reset all the vertices in the graph
        for vertex in self.vertices.values():
            vertex.resetting()


#The main() function reads the input file provided as a command line argument and initializes a graph object.
# It then reads the queries from the standard input until the "quit" command is received.
def main():
    input_file = argv[1]
    f = open(input_file,'r')
    graph = Graph()
    for line in f: 
        node = line.split()
        if len(node) != 3:
            print("Invalid line ", end="")
            print(node)
            exit()
        else:
            v1 = Vertex(line.split()[0], True)  # vertex 1 and vertex 2
            v2 = Vertex(line.split()[1], True)  
            graph.addvertex(v1.name,v1)         # adding vertex 1 and vertex 2
            graph.addvertex(v2.name,v2)        
            edge1 = Edge(line.split()[0], line.split()[1], line.split()[2], True)   # make edge 1 and edge 2
            edge2 = Edge(line.split()[1], line.split()[0], line.split()[2], True)  
            graph.addedge((v1.name, v2.name), edge1)    # adding edge 1 and edge 2
            graph.addedge((v2.name, v1.name), edge2)    
    
    f.close()   # close the input graph file

    # reading the queries.
    while True:
        line = sys.stdin.readline()
        if line.strip():
            input_cmd = line.split()
            if len(input_cmd) == 4:
                if input_cmd[0] == "addedge":   #If the query is a "addedge" command, it creates a new edge object and adds it to the graph using the addedge() method.
                    e1 = Edge(input_cmd[1], input_cmd[2], input_cmd[3], True)
                    graph.addedge((input_cmd[1],input_cmd[2]), e1)
                else:
                    print("Command Incorrect.")

            elif len(input_cmd) == 3:
                if input_cmd[0] == "deleteedge":   #If the query is a "deleteedge" command, it removes the edge between the two vertices using the deleteEdge() method.
                    graph.deleteEdge(input_cmd[1], input_cmd[2])

                elif input_cmd[0] == "edgedown":  #If the query is a "edgedown" command, it reduces the cost of the edge between the two vertices using the edgedown() method.
                    graph.edgedown(input_cmd[1], input_cmd[2])

                elif input_cmd[0] == "edgeup":    #If the query is a "edgeup" command, it increases the cost of the edge between the two vertices using the edgeup() method.
                    graph.edgeup(input_cmd[1], input_cmd[2])

                elif input_cmd[0] == "path":     #If the query is a "path" command, it calculates the shortest path between the two vertices using Dijkstra's algorithm and prints the path and its cost using the path() method.
                    if input_cmd[1] not in graph.vertices.keys():
                        print("Source Vertex Can Not be found.")
                    
                    elif input_cmd[2] not in graph.vertices.keys():
                        print("Destination Vertex Can Not be found.")
                    
                    else:
                        graph.path(input_cmd[1],input_cmd[2])

                else:
                    print("Command Incorrect.")

            elif len(input_cmd) == 2:      #If the query is a "vertexdown" command, it sets the status of the vertex to inactive using the vertexdown() method.
                if input_cmd[0] == "vertexdown":
                    graph.vertexdown(input_cmd[1])

                elif input_cmd[0] == "vertexup":   #If the query is a "vertexup" command, it sets the status of the vertex to active using the vertexup() method.
                    graph.vertexup(input_cmd[1])

                else:
                    print("Command Incorrect.")
    #If the query is a "reachable" command, it prints all the vertices that can be reached from all active vertices in the graph 
    #using the print_Reachable() method.
            elif len(input_cmd) == 1:      
                if input_cmd[0] == "reachable":
                    graph.print_Reachable()

                elif input_cmd[0] == "print":  #If the query is a "print" command, it prints the graph and its properties using the print_Graph() method.
                    graph.print_Graph()
                
                elif input_cmd[0].lower() == "quit":   #If the query is a "quit" command, the loop is broken and the program terminates.
                    break

                else:     #If the query is an invalid command or does not follow the correct format, an error message is printed.
                    print("Command Incorrect.")
                
            else:
                print("Command Incorrect.")

# calling main function
if __name__ == '__main__':
    main()
