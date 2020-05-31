from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import sys
sys.path.insert(1, '/Users/davidscottbernstein/Dropbox/Dev/Python/Projects/PlantPlayground')
from services.DataLogger import DataLogger

dl = DataLogger()

def raw_handler(address, *args):
    dummy = 0
    #print(f"{address}: {args}")

def sec_handler(address, *args):
    print(f"{address}: {args}")


def min_handler(address, *args):
    print(f"{address}: {args}")
    dl.write(address, args)

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

if __name__ == '__main__':
    # isDashInitialized = True
    # app.run_server() #debug enables reload by default. This means that every line is run again, resulting in reinitialization. This breaks sockets.
    app.run_server(debug=True, use_reloader=False)  # to debug and block reload
    # see https://stackoverflow.com/questions/9449101/how-to-stop-flask-from-initialising-twice-in-debug-mode for another option to block only certain things from being reinitialized

