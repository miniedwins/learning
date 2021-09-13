import socket

address = ('127.0.0.1', 8888)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)
server.listen(5)

print('*** START ECHO SERVER ***')
while True:

    print("WAIT FOR A CONNECTION ...")
    conn, addr = server.accept()
    print('CLIENT ADDRESS:', addr)

    while True:
        try:
            if not (msg := conn.recv(1024).decode('utf-8')):
                print("CLIENT CLOSE !!!")
                conn.close()
                break
            print(f"RECIVER MESSAGE: {msg}")
            conn.send(msg.encode('utf-8'))
        except Exception as err:
            print(err)
            break