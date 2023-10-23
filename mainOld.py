import subprocess
import optparse
import re


# interface = input("interface > ")
# newMac = input("new MAC > ")

# interface = raw_input("interface > ")
# newMac = raw_input("new MAC > ")

# (options, arguments) options = -i, -m and argument = dest ="interface" or dest = "newMac" => eth0 or 00:11
def getArguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="newMac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify and interface, use --help for more information")
    elif not options.newMac:
        parser.error("[-] Please specify and MAC, use --help for more information")
    return options


def changeMac(interface, newMac):
    print("[+] Changing Mac address for " + interface + " to " + newMac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", newMac])
    subprocess.call(["ifconfig", interface, "up"])


def getCurrentMac(interface):
    # enter the line (\n)
    # .decode("utf-8") => convert byte  to string
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    print(ifconfig_result)
    # get address eth0
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


# interface = options.interface
# newMac = options.newMac

options = getArguments()
currentMac = getCurrentMac(options.interface)
print("Current Mac = " + str(currentMac))

changeMac(options.interface, options.newMac)
currentMac = getCurrentMac(options.interface)
if currentMac == options.newMac:
    print("[+] MAC address was successfully changed to " + currentMac)
else:
    print("[-] Mac address did not get changed.")
# print("[+] Changing MAC address for " + interface + " to " + newMac)
# subprocess.call("ifconfig" + interface + " down", shell=True)
# subprocess.call("ifconfig" + interface + " hw ether" + newMac, shell=True)
# subprocess.call("ifconfig" + interface + " up", shell=True)

# subprocess.call("ifconfig eth0 down", shell=True)
# subprocess.call("ifconfig eth0 hw ether 00:11:22:33:44:77", shell=True)
# subprocess.call("ifconfig eth0 up", shell=True)
