#! /usr/bin/env python
import subprocess

interface = "eth0"
newMac = "00:11:22:33:44:55"

print("[+] Changing MAC address for " + interface + " to " + newMac)

subprocess.call("ifconfig", shell=True)
subprocess.call("ifconfig" + interface + "down", shell=True)
subprocess.call("ifconfig" + interface + "hw ether" + newMac, shell=True)
subprocess.call("ifconfig" + interface + "up", shell=True)
subprocess.call("ifconfig" + interface, shell=True)
