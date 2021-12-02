from kivy.lang import Builder

from kivymd.app import MDApp

import socket
import json
from time import sleep

# =======GLOBALS=========
host = '192.168.0.196'  # IP Adresse des Servers
pins = []


# =========SETUP==========
class Pin:
    def __init__(self, pin_number, pin_state=0):
        self.id = pin_number
        self.state = pin_state


# =======SOCKET FUNCTIONS=======
def get_current():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((host, 80))
        current = json.loads(server.recv(1024).decode("utf-8"))
    for key in current.keys():
        pins.append(Pin(int(key), current[key]))
    sleep(0.5)
    return pins


def send_changes(pin):
    dic = {
        "pin": pin.id,
        "state": pin.state
    }
    data = json.dumps(dic)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, 80))
        s.sendall(bytes(data, encoding="utf-8"))
    sleep(0.5)


# =========KIVY==========
KV = '''
MDScreen:

    MDIconButton:
        icon: "power"
        user_font_size: "64sp"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        on_press: app.switch()
'''


class Ljos(MDApp):
    def switch(self):
        p = pins[0]
        if p.state == 0:
            p.state = 1
        elif p.state == 1:
            p.state = 0
        send_changes(p)


    def build(self):
        get_current()
        return Builder.load_string(KV)


if __name__ == '__main__':
    Ljos().run()

