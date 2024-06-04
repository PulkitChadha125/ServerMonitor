import pickle
from CheckServer import Server
servers = pickle.load( open( "servers.pickle", "rb" ) )
print("Example to add server")
servername = input("enter server name: ")
port = int(input("Enter a port number as integer (set 80 if you dont know): "))
connection = input("Enter a type ping/plain/ssl (set ping if you dont know): ")
priority = input("Enter priority high/low: ")
new_server = Server(servername, port, connection, priority)
servers.append(new_server)
pickle.dump(servers, open("servers.pickle", "wb" ))