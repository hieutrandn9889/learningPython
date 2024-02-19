import netfilterqueue


def processPacket(packet):
    print(packet)
    # modify in python program
    # accept packet ==> access allowed internet connection
    # drop packet ==> can't access allow internet connection
    packet.drop()


queue = netfilterqueue.NetfilterQueue()
# iptables -I FORWARD -j NFQUEUE — queue-num 0 ==> queue.blind(0, processPacket)
queue.blind(0, processPacket)
queue.run()
