import socket
import json

# =======GLOBALS=========
host = '192.168.0.196'  # IP Adresse des Servers
pins = []


# =========SETUP==========
class Pin:
    def __init__(self, pin_number, pin_state=0):
        self.id = pin_number
        self.state = pin_state


def get_current():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((host, 80))
        current = json.loads(server.recv(1024).decode("utf-8"))

    for key in current.keys():
        pins.append(Pin(int(key), current[key]))
    return pins


def send_changes():
    dic = {
        "pin": pins[0].id,
        "state": pins[0].state
    }
    data = json.dumps(dic)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, 80))
        s.sendall(bytes(data, encoding="utf-8"))

