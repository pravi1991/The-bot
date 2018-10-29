import socket
import sys


# create socket
def socket_create():
    try:
        global host
        global port
        global s

        host = ''
        port = 6666
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    except socket.error as msg:
        print(f"Socket creation failed: {msg}")


# bind the socket to the port
def socket_bind():
    try:
        global host
        global port
        global s
        print(f"Binding socket to the {port}")
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print(f"Socket binding failed: {msg}, Retrying...")
        socket_bind()


# establish a connection
def socket_accept():
    conn, address = s.accept()
    print(conn)
    print(address)
    print(f'Connection established | IP: {address[0]} | Port: {address[1]} ')
    send_commands(conn)
    conn.close()


# send commands to the client
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.send(str.encode(cmd))
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), 'utf-8')
            print(client_response, end='')


def main():
    socket_create()
    socket_bind()
    socket_accept()


main()
