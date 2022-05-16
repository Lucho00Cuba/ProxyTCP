import socket
import ast
import sys
import select

class Proxy:

    def __init__(self, host, port):
        
        self.host = host
        self.port = port
        self.port_alt = 10001


    def stream(self):
        services = {
            "app-3.localhost" : ["localhost", "8081"],
            "app-4.localhost" : ["localhost", "8082"],
            "mysql.localhost": ["localhost", "3306"]
        }
        return services

    def main(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = self.sock
        # Bind the socket to the port
        try:
            server_address = (self.host, self.port)
            sock.bind(server_address)
            # Listen for incoming client_connections
            sock.listen(1)
        except OSError:
            server_address = (self.host, self.port_alt)
            sock.bind(server_address)
            # Listen for incoming client_connections
            sock.listen(1)
        print('Starting up on {} port {}'.format(*server_address))

        while True:
            # Wait for a client_connection
            print('waiting for a client_connection')
            client_connection, client_address = sock.accept()
            try:
                print('client_connection from', client_address)
                # Receive the data in small chunks and retransmit it
                while True:
                    data = client_connection.recv(1024)
                    dataFromClient = data.decode('utf-8')
                    print('received {!r}'.format(data))
                    services = self.stream()
                    if data:
                        dataFromClient = ast.literal_eval(dataFromClient)
                        # Check
                        if dataFromClient['action'] == "check":
                            if dataFromClient['host'] in services:
                                print('sending data back to the client')
                                message = "200"
                                client_connection.sendall(message.encode())
                            else:
                                print('sending data back to the client')
                                message = "400"
                                client_connection.sendall(message.encode())
                        # Route
                        elif dataFromClient['action'] == "route":
                            print(f"routing: alias -> {dataFromClient['host']} -> {services[dataFromClient['host']][0]}:{services[dataFromClient['host']][1]}")
                            message = f"200"
                            client_connection.sendall(message.encode())
                            #server_address = (services[dataFromClient['host']][0], int(services[dataFromClient['host']][1]))
                            self.remote_addr = services[dataFromClient['host']][0]
                            self.remote_addr = int(services[dataFromClient['host']][1])
                    else:
                        #print('no data from', client_address)
                        break
            finally:
                # Clean up the client_connection
                print(f"closing current client_connection {client_address[0]}:{client_address[1]}\n")
                client_connection.close()

if __name__ == '__main__':
        server = Proxy('localhost', 10000)
        try:
            server.main()
        except KeyboardInterrupt:
            print("Ctrl C - Stopping server")
            sys.exit(1)
