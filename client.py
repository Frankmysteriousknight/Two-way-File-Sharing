import os
import time
import socket
import threading
def send():
    while True:
        c_msg=input("\nClient-->")
        server.send(c_msg.encode())

def rec():
    while True:
        s_msg=server.recv(1024)
        if s_msg==('SFN'.encode()):
            print("Press Enter to continue....")
            t2=threading.Thread(target=recFile)
            t2.start()
            t2.join()
        if s_msg.decode()=='FILE':
            t3=threading.Thread(target=sendFile)
            t3.start()
            t3.join()
        if s_msg.decode().lower().strip()=='bye':
            server.close()
            print("Connection Closed By Server,Said Bye")
            break
        print("\nServer-->",s_msg.decode())
        print("\nClient-->")


def sendFile():
    server.send("SFN".encode())
    fc_msg=server.recv(1024)
    f=fc_msg.decode()
    c,k=0,0
    wd=os.getcwd()
    l=os.listdir(wd)
    c=l.count(f)
    if c:
        server.send('Found'.encode())
        time.sleep(2)
        i=l.index(f)
        k=os.listdir(wd)[i]
        fp=open(k,'rb')
        while True:
            for line in fp:
                server.send(line)
            server.send('EOF'.encode())
            fp.close()
            break
    else:
        server.send('Not Found'.encode())
     
     
def recFile():
    f_msg=input("Enter the file name that you want with extension")
    server.send(f_msg.encode())
    f_msg=server.recv(1024)
    
    if (f_msg.decode())=='Found':
        print(f_msg)
        fname="cloud22.jpg"
        f=open(fname,'wb')
        while True:
            f_cont=server.recv(1024)
            if f_cont==('EOF'.encode()):
                f.close()
                print("File added to the system")
                break
            f.write(f_cont)
    elif f_msg==('Not Found'.encode()):
        print("File Not Found,Chatting Continued")

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostbyname(socket.gethostname())
port=12345
server.connect((host,port))
print("\nIf you want to receive a file then type FILE")
t=threading.Thread(target=send)
t1=threading.Thread(target=rec)
t2=threading.Thread(target=recFile)
t3=threading.Thread(target=sendFile)
t.start()
t1.start()
t.join()
t1.join()
server.close()
print("Thank you for using our services")
                
