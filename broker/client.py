import socket
import sys
import os

def reader(sock):
    data = sock.recv(1024)
    if debug:
        data_out = data.decode("utf-8")
        print(f"received: {data_out}")
    return data

def sender(sock, message):
    print(f"sending: {message}")
    sock.send(message.encode())

def actions(sock, message):
    message = str(message)
    sender(sock,message)
    data = reader(sock)
    return data

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

debug = False

# Connect the socket to the port where the server is listening
try:
    server_address = ('localhost', 10000)
    sock.connect(server_address)
except:
    server_address = ('localhost', 10001)
    sock.connect(server_address)
print('connecting to {} port {}'.format(*server_address))

try:
    # Data
    message = {
        "host": "mysql.localhost",
        "action": "check"
    }

    data = actions(sock, message)

    # Check
    if data.decode('utf-8') == "200": # action
        print("code: 200")
        message['action'] = "route"
        # Route
        data = actions(sock, message)
        if data.decode('utf-8') == "200":
            print(f"code: {data.decode('utf-8')}")
            os.system("mycli -h localhost -u root -P 10000")
    else:
        print("trace: not found host")

except KeyboardInterrupt:
    print("\nCtrl C - Stopping client")
    sys.exit(1)

finally:
    print('closing socket')
    sock.close()