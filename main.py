from changeMacAddress import Mac_changer

if __name__ == '__main__':
    mc = Mac_changer()
    changeMacAddress = mc.get_MAC_Address("eth0")
    current_mac = mc.change_MAC_Address("eth0", "00:11:22:33:44")
