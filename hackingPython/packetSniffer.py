#! /usr/bin/env python
import scapy.all as scapy


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processSniffedPackage)


def processSniffedPackage(packet):
    print(packet)


sniff("eth0")
