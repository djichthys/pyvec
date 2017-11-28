

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
        self._edges = edges

    @property
    def name( self ):
        return self._name

    @name.setter
    def name( self, val ):
        self._name = val

    @property
    def edges(self):
        return self._edges


    @edges.setter
    def edges(self, edge):
        if type(edge) is list:
            self._edges = edge
        elif type(edge) is Connected_Component :
            self._edges.append(edge)
        else :
            raise TypeError


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



class Node_to_SCC_Map():
    """
    Worker Class to help with connecting strongly connected regions

    """
    def __init__(self, scc):
        self.scc = {}
        if type(scc) is list :
            for supernode in scc:
                for node in supernode.node_list:
                    self.scc[node] = supernode
        elif type(scc) is Connected_Component :
            for node in scc.node_list :
                self.scc[node] = scc

def connect_super_nodes( super_node_list ):
    """
    Function to connect between strongly connected regions
    """
    reverse_map = Node_to_SCC_Map(super_node_list)

    for s_node in super_node_list:
        for node in s_node.node_list:
            for dest in node.successors :
                worker = reverse_map.scc[dest]
                if (worker != s_node) :
                    if s_node.edges == None :
                        s_node.edges = [worker]
                    elif worker not in s_node.edges :
                        s_node.edges.append(worker)

        #Some SCCs will only have incoming edges and no outgoing edges
        if s_node.edges == None :
            s_node.edges = []

    return super_node_list




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







if __name__ == "__main__" :
    #unit-test
    #also a primer on how to use the classes and the function
    init_list = []
    for i in range(1,9,1):
        init_list.append(Graph_Node("{0:02d}".format(i)))


    init_list[0].successors = [init_list[1]]
    init_list[1].successors = [init_list[2]]
    init_list[2].successors = [init_list[0]]
    init_list[3].successors = [init_list[1],init_list[2],init_list[4]]
    init_list[4].successors = [init_list[3],init_list[5]]
    init_list[5].successors = [init_list[2],init_list[6]]
    init_list[6].successors = [init_list[5]]
    init_list[7].successors = [init_list[4],init_list[6],init_list[7]]

    for i in init_list:
        edges = []
        for j in i.successors :
            edges.append(j.name)
        print("name = {0}. type = {1:s}. edges-to {2}".format(i.name,str(type(i.name)), edges))




    scc_list = strongly_connected_components(init_list)
    scc =  connect_super_nodes( scc_list )
    i = 0
    print("================================")
    print("Strongly connected components")
    print("================================")
    for idx in scc:
        print("supernode[{0}] = {1}".format(i , idx.name))
        for idx_j in idx.node_list:
            print("components = {0}".format(idx_j.name))

        j = 0
        for idx_j in idx.edges:
            print("supernode-connections[{0}] = {1}".format(j , idx_j.name))

        print("================================")
        i += 1


    #show diagrammatically
    import graphviz as gv
    orig_graph = gv.Digraph(name="original graph", format="png")
    for node in init_list:
        orig_graph.node(node.name)
        for edge in node.successors:
            orig_graph.edge(node.name,edge.name)

    orig_graph.render("img/orig_graph")

    scc_img = gv.Digraph(name="connected components", format="png")
    for supernode in scc:
        cluster_name = "cluster_" + supernode.name
        with scc_img.subgraph(name=cluster_name) as subg :
            subg.attr(style="filled")
            subg.attr(color="lightgrey")
            subg.node_attr.update(style="filled", color="white")
            subg.attr(label="scc_" + supernode.name)

            for node in supernode.node_list:
                subg.node(node.name)


    #add edges to the nodes already in each
    #subgraph in main graph description
    for src in init_list:
        for dest in src.successors:
            scc_img.edge(src.name,dest.name)

    scc_img.render("img/scc_img")
