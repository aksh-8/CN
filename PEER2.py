import os
import socket
import time
from tkinter import *
from tkinter import filedialog
# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = '0.0.0.0'
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)
    
    except socket.error as msg:
        print("Socket Binding error" + str(msg)+ '\n' + "Retrying...")
        bind_socket()

# Establish connection with a client (socket must be listening)
def socket_accept():
    conn, address  = s.accept()
    print("Connection has been established! |" + " IP " + address[0] + " | Port " + str(address[1]))
    send_file(conn)
    conn.close()


# Read file as bytes and send
def send_file(conn):
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir="/home/amit/Desktop/CN", title="Select file", filetypes=(("png files", "*.png"),("all files", "*.*")))
    #print(root.filename)
    filename = os.path.split(root.filename)[1]
    f = open(filename,'rb')
    filesize = os.stat(filename).st_size
    print("filesize in bytes",filesize)
    #print(f)
    start_time = time.time()
    f_data = f.read(1024)
    conn.send(filename.encode())
    while (f_data):
        conn.send(f_data)
        f_data = f.read(1024)
    f.close()
    print('Sent file')
    end_time = time.time()
    elapsed_time = end_time-start_time
    #print('Sent File')
    print("Transfer time = ",'%.2f'%elapsed_time+'sec')
    transfer_rate = filesize/elapsed_time
    transfer_rate_b = transfer_rate*8
    transfer_rate_Mb = transfer_rate_b/1000000
    print("Transfer rate = ",'%.2f'%transfer_rate_Mb+'Mbps')


# Establish connection with a server and receive file 
def connect_socket():
    s = socket.socket()
    s.connect(('192.168.1.7', 9999))
    # Accept file
    #def recv_file():
    temp = s.recv(1024)
    filename = temp.decode()
    f = open(filename,'wb')
    f_data = s.recv(1024)
    while(f_data):
        f.write(f_data)
        f_data = s.recv(1024)
    f.close()
    print('Recieved Data')
    
#initiate file sending process
def sendmode():
        create_socket()
        bind_socket()
        socket_accept()
        exit()

#$initiate file receiving process
def recvmode():
        connect_socket()
        exit()


# MAIN
def main():

    root = Tk()
    print('searching for peers')
    root.geometry('350x150')
    root.title('CN Project')
    topframe = Frame(root)
    topframe.pack()
    midframe = Frame(root)
    midframe.pack()
    label = Label(topframe, text="P2P file sharing", font=("Times", 20) )
    label.pack()
    send_button = Button(midframe, text="Send File", fg="blue", command=sendmode)
    recv_button = Button(midframe, text="Recieve File", fg="blue", command=recvmode)
    send_button.grid(row=1, column=0, padx=10, pady=10)
    recv_button.grid(row=1, column=1, padx=10, pady=10)
    root.mainloop()
    
main()




