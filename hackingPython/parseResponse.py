#! /usr/bin/env python
import scapy.all as scapy


def scan(ip):
    # scan ip: 10.211.55.3
    # pdst = Net ('10.211.55.1/24')
    arpRequest = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arpRequestBroadcast = broadcast/arpRequest
    answeredList = scapy.srp(arpRequestBroadcast, timeout=1)[0]
    for element in answeredList:
        print(element[1].psrc)
        print(element[1].hwsrc)
        print("----------------------------------------------------------------")


scan("10.211.55.1/24")