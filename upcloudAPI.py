import http.client
import UI
from servers import Serverlist
from storages import Storagelist
from base64 import b64encode
from getpass import getpass


class APIconnection:

	def __init__(self):
		self.address = "api.upcloud.com"
		self.version = "/1.2"
		print("Connecting to " + self.address)
		username = input("Username:")
		pswd = getpass("Password:")
		self.credentials = b64encode((username + ":" + pswd).encode())

	def conn(self, httpreq, url, body=None):
		connection = http.client.HTTPSConnection(self.address)
		url = self.version + url
		headers = {"Authorization": "Basic " + self.credentials.decode(),
				   "Content-Type": "application/json"}
		connection.request(httpreq, url, body, headers)
		# this object returns http status codes with .status method
		return connection.getresponse()

	def test_credentials(self):
		if self.conn("GET", "/account").status == 401:
			print("Authentication failed, exiting...")
			exit()

	def do(self, httpreq, url, body=None):
		return self.conn(httpreq, url, body).read().decode(encoding="UTF-8")


def main():
	api = APIconnection()
	api.test_credentials()
	while True:
		serverdata = api.do("GET", "/server")
		serverlist = Serverlist(serverdata)
		storagedata = api.do("GET", "/storage/private")
		storagelist = Storagelist(storagedata)
		storagelist.getdetails(api, serverlist)
		UI.welcome()
		cmd = input("What do you want to do? ")

		if cmd == "1":
			serverlist.show()
			srvcmd = UI.server_details()
			try:
				serveruuid = serverlist.getserverbyid(int(srvcmd))
				print(api.do("GET", "/server/" + serveruuid))
			except:
				print("Returning... (also in case of wrong ID)")
				continue

		if cmd == "2":
			templatefile = open("debian10.json", "r")
			print(api.do("POST", "/server", templatefile))
			templatefile.close()

		if cmd == "3":
			serverlist.show()
			srvcmd = UI.server_delete()
			try:
				serveruuid = serverlist.getserverbyid(int(srvcmd))
				print(api.do("DELETE", "/server/" + serveruuid + "/?storages=1"))
			except:
				print("Nothing happened, fortunately :)")
				continue

		if cmd == "4":
			serverlist.show()
			srvcmd = UI.server_stop()
			try:
				serveruuid = serverlist.getserverbyid(int(srvcmd))
				print(api.do("POST", "/server/" + serveruuid + "/stop"))
			except:
				print("Something went wrong...")
				continue

		if cmd == "5":
			storagelist.show()
			stocmd = UI.storage_options()
			if stocmd == "1":
				storageid = input("Enter storage number to be deleted: ")
				storageuuid = storagelist.getstoragebyid(int(storageid))
				print(storageuuid)
				areyousure = input("Storage " + storageid + " is going to be DELETED, sure about that?")
				if areyousure == "y":
					print(api.do("DELETE","/storage/" + storageuuid))
				continue
			if stocmd == "2":
				#attach a storage to a server
				#need to generate json for the storage in question
				#POST server/<serveruuid>/storage/attach
				#json stuff in httprequest body
				serverlist.show()
				pass
			if stocmd == "3":
				#detach a storage
				#POST server/<serveruuid>/storage/detach
				#body: json format needs storage address on the server (virtio:[0-7])
				#that data has to be gathered too from server infos:
				#server details: [server][storage_devices][storage_device][#number][address]
				#for first added storage, it is usually virtio:1
				#via web UI, the storages can't be added on the fly, via API
				#it is possible for virtio devices
				pass

		if cmd == "6":
			templatefile = open("storagedemo.json", "r")
			print(api.do("POST", "/storage", templatefile))
			templatefile.close()

		if cmd == "?":
			UI.welcome()
			continue
		if cmd == "0":
			exit()




if __name__ == "__main__":
	main()

