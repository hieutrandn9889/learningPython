#! /usr/bin/env python
import scapy.all as scapy
from scapy.layers import html


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processSniffedPackage)


def processSniffedPackage(packet):
    if packet.haslayer(http.HTTPRequest):
        print(packet)


sniff("eth0")
