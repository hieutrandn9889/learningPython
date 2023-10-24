import subprocess
import re
# ifconfig eth0 down
# ifconfig eth0 hw ether 00:11:22:33:44:55
# ifconfig eth0 up


class Mac_changer:
    def __init__(self):
        self.MAC = ""

    def get_MAC_Address(self, iface):
        output = subprocess.run(['ifconfig', iface],
                                shell=False, capture_output=True)

        cmd_result = output.stdout.decode('utf-8')

        # ifconfig eth0
        print(cmd_result)

        # format eth0 address
        pattern = r'ether\s[\da-z]{2}:[\da-z]{2}:[\da-z]{2}:[\da-z]{2}:[\da-z]{2}'
        regex = re.compile(pattern)
        ans = regex.search(cmd_result)

        # filter address
        current_mac = ans.group().split(" ")[1]
        self.MAC = current_mac
        return current_mac