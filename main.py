import logging
from llpserver.llp_server import LLPServer

# Setup Logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

server = LLPServer()
with server:
    server.listen_for_traffic()
