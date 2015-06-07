# socket 과 select 모듈 임포트
from socket import *
from select import *
import sys
from time import ctime

 
# 호스트, 포트와 버퍼 사이즈를 지정
HOST = ''
PORT = 56789
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 소켓 객체생성
serverSocket = socket(AF_INET, SOCK_STREAM)

# 서버 정보를 바인딩
serverSocket.bind(ADDR)

# 요청을 기다림(listen)
serverSocket.listen(10)
connection_list = [serverSocket]
print('==============================================')
print('Start Server. Waitin connection to %s port....' % str(PORT))
print('==============================================')

# 무한 루프를 시작
while connection_list:
    try:
        print('Waiting Request...')

        # select 로 요청을 받고, 10초마다 블럭킹을 해제하도록 함
        read_socket, write_socket, error_socket = select(connection_list, [], [], 10)
        for sock in read_socket:
            # 새로운 접속
            if sock == serverSocket:
                clientSocket, addr_info = serverSocket.accept()
                connection_list.append(clientSocket)
                print('[!] [%s] Client (%s) has connected.' % (ctime(), addr_info[0]))
                # 클라이언트로 응답을 돌려줌
                for socket_in_list in connection_list:
                    if socket_in_list != serverSocket and socket_in_list != sock:
                        try:
                            socket_in_list.send('[%s] Client has connected to room' % ctime())
                        except Exception as e:
                            socket_in_list.close()
                            connection_list.remove(socket_in_list)
            # 접속한 사용자(클라이언트)로부터 새로운 데이터 받음
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

        # 종료하기
        serverSocket.close()
        sys.exit()

                                      
                
