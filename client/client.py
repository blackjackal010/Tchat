import socket
import _thread
import sys
import os
import time


class Client:

    def __init__(self):

        #serv addr
        self.host = 'localhost'
        self.port = 10000
        self.server_addr = (self.host, self.port)

        self.sock = None

        self.client_name = None
        self.room_number = None

        self.in_room = False

    def client_run(self):
        self._create_client_socket()
        self._client_connect_server()
        _thread.start_new_thread(self.listen_to_server, ())
        self.terminal_interact()


    def terminal_interact(self):
        self.show_startup()
        self.ask_user_name()
        self.option_page()

    def clear_all(self):
        if sys.platform == 'linux':
            os.system('clear')
        elif sys.platform == 'win32':
            os.system('cls')

    def show_terminal_bg(self):
        self.clear_all()
        print(" ")
        print(" "*10+"+---------------------+")
        print(" "*10+"|  ._.  ___           |")
        print(" "*10+"|  |*|   | CHAT ...   |")
        print(" "*10+"+---------------------+\n")    
        if self.client_name:
            print(f" Current User : {self.client_name}")
        print("\n")
    
    def show_startup(self):
        self.clear_all()
        print("\n \twelcome to TCHAT application ")
        time.sleep(1)
        print("\t         -live terminal based chat application\n")
        time.sleep(2)
        print("\t    -< credits: blackjackal010 >-   ")
        time.sleep(2)

    def ask_user_name(self):
        self.show_terminal_bg()
        while not self.client_name:
            self.client_name = input("Enter your user name: ")
        self.send_cli_name_to_server()

    def send_cli_name_to_server(self):
        self._send_data(self.sock, 100, self.client_name)
        

    def show_options(self):
        self.show_terminal_bg()
        print(" option [1] :  Create/Enter Room ")
        print(" option [2] :  help - see available cmd ")
        print(" option [3] :  Exit app")

    def choose_option(self):
        print("\n")
        option = input("Choose a option: ")
        if option == '1':
            self.chat_room_page()
        elif option == '2':
            self.help_page()
        elif option == '3':
            self._send_data(self.sock, 5001, 'exit')
            self.clear_all()
            sys.exit()
        else:
            self.option_page()

    def option_page(self):
        self.show_options()
        self.choose_option()

    def help_page(self):
        self.show_terminal_bg()
        print("Available cmd:\n")
        print(" ->type '@exit' in chat room - to exit a chat room")
        try:
            c = input("press enter")
        except:
            pass
        finally:
            self.option_page()

    def chat_room_page(self):

        self.show_terminal_bg()
        self.room_number = input("Enter room number: ")
        #snd room no. to server
        self._send_data(self.sock, 101, self.room_number)
        self.show_terminal_bg()
        print("Entering room......")
        time.sleep(1)
        self.room_page()

    def room_page(self):
        self.show_terminal_bg()
        print(f"  Entered Room : {self.room_number}")
        self.in_room = True
        while self.in_room:
            self.in_room = self.chat()
        print("\n-----room exiting-----")
        self.option_page()

    def chat(self):
        msg = input()
        if msg == '@exit':
            self._send_data(self.sock, 102, 'exit')
            return False
        self._send_data(self.sock, 401, msg)
        return True
        


    def _send_data(self, sock, req_code, data):
        """send encoded data via socket with req_code linked"""
        d = str(req_code)+"#@#"+str(data)
        try:
            sock.sendall(d.encode())
        except:
            pass


    def listen_to_server(self):
        while True:
            d = self.sock.recv(2048).decode()
            req_code, data = d.split('#@#')
            print(data)

    def _create_client_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _client_connect_server(self):
        self.sock.connect(self.server_addr)

c = Client()
c.client_run()