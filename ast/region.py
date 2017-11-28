#!/usr/bin/python3

import ast 
#
# 1. Travel node and create stack of interesting nodes 
#       1.1 create 3-D lattice of interesting nodes
#	    ie Function definitions , loop-ranges, loop-body defs & associated variable dependencies
#
# 2. For each function 
#       do tarjan() + codegen annotation algorithm () 
# 3. create kernels 
#
# 4. loop-fusion (neighbouring type node aggregator) 
# 5. 
#
import ast 
import weakref


def iter_node(node): 
	fields = getattr(node,"_fields", None) 
	if fields is not None : 
		for name in fields : 
			val = getattr(node,name,None) 
			if val is not None: 
				yield name, val 
	elif isinstance(node, list):
		print("_fields not available, iterating list instead")
		for value in node:
			yield "list-val" , val 




class For_Limits(ast.NodeVisitor) :
    def __init__( self, for_iter_node ):
        self.node = weakref.ref(for_iter_node)
        self.std_iterator = None 
        self.std_iterator_ctx = None 
        self.limits = { "start" : ("lazy", None) , 
                        "end"   : ("lazy", None) , 
                        "step"  : ("lazy", None) } 
        self.__init_extract__() 


    def __init_range_limit_args( self, range_lim_args): 
        if type(range_lim_args) is list : 
            print("entering __init_range_limit_args")
            if len(range_lim_args) == 1 : 
                self.limits["start"] = ("imm", 0)
                self.limits["step"] = ("imm", 1)
                if type(range_lim_args[0]) is weakref : 
                    try : 
                        eval_arg = ast.literal_eval(range_lim_args[0]())
                        self.limits["end"] =  ("imm", eval_arg)
                    except ValueError as excpt : 
                        self.limits["end"] =  ("lazy", range_lim_args[0])
                        print("cannot eval [{0}] immediately".format(excpt))
                else : 
                    try : 
                        eval_arg = ast.literal_eval(range_lim_args[0])
                        self.limits["end"] =  ("imm", eval_arg)
                    except Exception as excpt : 
                        self.limits["end"] =  ("lazy", weakref.ref(range_lim_args[0]))
                        print(">>>>>>>>>>> cannot eval [{0}] immediately".format(excpt))
            else : 
                print("entering __init_range_limit_arg else")
                for key,arg in zip(["start", "end", "step"] , range_lim_args) : 
                    print("entering __init_range_limit_arg else for type = {0}".format((type(arg))))
                    if type(arg) is weakref : 
                        try : 
                            eval_arg = ast.literal_eval(arg())
                            self.limits[key] =  ("imm", eval_arg)
                        except ValueError as excpt : 
                            self.limits[key] =  ("lazy", arg)
                            print("cannot eval [{0}] immediately".format(excpt))
                    else : 
                        try : 
                            eval_arg = ast.literal_eval(arg)
                            self.limits[key] =  ("imm", eval_arg)
                        except Exception as excpt : 
                            self.limits[key] =  ("lazy", weakref.ref(arg))
                            print(">>>>>>>>>>> cannot eval [{0}] immediately".format(excpt))

    def __init_extract__(self):
        print("         __extract() --> type(self.node == {0}".format(type(self.node())))
        if type(self.node()) is ast.Call : 
            if 'func' in self.node()._fields :
                if self.node().func.id == 'range': 
                    self.std_iterator = self.node().func.id
                    self.std_iterator_ctx = self.node().func.ctx 
                    self.__init_range_limit_args(self.node().args)
                    print("limits = {0}".format(self.limits))
            for name,val in iter_node(self.node()): 
                print("             iter call args ######### name = {0} -> val  = {1} ".format(name,val))
                if name == 'func'  and type(val) is ast.Name :
                    for arg_name,arg_val in iter_node(val): 
                        print("                 func-name args ######### name = {0} -> val  = {1} ".format(arg_name,arg_val))
        else : 
            print("Something went wrong") 

    def back_patch(self, elmement_type, val) :
        pass 


class For_Targets(ast.NodeVisitor):
	def __init__(self, node) : 
		self.target = []  
		self.__rexpand__(node) 

	def visit_Name(self, node) : 
		self.target.append(node.id) 
		
	def __rexpand__(self, node) : 
		if type(node) is ast.Name : 
			self.target.append(node.id) 
		else :
			self.generic_visit(node) 

# indent level, statement-no  |  { "for_targets" : for_targets, "for_limits" : for_limits } 
#                           , |  non-loop statements 
class CodeStructure: 
	def __init__(self, nest_level , node ):
		if type(node) is weakref : 
			self._node = node 
		else :
			self._node = weakref.ref(node) 
		self._nest_level = nest_level 
		self._lineno = node.lineno 


	def demux_type( self, node ):
		if type(node) is weakref : 
			_node = node() 
		else : 
			_node = node 
		


class Accumulator(ast.NodeVisitor):
	def __init__( self, node=None ) :
		self.visit_stack = []  # every visited node
		self.poi_stack = []    # nearest interesting parent node
		self.context = None
		self.nest_level = 0 
		self.skeleton = [] 
		if node == None : 
			self._func_list = []      # this acts as a list of functions

			

	def generic_visit(self, node, nest_level=-1 , push=True ):
		"""
		   push - Boolean - True - generic visit should push onto stack
		          False : specialised function would have already pushed onto stack
		          in both cases the generic visit will pop() off stack
		""" 
		
		if push == True :
			self.visit_stack.append(weakref.ref(node))

		if nest_level > -1 :
			self.nest_level = nest_level 

		super().generic_visit(node) 

		if push == True :
			self.visit_stack.pop() 
		if nest_level > -1 :
			self.nest_level -= 1 
		


	def visit_FunctionDef(self, node):
		self._func_list.append(node) 

		self.poi_stack.append(weakref.ref(node))
		self.visit_stack.append(weakref.ref(node)) 
		for name, val in iter_node(node):
			print("FuncDef >>>>> name = {0} -- val = {1}".format(name, val))

		for idx , b_field in enumerate( node.body) :
			print("{0:03d} --> {1}".format(idx, b_field)) 

		self.generic_visit(node, self.nest_level + 1 , False) 
		self.poi_stack.pop() 

	

	def visit_For(self, node):
		if type(self.poi_stack[-1]()) is ast.FunctionDef :
			print("First indentation of For loop") 
		elif type(self.poi_stack[-1]()) is ast.For :
			print("nest level of For loop {0}".format(len(self.poi_stack))) 

		self.poi_stack.append(weakref.ref(node)) 
		self.visit_stack.append(weakref.ref(node))
		for_limits = For_Limits( getattr(node,"iter", None)) 
		for_targets = For_Targets( getattr(node,"target", None)) 
		for name, val in iter_node(node):
			print("For - >>>>> name = {0} -- val = {1}".format(name, val))
			if name == "iter":
				print("For - >>>>> limits =  {0} - class-type[{1}] ".format(for_limits.limits, type(for_limits)))
			elif name == "target" :
				print("For - >>>>> targets =  {0} - class-type[{1}] ".format(for_targets.target, type(for_targets)))

		if True :
			self.generic_visit(node, -1, False)
		else :
			self.generic_visit(node, -1, False)
		self.poi_stack.pop() 


	def display_func_list( self ) :
		for idx, node in enumerate(self._func_list): 
			print("function[{0:d}] = {1:s} , line={2} , col = {3} ".format(idx, node.name, node.lineno , node.col_offset))


if __name__ == '__main__':
	with open("test.py", mode="r") as fd : 
		code = fd.read() 
		tree = ast.parse( code ) 

	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>") 
	print(ast.dump(tree,True, True)) 
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>") 
	acc = Accumulator() 
	acc.visit(tree) 
	acc.display_func_list() 

		
