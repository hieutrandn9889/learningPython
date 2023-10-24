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
        print(cmd_result)

        pattern = r'ether\s[\da-z]{2}:[\da-z]{2}:[\da-z]{2}:[\da-z]{2}:[\da-z]{2}'
        regex = re.compile(pattern)
        ans = regex.search(cmd_result)
        print(ans)
