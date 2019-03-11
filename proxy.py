"""A proxy server that forwards requests from one port to another server.

To run this using Python 2.7:

% python proxy.py

It listens on a port (`LISTENING_PORT`, below) and forwards commands to the
server. The server is at `SERVER_ADDRESS`:`SERVER_PORT` below.
"""

# This code uses Python 2.7. These imports make the 2.7 code feel a lot closer
# to Python 3. (They're also good changes to the language!)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import library
import socket


# Where to find the server. This assumes it's running on the smae machine
# as the proxy, but on a different port.
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 7777

# The port that the proxy server is going to occupy. This could be the same
# as SERVER_PORT, but then you couldn't run the proxy and the server on the
# same machine.
LISTENING_PORT = 8888

# Cache values retrieved from the server for this long.
MAX_CACHE_AGE_SEC = 60.0  # 1 minute


def ForwardCommandToServer(command, server_addr, server_port):
  """Opens a TCP socket to the server, sends a command, and returns response.

  Args:
    command: A single line string command with no newlines in it.
    server_addr: A string with the name of the server to forward requests to.
    server_port: An int from 0 to 2^16 with the port the server is listening on.
  Returns:
    A single line string response with no newlines.
  """

  ###################################################
  #TODO: Implement Function: WiP
  ###################################################

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(server_addr, server_port)
  s.send(command)
  data = s.recv(library.COMMAND_BUFFER_SIZE)
  s.close()

  print("The data received was: {}".format(data))
  return data


  



def CheckCachedResponse(command_line, cache):
  cmd, name, text = library.ParseCommand(command_line)

  # Update the cache for PUT commands but also pass the traffic to the server.
  ##########################
  #TODO: Implement section
  ##########################

  status = []
  status[0] = True

  if ( cmd == "PUT" ):
    # Store the key value pair name : text
    cache.StoreValue(name, text)
    status[0] = False
    status[1] = None

  # GET commands can be cached.

  ############################
  #TODO: Implement section
  ############################

  if ( cmd == "GET" ):
    # Get value of key, where key => name
    data = cache.GetValue(name)
    if data == None:
      status[0] = False
      status[1] = None
    else:
      status[1] = data
  
  if ( cmd == "DUMP" ):
    # print everything
    keys = cache.Keys()
    info = []
    for key in keys:
      info.append(cache.GetValue(key))
      status[1] = info
  
  return status


def ProxyClientCommand(sock, server_addr, server_port, cache):
  """Receives a command from a client and forwards it to a server:port.

  A single command is read from `sock`. That command is passed to the specified
  `server`:`port`. The response from the server is then passed back through
  `sock`.

  Args:
    sock: A TCP socket that connects to the client.
    server_addr: A string with the name of the server to forward requests to.
    server_port: An int from 0 to 2^16 with the port the server is listening on.
    cache: A KeyValueStore object that maintains a temorary cache.
    max_age_in_sec: float. Cached values older than this are re-retrieved from
      the server.
  """

  ###########################################
  #TODO: Implement ProxyClientCommand
  ###########################################

  data = sock.recv(library.COMMAND_BUFFER_SIZE)

  info_from_cache =  CheckCachedResponse(data, cache)
  if ( info_from_cache[0] == False ):
    # Forward the request to the server
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((server_addr, server_port))

    # Forward the data to the server
    proxy_socket.send(data)
    # close?
    # proxy_socket.close()


  else:
    # Sending the data directly from the cache back to the client

    sock.send( info_from_cache[1] )



def main():
  # Listen on a specified port...
  server_sock = library.CreateServerSocket(LISTENING_PORT)
  cache = library.KeyValueStore()
  # Accept incoming commands indefinitely.
  while True:
    # Wait until a client connects and then get a socket that connects to the
    # client.
    client_sock, (address, port) = library.ConnectClientToServer(server_sock)
    print('Received connection from %s:%d' % (address, port))
    ProxyClientCommand(client_sock, SERVER_ADDRESS, SERVER_PORT,
                       cache)

  #################################
  #TODO: Close socket's connection
  #################################

  server_sock.close()


main()
