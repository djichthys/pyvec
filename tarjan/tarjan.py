

class Graph_Node(): 
    """
    Graph Node contains 
      id : name of the node as a string 
      edges : list of nodes that this node connects to - representative of outgoing edges
    """ 
    def __init__( self, name , edges=None ):
        self.name= name 
        self.successors = edges 

class Connected_Component():
    """
    Connected Component Class holds a list of Graph-Nodes that are strongly connected
      name : name of the SCC as a string 
      edges : list of other SCCs  that this SCC connects to - representative of outgoing edges
      node_list : list of Graph Nodes contained within this SCC
    """ 
    def __init__(self, node_list, name=None, edges=None): 
        self._name = name 
        self.node_list = node_list 
        self.edges = edges 

    @property
    def name( self ): 
        return self._name

    @name.setter
    def name( self, val ):
        self._name = val 


    def create_id( self, new_name=None ):
        if(new_name == None):   # add random name generator later on 
            generated_id = "__anonymous"
        elif type(new_name) is str : 
            generated_id = new_name 
        elif (type(new_name) is int 
              or type(new_name) is float):
            generated_id = str(new_name) 
        elif type(new_name) is list:
            iterator = iter(new_name) 
            if type(new_name[0]) is str : 
                generated_id = iterator.__next__() 
                while(True):
                    try:
                        nxt = iterator.__next__() 
                        generated_id += "_" + nxt 
                    except StopIteration: 
                        break
            elif (type(new_name[0]) is int 
                   or type(new_name[0]) is float):
                generated_id = str(iterator.__next__())
                while(True):
                    try:
                        nxt = str(iterator.__next__())
                        generated_id += "_" + nxt 
                    except StopIteration: 
                        break
            else: #type is Graph_Node
                generated_id = iterator.__next__().name 
                while(True):
                    try:
                        nxt = iterator.__next__().name
                        generated_id += "_" + nxt
                    except StopIteration: 
                        break
        else:
            try :
                generated_id = new_name.name
            except AttributeError : 
                raise AttributeError("attr - name does not exist. Only custom class type allowed is type Graph_Node") 
        return generated_id 
                

def strongly_connected_components( graph ):
    """
    Tarjan's algorithm : input should be the complete list of Nodes 
    with outgoing edges already encoded 
    """ 
    index = 0 
    stack = [] 
    component_graph = [] #should contain list of Connected_Components()



    def strong_connect( node ):
        """
        node : node at which to start further searh. 
        Note that this function will be called recursively
        """ 
        nonlocal index 
        node.index = index 
        node.lowest_link = index    #initialise to current index - might change later
        index += 1 
        stack.append( node ) 
        node.on_stack = True 
    
        for successor in node.successors : 
            if not(hasattr(successor,"index")) : 
                #successor has not yet been visited - recurse on this node 
                strong_connect( successor ) 

                # either this node is the root of an SCC or 
                # this node is on the only path from the root node or 
                # the successor node has an edge to a node closer to the root node 
                # than the current node
                node.lowest_link = min( node.lowest_link, successor.lowest_link )
            elif (hasattr(successor,"on_stack") and successor.on_stack == True) :
                #Successor is already on stack => already visited 
                node.lowest_link = min( node.lowest_link, successor.index ) 
        
        #if node is a root node, pop stack and generate an Strongly connected component
        if node.lowest_link == node.index :
            connected_components = [] 
            while True : 
                component = stack.pop() 
                component.on_stack = False
                connected_components.append( component ) 
                if component == node :
                    break
            # compute edges to new set 
            scc_list = list(connected_components)
            super_node = Connected_Component(scc_list)
            super_node.name = super_node.create_id(scc_list)
            component_graph.append(super_node) 
        

    for node in graph:
        if not(hasattr(node,"index")) : 
            strong_connect(node)

    return component_graph  








#unit-test
#also a primer on how to use the classes and the function 
init_list = [] 
for i in range(1,9,1):
    init_list.append(Graph_Node("{0:02d}".format(i)))


init_list[0].successors = [init_list[1]]
init_list[1].successors = [init_list[2]]
init_list[2].successors = [init_list[0]]
init_list[3].successors = [init_list[1],init_list[2],init_list[4]] 
init_list[4].successors = [init_list[3],init_list[3]]
init_list[5].successors = [init_list[2],init_list[6]]
init_list[6].successors = [init_list[5]]
init_list[7].successors = [init_list[7],init_list[6],init_list[7]]

for i in init_list:
    edges = [] 
    for j in i.successors :
        edges.append(j.name) 
    print("name = {0}. type = {1:s}. edges-to {2}".format(i.name,str(type(i.name)), edges))




scc_list = strongly_connected_components(init_list)
i = 0 
for idx in scc_list : 
    print("supernode[{0}] = {1}".format(i , idx.name))
    for idx_j in idx.node_list:
        print("components = {0}".format(idx_j.name))
    print("================================")
    i += 1 

