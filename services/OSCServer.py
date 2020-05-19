from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


def raw_handler(address, *args):
    print(f"{address}: {args}")


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")


dispatcher = Dispatcher()
dispatcher.map("/PP01/ADC0/RAW/", raw_handler)
dispatcher.set_default_handler(default_handler)

#ip = "127.0.0.1"
ip = ""
#ip = "192.168.0.36"
port = 50000

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever