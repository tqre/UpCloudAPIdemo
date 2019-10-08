import json


class Storagelist:

	def __init__(self,data):
		self.__dict__ = json.loads(data)
		self.storagelist, nr = [], 0
		for entry in self.__dict__['storages']['storage']:
			self.storagelist.append(Storage(entry, nr))
			nr += 1

	def getdetails(self, api, serverlist):
		for storage in self.storagelist:
			uuid = storage.uuid
			details = api.do("GET", "/storage/" + uuid)
			detailsjson = json.loads(details)
			for serveruuid in detailsjson['storage']['servers']['server']:
				storage.putdetails(serveruuid, serverlist)

	def show(self):
		data = []
		for storage in self.storagelist:
			data.append(storage.get())
		template = "{0:3}| {1:35}|{2:8}|{3:12}|{4:20}"
		print(template.format("#ID", "Storage description", "Size(GB)", "State", "Server"))
		for i in data:
			print(template.format(*i))

	def getstoragebyid(self,nr):
		return self.storagelist[nr].uuid


class Storage:

	def __init__(self, attr, id):
		self.id = id
		self.uuid = attr["uuid"]
		self.title = attr["title"]
		self.size = attr["size"]
		self.state = attr["state"]
		self.access = attr["access"]
		self.serveruuid = ""
		self.servername = ""

	def putdetails(self, serveruuid, serverlist):
		self.serveruuid = serveruuid
		# get name by uuid from servers class
		self.servername = serverlist.getserverhostnamebyuuid(serveruuid)

	def get(self):
		return self.id, self.title, self.size, self.state, self.servername
