#!/bin/python3
import sys
import socket
from datetime import datetime

# Define our target
if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1])  # translate hostname to ip4
else:
    print("Invalid amount of arguments.")
    print("Syntax: python3 scanIP.py <ip>")

# Add a pretty banner
print("-" * 50)
print("- Scanning target " + target)
print("Time started:" + str(datetime.now()))
print("-" * 50)

try:
    for port in range(1, 65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))
        print("Checking port {}".format(port))  # return an error indicating
        if result == 0:
            print("Port {} is open".format(port))
            s.close()

except KeyboardInterrupt:
    print("\nExiting program.")
    sys.exit()


except socket.gaierror:
    print("Hostname could not be resolved.")
    sys.exit()


except socket.error:
    print("Could not connect to server.")
    sys.exit()
