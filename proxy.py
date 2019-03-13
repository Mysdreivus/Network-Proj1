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
  # print("cmd => {} name => {} text=> {}".format(cmd, name, text))

  # Update the cache for PUT commands but also pass the traffic to the server.
  ##########################
  #TODO: Implement section
  ##########################

  if ( cmd == "PUT" ):
    # Store the key value pair name : text and then return Not in cache so we head to the server
    cache.StoreValue(name, text)
    return "Not in cache"

  # GET commands can be cached.

  ############################
  #TODO: Implement section
  ############################

  if ( cmd == "GET" ):
    print("This is the getting in the cache")
    # Get value of key, where key => name
    if name in cache.storage:
      return cache.GetValue(name, MAX_CACHE_AGE_SEC)
    else:
      return "Not in cache"
  
  if ( cmd == "DUMP" ):
    # This is so that when we call the DUMP Command we only get it from the server, since DUMP
    # shouldn't be cached
    return "Not in cache"


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

  data = sock.recv(library.COMMAND_BUFFER_SIZE).decode()
  print("The data received is {}".format(data))

  info_from_cache = CheckCachedResponse(data, cache)
  print(info_from_cache)

  if ( info_from_cache == "Not in cache" ):
    # Forward the request to the server
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.connect((server_addr, server_port))

    # Forward the data to the server
    proxy_socket.send(data)

    new_data = proxy_socket.recv(library.COMMAND_BUFFER_SIZE).decode()
    print("This is the data received")
    print(new_data)

    if ( new_data != "This key is not in the database" ):
      # Update the cache in the proxy
      # print("The new data is => {}".format(new_data))
      my_cmd, my_name, my_text = library.ParseCommand(data)
      if ( my_cmd == "GET" ):
        # print("Key and value are => {} and {}".format(my_name, new_data))
        cache.StoreValue(my_name, new_data)

    if ( new_data == None ):
      new_data = "No data was stored in this key\n"
    sock.send(new_data)
    sock.close()


  else:
    # Sending the data directly from the cache back to the client
    print("Sending directly from cache")
    if (info_from_cache == None):
      my_cmd, my_name, my_text = library.ParseCommand(data)
      possible_cmds = ("GET", "PUT")
      if ( my_cmd in possible_cmds ):
        info_from_cache = "No data was stored in this key"
      else:
        info_from_cache = "Error command"
    info_from_cache += "\n"
    sock.send(info_from_cache)
    sock.close()



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

  client_sock.close()

  server_sock.close()


main()
