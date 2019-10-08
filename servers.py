import json


class Serverlist:

	def __init__(self,data):
		self.__dict__ = json.loads(data)
		self.serverlist, nr = [], 0
		for entry in self.__dict__['servers']['server']:
			self.serverlist.append(Server(entry, nr))
			nr += 1

	def show(self):
		data = []
		for server in self.serverlist:
			data.append(server.get())
		template = "{0:3}| {1:20}|{2:4}|{3:6}|{4:10}"
		print(template.format("#ID", "Hostname", "CPUs", "Memory", "State"))
		for i in data:
			print(template.format(*i))

	def getserverbyid(self,nr):
		return self.serverlist[nr].uuid

	def getserverhostnamebyuuid(self, uuid):
		for server in self.serverlist:
			if server.uuid == uuid:
				return server.hostname
		return "Not found"


class Server:

	def __init__(self, attr, id):
		self.id = id
		self.uuid = attr["uuid"]
		self.hostname = attr["hostname"]
		self.cpus = attr["core_number"]
		self.memory = attr["memory_amount"]
		self.state = attr["state"]

	def get(self):
		return self.id, self.hostname, self.cpus, self.memory, self.state
