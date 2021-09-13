import socket

buffer_size=1024
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8888))

while True:
    if not (msg := input("$: ")):
        continue
    elif msg == 'q':
        client.close()
        break
    else:
        client.send(msg.encode('utf-8'))
        print(client.recv(1024).decode('utf-8'))
