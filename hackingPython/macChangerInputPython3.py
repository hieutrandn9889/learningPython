#! /usr/bin/env python
import subprocess

interface = input("interface > ")
newMac = input("new MAC > ")

print("[+] Changing MAC address for " + interface + " to " + newMac)

subprocess.call("ifconfig " + interface + " down", shell=True)
subprocess.call("ifconfig " + interface + " hw ether" + newMac, shell=True)
subprocess.call("ifconfig " + interface + " up", shell=True)
subprocess.call("ifconfig " + interface, shell=True)
