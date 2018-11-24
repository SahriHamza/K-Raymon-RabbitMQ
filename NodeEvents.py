from Node import Node

class NodeEvents:

	def __init__(self,node):
		self.node = node

	def enterTheCriticalSection(self):
		self.node.enqueue(self.node.ref) 
		self.node.assign_privilege()	
		self.node.make_request()
	
	def receiveRequestMessage(self,nodeRef):
		self.node.enqueue(nodeRef)
		self.node.assign_privilege()
		self.node.make_request() 

	def receivePrivilegeMessage(self):
		self.node.holderRef = self.node.ref
		self.node.assign_privilege()
		self.node.make_request()

	def exitTheCriticalSection(self):
		self.node.using = False
		self.node.assign_privilege()
		self.node.make_request()
