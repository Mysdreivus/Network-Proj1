"""A set of libraries that are useful to both the proxy and regular servers."""

# This code uses Python 2.7. These imports make the 2.7 code feel a lot closer
# to Python 3. (They're also good changes to the language!)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# THe Python socket API is based closely on the Berkeley sockets API which
# was originally written for the C programming language.
#
# https://en.wikipedia.org/wiki/Berkeley_sockets
#
# The API is more flexible than you need, and it does some quirky things to
# provide that flexibility. I recommend tutorials instead of complete
# descriptions because those can skip the archaic bits. (The API was released
# more than 35 years ago!)
import socket

import time

# Read this many bytes at a time of a command. Each socket holds a buffer of
# data that comes in. If the buffer fills up before you can read it then TCP
# will slow down transmission so you can keep up. We expect that most commands
# will be shorter than this.
COMMAND_BUFFER_SIZE = 256


def CreateServerSocket(port):
  """Creates a socket that listens on a specified port.

  Args:
    port: int from 0 to 2^16. Low numbered ports have defined purposes. Almost
        all predefined ports represent insecure protocols that have died out.
  Returns:
    An socket that implements TCP/IP.
  """

  #############################################
  #TODO: Implement CreateServerSocket Function
  #############################################

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # Next bind to the port 
  # we have not typed any ip in the ip field 
  # instead we have inputted an empty string 
  # this makes the server listen to requests  
  # coming from other computers on the network 
  s.bind(('', port))
  print("socket binded to {}".format(port))

  print("Server is listening")
  s.listen(5)
  return s

def CreateClientSocket(server_addr, port):
  """Creates a socket that connects to a port on a server."""

  #############################################
  #TODO: Implement CreateClientSocket Function
  #############################################
  client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  client_sock.connect((server_addr, port))

  data = client_sock.recv(COMMAND_BUFFER_SIZE)
  
  print("Data received from server  is {}".format(data))

def ConnectClientToServer(server_sock):
    # Wait until a client connects and then get a socket that connects to the
    # client.
    

    #############################################
    #TODO: Implement CreateClientSocket Function
    #############################################

    # Establish connection with client
    conn, addr = server_sock.accept()

    # This will send a message to the client that connected
    # conn.send('You connected\n')
    
    conn_port = conn.getsockname()[1]
    # print("client listening on port: {}".format(conn_port))
    # conn is the client socket, addr is the address

    return conn, (addr, conn_port)

def ReadCommand(sock):
  """Read a single command from a socket. The command must end in newline."""

  #############################################
  #TODO: Implement ReadCommand Function
  #############################################
  data = sock.recv(COMMAND_BUFFER_SIZE).decode()
  print("{}".format(data))
  return data

  


def ParseCommand(command):
  """Parses a command and returns the command name, first arg, and remainder.

  All commands are of the form:
      COMMAND arg1 remaining text is called remainder
  Spaces separate the sections, but the remainder can contain additional spaces.
  The returned values are strings if the values are present or `None`. Trailing
  whitespace is removed.

  Args:
    command: string command.
  Returns:
    command, arg1, remainder. Each of these can be None.
  """
  args = command.strip().split(' ')
  command = None
  if args:
    command = args[0]
  arg1 = None
  if len(args) > 1:
    arg1 = args[1]
  remainder = None
  if len(args) > 2:
    remainder = ' '.join(args[2:])
  return command, arg1, remainder


class KeyValueStore(object):
  """A dictionary of strings keyed by strings.

  The values can time out once they get sufficiently old. Otherwise, this
  acts much like a dictionary.
  """

  def __init__(self):

    ###########################################
    #TODO: Implement __init__ Function
    ###########################################

    # Store key : value pairs
    self.storage = {}

    

  def GetValue(self, key, max_age_in_sec=None):
    """Gets a cached value or `None`.

    Values older than `max_age_in_sec` seconds are not returned.

    Args:
      key: string. The name of the key to get.
      max_age_in_sec: float. Maximum time since the value was placed in the
        KeyValueStore. If not specified then values do not time out.
    Returns:
      None or the value.
    """
    # Check if we've ever put something in the cache.

    ###########################################
    #TODO: Implement GetValue Function
    ###########################################

    if ( max_age_in_sec == None ):
      if (key in self.storage):
        return self.storage[key]
      else:
        return "Not in database"

    time_now = time.time()
    if ( key in self.storage ):
      time_then = self.storage[key][1]
      # Get the time that passed in seconds
      time_passed = (time_now - time_then)
      # print("Time passed for this key is {}".format(time_passed)) For debugging purposes
      if ( time_passed < max_age_in_sec ):
        return self.storage[key][0]
      else:
        # We need to update the time to now since we are gonna go to the server
        self.storage[key][1] = time.time()
        return "Not in cache"
    else:
      return "Not in cache"



  def StoreValue(self, key, value):
    """Stores a value under a specific key.

    Args:
      key: string. The name of the value to store.
      value: string. A value to store.
    """

    ###########################################
    #TODO: Implement StoreValue Function
    ###########################################

    value_time = []
    # Store the value and the time the value wanted to be stored
    value_time.append(value)
    value_time.append(time.time())

    self.storage[key] = value_time
    return

    

  def Keys(self):
    """Returns a list of all keys in the datastore."""

    ###########################################
    #TODO: Implement Keys Function
    ###########################################

    # print("A list of all the keys are as shown below")

    list_of_keys = []
    for key in self.storage.keys():
      if ( self.storage[key] != None ):
        list_of_keys.append(key)
        print("{}".format(key))
    return list_of_keys
    








