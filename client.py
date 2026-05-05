# Imports go at the top
from microbit import *
import radio
radio.on()
radio.config(group=36)

class Server():
    def __init__(self):
        self.quorum_conf_is_finished = False
        self.voti_si = 0
        self.voti_no = 0
        self.voti_tot = 0
        self.binario = ""
        self.quorum = 0

    
 
      
    def on_button_pressed_a(self):

        if not self.quorum_conf_is_finished:
            # se è gia stato scelto il ruolo del bot adesso si passa alla conf. del quoru
            self.binario = "" + self.binario + "1"
            print(self.binario)
        elif self.quorum_conf_is_finished:
            # se è gia stato conf. tutto fa partire il permess
            # parte la votazione
            radio.send("1")
    def on_button_pressed_b(self):

        if not self.quorum_conf_is_finished:
            self.binario = "" + self.binario + "0"
            print(self.binario)
            
    def on_button_pressed_ab(self):

        if not self.quorum_conf_is_finished:
            self.quorum_conf_is_finished = True
            self.binario = self.binario[::-1]
            decimale = int(self.binario, 2)
            self.quorum = decimale
            print(self.quorum)
    def config_quorum(self):
       
        if button_a.was_pressed():
            self.on_button_pressed_a()
        elif button_b.was_pressed():
            self.on_button_pressed_b()
       
        elif button_a.is_pressed() and button_b.is_pressed():
            self.on_button_pressed_ab()

    def reciev_vote(self):
        message = radio.receive()
        if message == 's':
            self.voti_si += 1
            self.voti_tot += 1
        elif message == 'n':
            self.voti_no += 1
            self.voti_tot += 1
        sleep(100)#così controlla ogni 100milliscecondi, 10 volte al secondo
class Client():
    def __init__(self):
        self.has_voted = False
    def vote_yes(self):
        if not self.has_voted:
            radio.send("s")# si

    def vote_no(self):
        if not self.has_voted:
            radio.send("n")# no

class Main():
    def __init__(self):
        self.is_configured = False
        self.is_server = False
        self.is_client = False
        self.microbit = 0
        
    def config(self):
        if not self.is_configured:
            if button_a.was_pressed(): #client
                self.is_client = True
                self.microbit = Client()
            elif button_b.was_pressed():
                self.is_server = True
                self.microbit = Server()
            self.is_configured = True
            
    def run(self):
        self.config()

        while 1:
            pass



