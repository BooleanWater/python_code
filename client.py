import socket
s=socket.socket()
host='127.0.0.1'
port=8080
s.connect((host,port))
while True:
    send_data=input("请输入要发送的数据： ")
    s.send(send_data.encode())
    recvData=s.recv(1024).decode()
    print('接收到的数据为： ',recvData)
#s.close()