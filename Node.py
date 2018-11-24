import pika

class PikaConnection:


	def sendMessage(self,routing_key,body):
		connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
		channel = connection.channel()
		channel.exchange_declare(exchange='K_Raymond',
                         exchange_type='direct')
		channel.basic_publish(exchange='K_Raymond',
                      routing_key=routing_key,
                      body=body,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
		connection.close()

class Node:

	def __init__(self,ref,neighbors,holderRef):
		self.ref = ref #the name of the node
		self.neighbors = neighbors #the neighbors : a list of node names
		self.holderRef = holderRef #the name of the holder
		self.asked = False # True if the node asked for the privilege
		self.using = False # True if the node is using the priviege
		self.requestQ = [] # FIFO of the requester neighbors
		self.connection = PikaConnection() 
		

	def make_request(self):
		if (self.holderRef != self.ref and not self.asked and len(self.requestQ) != 0):
			print("making request")
			self.connection.sendMessage(self.holderRef,"REQUEST-" + self.ref)
			print("sent request to the node " + self.holderRef)
			self.asked = True
			

	def assign_privilege(self):
		if (self.holderRef == self.ref and not self.using and len(self.requestQ) != 0):
			print("assinging privilege")
			self.holderRef = self.dequeue()
			self.asked = False
			if (self.holderRef == self.ref):
				self.using = True
				self.entreCriticalSection()
			else :
				self.connection.sendMessage(self.holderRef,"PRIVILEGE-" + self.ref)
				print("sent privilege to the node " + self.holderRef)

	def dequeue(self):
		return self.requestQ.pop(0)

	def enqueue(self,neighborRef):
		print("added " + neighborRef + " to requestQ")
		self.requestQ.append(neighborRef)
		


	def entreCriticalSection(self):
		print("Node [" + self.ref + "] : entering the critical section")
	
	def exitCriticalSection(self):
		self.using = False
		print("Node [" + self.ref + "] : exiting the critical section")

	def __repr__(self):
		return "Node: " + self.ref
