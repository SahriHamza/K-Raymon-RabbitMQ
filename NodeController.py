from NodeEvents import NodeEvents
from Node import Node
import pika

class NodeController:
	
	def __init__(self,ref,neighbors,holderRef):
		self.node = Node(ref,neighbors,holderRef)
		self.nodeEvent = NodeEvents(self.node)
		self.channel = None
	
	def init_channel(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		self.channel = connection.channel()

		self.channel.exchange_declare(exchange='K_Raymond',
			 exchange_type='direct')

		result = self.channel.queue_declare(exclusive=True)
		queue_name = result.method.queue

		print("subscribing to the node queue")
		self.channel.queue_bind(exchange='K_Raymond',
		       		queue=queue_name,
		       		routing_key=self.node.ref)
		self.channel.basic_consume(self.callback,queue=queue_name,no_ack=True)

	def beginListen(self):
		self.channel.start_consuming()

	def enterCriticalSection(self):
		self.nodeEvent.enterTheCriticalSection()

	def exitCriticalSection(self):
		self.nodeEvent.exitTheCriticalSection()

	def callback(self,ch, method, properties, body):
		props = body.split("-") #body -> REQUEST-B
		print("Received: " + props[0] + " from : " + props[1])
		if props[0] == "REQUEST":
			self.nodeEvent.receiveRequestMessage(props[1])
		elif props[0] == "PRIVILEGE":
			self.nodeEvent.receivePrivilegeMessage()



