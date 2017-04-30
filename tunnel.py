import socket

TCP_IP = '107.170.224.107'
TCP_PORT_pi = 443
TCP_PORT_lambda = 3678
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

# Have Microwave Connect First
socket_pi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_pi.bind((TCP_IP, TCP_PORT_pi))
print("Waiting for PI to connect")
socket_pi.listen(1)
conn_pi, addr_pi = socket_pi.accept()

# Create Lamda Socket   
socket_lambda = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_lambda.bind((TCP_IP, TCP_PORT_lambda))

print 'Connection address:', addr_pi
while 1:
    # Listen For Lambda Connections
    socket_lambda.listen(1)
    conn_lambda, addr_lambda = socket_lambda.accept()
    data = conn_lambda.recv(BUFFER_SIZE)
    print "received data:", data
    conn_lambda.close()
    conn_pi.send(data)  # echo
conn_pi.close()
