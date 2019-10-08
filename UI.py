def welcome():
	print('''
	UpCloud API Python DEMO 						(c)tqre 2019
	1 - get details from servers
	2 - DEMO - create Debian 10 server
	3 - delete a server
	4 - stop a server
	5 - storage options
	6 - DEMO - create storage 10GB disk
	? - list commands
	0 - exit program	
	''')


def server_details():
	cmd = input("Enter number to get details:")
	return cmd


def server_delete():
	cmd = input("Enter server ID number which is to be deleted:")
	print("Server " + cmd + " is going to be deleted!")
	verify = input("Are you sure? (y/n) ")
	if verify == "y":
		return cmd
	else:
		return "ERROR"


def server_stop():
	cmd = input("Enter server ID to stop:")
	return cmd


def storage_options():
	print('''
	Storage options:
	1 - delete a storage
	2 - attach a storage to a server (NOT IMPLEMENTED)
	3 - remove storage from a server (NOT IMPLEMENTED)
	''')
	cmd = input("Storage options:")
	return cmd
