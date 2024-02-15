#! /usr/bin/env python
import scapy.all as scapy


def scan(ip):
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
    for element in answeredList:
        print("IP\t\t\tMAC Address\n-------------------------------------------")
        print(element[1].psrc + "\t\t" + element[1].hwsrc)


scan("10.211.55.1/24")
