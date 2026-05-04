# Imports go at the top
from microbit import *
import radio
radio.on()
radio.config(group=36)
class Server():
    def __init__(self):
        self.quorum_conf_is_finished = False
        self.is_configured = False
        self.binario = ""
        self.quorum = 0

    def on_button_pressed_a(self):

        if self.is_configured and not self.quorum_conf_is_finished:
            # se è gia stato scelto il ruolo del bot adesso si passa alla conf. del quoru
            self.binario = "" + self.binario + "1"
            print(self.binario)
        elif self.is_configured and self.quorum_conf_is_finished and is_server:
            # se è gia stato conf. tutto fa partire il permess
            # parte la votazione
            radio.send("1")
    def on_button_pressed_b(self):

        if self.is_configured and not self.quorum_conf_is_finished:
            self.binario = "" + self.binario + "0"
            print(self.binario)
    def on_button_pressed_ab(self):

        if not self.quorum_conf_is_finished:
            self.quorum_conf_is_finished = True
            self.binario = self.binario[::-1]
            decimale = int(self.binario, 2)
            self.quorum = decimale
            print(self.quorum)
class Client():
    def __init__(self):
        self.has_voted = False
    def vote(self):
        
        
        

input.on_button_pressed(Button.A, on_button_pressed_a)


input.on_button_pressed(Button.AB, on_button_pressed_ab)


input.on_button_pressed(Button.B, on_button_pressed_b)



