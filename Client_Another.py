# socket �� select ��� ����Ʈ
from socket import *
from select import select
import sys

# ȣ��Ʈ, ��Ʈ�� ���ۻ���� ����
HOST = "127.0.0.1"
PORT = 56789
BUFSIZE = 1024
ADDR = (HOST, PORT)

#���� ��ü ����
clientSocket = socket(AF_INET, SOCK_STREAM)

#���� ���� �õ�
try:
    clientSocket.connect(ADDR)
except Exception as e:
    print('Can not connect to Server (%s:%s)' % ADDR)
    sys.exit()
print('Connecetd to Server (%s:%s)' % ADDR)

#����� ���� ���
def prompt():
    sys.stdout.write('<User>')
    sys.stdout.flush()
    
#���� ����
    while True:
        try:
            connection_list = [sys.stdin, clientSocket]

            read_socket, write_socket, error_socket = select(connection_list, [], [], 10)

            for sock in read_socket:
                #Ŭ���̾�Ʈ ���ϰ� ������ ��ġ�Ұ��, �����͸� �Է�
                if sock == clientSocket:   
                    data = sock.recv(BUFSIZE)
                    #�����͸� ������ �������, ����������� �˸��� ���α׷� ����
                    if not data:
                        print('Disconnected from Server (%s:%s)' % ADDR)
                        clientSocket.close()
                        sys.exit()
                    #�����͸� �޴°��, �����͸� �Է��ϵ��� ��   
                    else:
                        print('%s' % data)
                        prompt()
                #Ŭ���̾�Ʈ ���ϰ� ������ �ٸ����, �����͸� ����       
                else:
                    message = sys.stdin.readline()
                    clientSocket.send(message)
                    prompt()
        #���α׷� ����
        except KeyboardInterrupt:
            clientSocket.close()
            sys.exit()
            
                        
    
