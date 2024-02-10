#! /usr/bin/env python
import subprocess
import optparse


def changeMac():
    print("[+] Changing MAC address for " + interface + " to " + newMac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether ", newMac])
    subprocess.call(["ifconfig", interface, "up"])


parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface",
                  help="Interface to change its MAC address")
parser.add_option("-m", "--mac", dest="newMac",
                  help="New MAC address")

(options, args) = parser.parse_args()
changeMac(options.interface, options.newMac)
