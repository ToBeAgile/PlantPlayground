import sys
sys.path.insert(1, "/Users/davidscottbernstein/Dropbox/Dev/Python/Projects/PlantPlayground")
from services.DataLogger import DataLogger
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

dl = DataLogger()

def raw_handler(address, *args):
    print(f"{address}: {args}")

def sec_handler(address, *args):
    dl.write(args)
    print(f"{address}: {args}")

def min_handler(address, *args):
    print(f"{address}: {args}")

def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")


dispatcher = Dispatcher()
dispatcher.map("/PP01/ADC0/RAW/", raw_handler)
dispatcher.map("/PP01/ADC1/RAW/", raw_handler)
dispatcher.map("/PP01/ADC0/SEC/", sec_handler)
dispatcher.map("/PP01/ADC1/SEC/", sec_handler)
dispatcher.map("/PP01/ADC0/MIN/", min_handler)
dispatcher.map("/PP01/ADC1/MIN/", min_handler)
dispatcher.set_default_handler(default_handler)

#ip = "127.0.0.1"
ip = ""
#ip = "192.168.0.36"
port = 50000

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever