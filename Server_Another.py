# socket �� select ��� ����Ʈ
from socket import *
from select import *
import sys
from time import ctime

 
# ȣ��Ʈ, ��Ʈ�� ���� ����� ����
HOST = ''
PORT = 56789
BUFSIZE = 1024
ADDR = (HOST, PORT)

# ���� ��ü����
serverSocket = socket(AF_INET, SOCK_STREAM)

# ���� ������ ���ε�
serverSocket.bind(ADDR)

# ��û�� ��ٸ�(listen)
serverSocket.listen(10)
connection_list = [serverSocket]
print('==============================================')
print('Start Server. Waitin connection to %s port....' % str(PORT))
print('==============================================')

# ���� ������ ����
while connection_list:
    try:
        print('Waiting Request...')

        # select �� ��û�� �ް�, 10�ʸ��� ��ŷ�� �����ϵ��� ��
        read_socket, write_socket, error_socket = select(connection_list, [], [], 10)
        for sock in read_socket:
            # ���ο� ����
            if sock == serverSocket:
                clientSocket, addr_info = serverSocket.accept()
                connection_list.append(clientSocket)
                print('[!] [%s] Client (%s) has connected.' % (ctime(), addr_info[0]))
                # Ŭ���̾�Ʈ�� ������ ������
                for socket_in_list in connection_list:
                    if socket_in_list != serverSocket and socket_in_list != sock:
                        try:
                            socket_in_list.send('[%s] Client has connected to room' % ctime())
                        except Exception as e:
                            socket_in_list.close()
                            connection_list.remove(socket_in_list)
            # ������ �����(Ŭ���̾�Ʈ)�κ��� ���ο� ������ ����
            else:
                data = sock.recv(BUFSIZE)
                if data:
                    print('[%s] Got data from Client...' % ctime())
                    for socket_in_list in connection_list:
                        if socket_in_list != serverSocket and socket_in_list != sock:
                            try:
                                socket_in_list.send('[%s] %s' % (ctime(), data))
                                print('[%s] Sending data to Client...' % ctime())
                            except Exception as e:
                                print(e.message)
                                socket_in_list.close()
                                connection_list.remove(socket_in_list)
                                continue
                else:
                    connection_list.remove(sock)
                    sock.close()
                    print('[!][%s] Disconnected...' % ctime())
    except KeyboardInterrupt:

        # �����ϱ�
        serverSocket.close()
        sys.exit()

                                      
                
