import subprocess
import re

def get_current_mac(interface):
    result = subprocess.run(['ifconfig', interface], stdout=subprocess.PIPE, text=True)
    output = result.stdout
    
    mac_address = re.search(r'(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)', output)
    if mac_address:
        return mac_address.group(0)
    else:
        return None

def change_mac(interface, new_mac):
    subprocess.run(['sudo', 'ifconfig', interface, 'down'])
    subprocess.run(['sudo', 'ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.run(['sudo', 'ifconfig', interface, 'up'])

def is_valid_mac(mac):
    return re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', mac) is not None

interface = 'eth0'  

current_mac = get_current_mac(interface)
if current_mac:
    print(f"Current MAC address of {interface}: {current_mac}")
else:
    print(f"Could not find MAC address for {interface}")

new_mac = input("Enter the new MAC address: ")

if is_valid_mac(new_mac):
    change_mac(interface, new_mac)
    print(f"MAC address of {interface} changed to {new_mac}")
else:
    print("Invalid MAC address format. Please enter a valid MAC address.")