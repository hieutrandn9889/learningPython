import subprocess

# ifconfig eth0 down
# ifconfig eth0 hw ether 00:11:22:33:44:55
# ifconfig eth0 up


class Mac_changer:
    def __init__(self):
        self.MAC = ""

    def get_MAC(self, iface):
        output = subprocess.run(['ifconfig', iface],
                                shell=False, capture_output=True)

        cmd_result = output.stdout.decode('utf-8')
        print(cmd_result)
