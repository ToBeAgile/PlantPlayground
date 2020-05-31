from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio

"""
def filter_handler(address, *args):
    print(f"{address}: {args}")
    
dispatcher = Dispatcher()
dispatcher.map("/filter", filter_handler)
"""
def raw_handler(address, *args):
    print(f"{address}: {args}")

def sec_handler(address, *args):
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


async def loop():
    """Example main loop that only runs for 10 iterations before finishing"""
    for i in range(10):
        print(f"Loop {i}")
        await asyncio.sleep(1)


async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())