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

		result = self.channel.queue_declare(queue=self.node.ref,durable=True)
		queue_name = result.method.queue

		print("subscribing to the node queue")
		self.channel.queue_bind(exchange='K_Raymond',
		       		queue=queue_name,
		       		routing_key=self.node.ref)
		self.channel.basic_consume(self.callback,queue=queue_name,no_ack=False)

	def beginListen(self):
		self.channel.start_consuming()

	def enterCriticalSection(self):
		self.nodeEvent.enterTheCriticalSection()

	def exitCriticalSection(self):
		self.nodeEvent.exitTheCriticalSection()

	def callback(self,ch, method, properties, body):
		ch.basic_ack(delivery_tag = method.delivery_tag)
		props = body.split("-") #body -> REQUEST-B
		print("Received: " + props[0] + " from : " + props[1])
		if props[0] == "REQUEST":
			self.nodeEvent.receiveRequestMessage(props[1])
		elif props[0] == "PRIVILEGE":
			self.nodeEvent.receivePrivilegeMessage()



