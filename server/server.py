import socket
import _thread
import sys


class Server:


    """start server(done), 
        multi p -- accept client connection(done), 
        
        1.send success to cli(done), 
    
        2.'recv from cli'
        -name(done)
        loop
        -client can enter room
        -snd message to room
        -leveve room
        """


    def __init__(self):

        #settings
        self.port = 3389
        self.host = ''
        self.server_addr = (self.host, self.port)

        #socket
        self.sock = None

        #threading
        self.thread_count = 0

        #room
        self.rooms = {} #{room_id:{c_name:c_socket}}


    def server_run(self):
        self.server_socket_handle()
        try:
            self.client_handle()
        except KeyboardInterrupt:
            self.sock.close()
            print("--server closed--")
            sys.exit()

    #------------------------------------------------------------------------------client_handle
    def client_handle(self):
        """handles client connention and process init"""
        while True:
            cli_socket = self._accept_client_connection()
            self._init_client_process(cli_socket)

            self.thread_count += 1
            print("client connected:", self.thread_count) 
    

    def cli_communication(self, cli_socket):
        #snd ,loop recv
        #send connection success to cli
        #msg = "--> Connected to Server <--"
        #self._send_data(cli_socket, 99, msg)

        #get cli name
        cli_name = self._get_client_name(cli_socket)
        room_number = 0 #default room
        in_connection = True
        while in_connection:
            req_code, data = self._get_data(cli_socket)
            
            if req_code == 101:
                #data = room_id
                room_number = data
                if room_number in self.rooms:
                    self.rooms[room_number][cli_name] = cli_socket
                else:
                    self.rooms[room_number] = {cli_name: cli_socket}
                #print(self.rooms)
                self._send_data_to_all_room_members(room_number, cli_name, " \.Joined the room./ ")

            if req_code == 401:
                #data = chat_sent
                self._send_data_to_all_room_members(room_number, cli_name, data)
            
            if req_code == 102:
                #exit room
                del self.rooms[room_number][cli_name]
                self._send_data_to_all_room_members(room_number, cli_name, " \.exited the room./ ")
            
            if req_code == 5001:
                in_connection = False
                self.thread_count -= 1
                print("client connected:", self.thread_count)
        
    
    def _send_data_to_all_room_members(self,room_number, cli_name, data):
        """send msg to all members of the room"""
        for member in self.rooms[room_number]:
            m_data = f"{cli_name.title()}: {data}"
            if member == cli_name:
                continue
                #m_data = f" You : {data}"
            self._send_data(self.rooms[room_number][member], 400, data=m_data)

    def _get_client_name(self, cli_socket):
        req_code, cli_name = self._get_data(cli_socket) #data = name, req_code = 100
        return cli_name


    def _send_data(self, cli_socket, req_code, data):
        """send encoded data via socket with req_code linked"""
        d = str(req_code)+"#@#"+data
        try:
            cli_socket.sendall(d.encode())
        except:
            pass

    def _get_data(self, cli_socket):
        """recv decoded req_code and data via socket """
        d = cli_socket.recv(2048).decode()
        req_code, data = d.split('#@#')
        return int(req_code), data


    def _init_client_process(self, cli_socket):
        """starts new client process thread"""
        _thread.start_new_thread(self.cli_communication, (cli_socket, ))
        
    def _accept_client_connection(self):
        """accepts client connection"""
        cli_socket, cli_addr = self.sock.accept()
        return cli_socket

   
   #---------------------------------------------------------------------server_socket_handler
    def server_socket_handle(self):
        """handles the server socket (create-->bind-->listen)"""
        #create, bind , listen, accept, recv/snd
        self._create_socket()
        self._bind_socket_to_addr()
        self._listen(5)

    def _create_socket(self):
        """creates a tCP socket with ipv4 as addr family"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("SERVER INITIATED")
    
    def _bind_socket_to_addr(self):
        """associate the socket to server addr to use it as server"""
        self.sock.bind(self.server_addr)

    def _listen(self, backlog):
        """put the socket into server mode"""
        #backlog - number of allowed requests from client in queue
        self.sock.listen(backlog)

s = Server()
s.server_run()