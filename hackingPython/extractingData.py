#! /usr/bin/env python
import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processSniffedPackage)


def processSniffedPackage(packet):
    # HTTPRequest is an existing
    if packet.haslayer(http.HTTPRequest):
        print(packet.show())


sniff("eth0")
