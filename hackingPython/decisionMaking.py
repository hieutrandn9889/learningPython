#! /usr/bin/env python
import subprocess
import optparse


def getArguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="newMac",
                      help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error(
            "[-] Please specify an interface must be specified, use --help for more information.")
    elif not options.newMac:
        parser.error(
            "[-] Please specify a new MAC must be specified, use --help for more information.")
    return options


def changeMac(interface, newMac):
    print("[+] Changing MAC address for " + interface + " to " + newMac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", newMac])
    subprocess.call(["ifconfig", interface, "up"])


options = getArguments()
changeMac(options.interface, options.newMac)
