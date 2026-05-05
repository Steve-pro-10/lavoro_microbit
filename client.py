# Imports go at the top
from microbit import *
import radio, music

radio.on()
radio.config(group=36)

class Server():
    def __init__(self):
        self.quorum_conf_is_finished = False
        self.is_recieving_votes = False
        self.voti_si = 0
        self.voti_no = 0
        self.voti_tot = 0
        self.binario = ""
        self.quorum = 0

    def on_button_pressed_a(self):

        if not self.quorum_conf_is_finished:
            # se è gia stato scelto il ruolo del bot adesso si passa alla conf. del quoru
            self.binario = "" + self.binario + "1"
            display.show("1")
            print(self.binario)
    def on_button_pressed_b(self):
        if not self.quorum_conf_is_finished:
            self.binario = "" + self.binario + "0"
            display.show("0")
            print(self.binario)
            
    def on_button_pressed_ab(self):
        
        if not self.quorum_conf_is_finished:
            self.quorum_conf_is_finished = True
            decimale = int(self.binario, 2)
            self.quorum = decimale
            print(self.quorum)
    def config_quorum(self):
        display.show("configura")
        while not self.quorum_conf_is_finished:
            if button_a.is_pressed() and button_b.is_pressed():
                self.on_button_pressed_ab()
            elif button_a.was_pressed():
                self.on_button_pressed_a()
            elif button_b.was_pressed():
                self.on_button_pressed_b()
        
            sleep(50)  # piccola pausa per evitare busy loop
            
    def recive_vote(self):
        if self.quorum_conf_is_finished:
            
        # se è gia stato conf. tutto fa partire il permess
        # parte la votazione
            display.show("premi A per iniziare")
            while not self.is_recieving_votes:
                if button_a.is_pressed() and button_b.is_pressed():
                    self.is_recieving_votes = True
            radio.send("1")
            display.show("voto iniziato")

            while self.is_recieving_votes:
                message = radio.receive()
    
                if message == 's':
                    self.voti_si += 1
                    self.voti_tot += 1
                elif message == 'n':
                    self.voti_no += 1
                    self.voti_tot += 1
                if button_b.is_pressed() and button_a.is_pressed():
                    self.is_recieving_votes = False
                   
                sleep(100)#così controlla ogni 100milliscecondi, 10 volte al secondo

    def run(self):
        self.config_quorum()
        self.recive_vote()


class Client():
    def __init__(self):
        self.has_voted = False
        self.has_perm_to_vote = False
        
    def wait_for_perm_to_vote(self):
        message = radio.receive()
        if message == '1':
            self.has_perm_to_vote = True
    def vote_yes(self):
        if not self.has_voted and self.has_perm_to_vote:
            radio.send("s")# si

    def vote_no(self):
        if not self.has_voted and self.has_perm_to_vote:
            radio.send("n")# no
    def vote(self):
        if button_a.was_pressed():
            self.vote_yes()
        elif button_b.was_pressed():
            self.vote_no()
    def run(self):
        self.wait_for_perm_to_vote()
        self.vote()
        radio.off()#esce dalla radio

class Main():
    def __init__(self):
        self.is_configured = False
        self.is_server = False
        self.is_client = False
        self.microbit = None 

        
    def config(self):
        while not self.is_configured:
            if button_a.was_pressed(): #client
                self.is_client = True
                self.microbit = Client()
                display.show("client")
                self.is_configured = True
            elif button_b.was_pressed():
                self.is_server = True
                self.microbit = Server()
                display.show("server")
                self.is_configured = True
            
    def run(self):
        display.show("scegli")
        self.config()
        
        while 1:
            self.microbit.run()
app = Main()
app.run()
radio.off()
