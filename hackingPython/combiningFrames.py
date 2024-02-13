#! /usr/bin/env python
import scapy.all as scapy


def scan(ip):
    # scan ip: 10.211.55.3
    arpRequest = scapy.ARP(pdst=ip)
    print(arpRequest.summary())
    broadcastRequest = scapy.Ether()
    scapy.ls(scapy.Ether())


scan("10.211.55.1/24")
