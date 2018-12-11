import os
import socket
import threading
import time
event=threading.Event()
def send():
    while True:
        s_msg=input("\nServer-->")
        client.send(s_msg.encode())


def rec():
    while True:
        c_msg=client.recv(1024)
        if c_msg==('SFN'.encode()):
            print("Press Enter to Continue....")
            t3=threading.Thread(target=recFile)
            t3.start()
            t3.join()
        if c_msg.decode()=='FILE':
            t2=threading.Thread(target=sendFile)
            t2.start()
            t2.join()
        if c_msg.decode().lower().strip()=='bye':
            print("Connection Closed By Client, Said Bye")
            client.close()
            server.close()
            break
        print("\nClient-->",c_msg.decode())
        print("\nServer-->")

def sendFile():
    client.send("SFN".encode())
    fc_msg=client.recv(1024)
    f=fc_msg.decode()
    c,k=0,0
    wd=os.getcwd()
    l=os.listdir(wd)
    c=l.count(f)
    if c:
        client.send('Found'.encode())
        time.sleep(2)
        i=l.index(f)
        k=os.listdir(wd)[i]
        fp=open(k,'rb')
        while True:
            for line in fp:
                client.send(line)
            client.send('EOF'.encode())
            fp.close()
            break
            
    else:
        client.send('Not Found'.encode())
     
def recFile():
    f_msg=input("Enter the file name that you want with extension")
    client.send(f_msg.encode())
    f_msg=client.recv(1024)
    if f_msg==('Found'.encode()):
        print(f_msg)
        fname="new.jpg"
        f=open(fname,'wb')
        while True:
            f_cont=client.recv(1024)
            if f_cont==('EOF'.encode()):
                f.close()
                print("File added to the system,You can continue to chat")
                break
            f.write(f_cont)
    elif f_msg==('Not Found'.encode()):
        print("File Not Found,Chatting Continued")
            
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostbyname(socket.gethostname())
port=12345
server.bind((host,port))
print("\nServer is Waiting for Connection\n")
server.listen()
client,addr=server.accept()
print("\nServer is connected with IP{}\n".format(*addr))
print("\nIf you want to receive a file then type FILE ")
t=threading.Thread(target=send)
t1=threading.Thread(target=rec)
t2=threading.Thread(target=sendFile)
t3=threading.Thread(target=recFile)
t.start()
t1.start()
t.join()
t1.join()
print("Thank you for using our services")
server.close()
client.close()
exit()
