#!/usr/bin/python3 

class Column_Element :
	def __init__(self , node):
		self.node = node 
		self.type = node.__class__.__name__ 

class Row: 
	def __init__( self, node=None ) :
		if node == None :
			self.rows = [] 
		elif type(node) == list: 
			self.rows = [] 
			for child in node : 
				self += child 
		else : 
			self.rows = list([node]) 

	def __iadd__( self , col_elmnt ):
		if col_elmnt.__class__.__name__ != "Column_Element":
			raise TypeError("Can only add elements of type Column_Elemen") 

		self.rows.append( col_elmnt ) 
		return self 

	def display(self):
		for idx , col_element in enumerate(self.rows): 
			print("rows have element[{0}] = [{1}] ".format(idx, col_element.type))
		

if __name__ == '__main__':
	elements = [ Column_Element(i) for i in range(0,10,1) ] 
	
	row = Row( elements ) 

	row.display() 
