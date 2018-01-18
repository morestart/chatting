import socket
import threading

sock_list = []


def tcplink(sock, addr):
    print('Accept new connection from %s:%s' % addr)
    welcom = "欢迎来到3406聊天室!"
    sock.send(welcom.encode("utf-8"))

    while True:
        try:
            data = sock.recv(1024)
            if not data or data.decode('utf-8') == 'exit':
                break
            print(data.decode("utf-8"))
            # print(sock_list)
            for users in sock_list:
                users.send(data)

        except:
            try:
                sock_list.remove(sock)
                # print(sock_list)
            except:
                pass

    sock.close()
    print('Connection from %s:%s closed.' % addr)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 9999))
s.listen()
print('Waiting for connection...')
while True:
    # 接受一个新连接:
    sock, addr = s.accept()

    sock_list.append(sock)
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
