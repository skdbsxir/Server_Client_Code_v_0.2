# socket 과 select 모듈 임포트
from socket import *
from select import select
import sys

# 호스트, 포트와 버퍼사이즈를 지정
HOST = "127.0.0.1"
PORT = 56789
BUFSIZE = 1024
ADDR = (HOST, PORT)

#소켓 객체 생성
clientSocket = socket(AF_INET, SOCK_STREAM)

#소켓 연결 시도
try:
    clientSocket.connect(ADDR)
except Exception as e:
    print('Can not connect to Server (%s:%s)' % ADDR)
    sys.exit()
print('Connecetd to Server (%s:%s)' % ADDR)

#사용자 정보 출력
def prompt():
    sys.stdout.write('<User>')
    sys.stdout.flush()
    
#루프 시작
    while True:
        try:
            connection_list = [sys.stdin, clientSocket]

            read_socket, write_socket, error_socket = select(connection_list, [], [], 10)

            for sock in read_socket:
                #클라이언트 소켓과 소켓이 일치할경우, 데이터를 입력
                if sock == clientSocket:   
                    data = sock.recv(BUFSIZE)
                    #데이터를 받을수 없을경우, 연결종료됨을 알리고 프로그램 종료
                    if not data:
                        print('Disconnected from Server (%s:%s)' % ADDR)
                        clientSocket.close()
                        sys.exit()
                    #데이터를 받는경우, 데이터를 입력하도록 함   
                    else:
                        print('%s' % data)
                        prompt()
                #클라이언트 소켓과 소켓이 다를경우, 데이터를 받음       
                else:
                    message = sys.stdin.readline()
                    clientSocket.send(message)
                    prompt()
        #프로그램 종료
        except KeyboardInterrupt:
            clientSocket.close()
            sys.exit()
            
                        
    
