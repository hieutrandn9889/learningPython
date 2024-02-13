#! /usr/bin/env python
import scapy.all as scapy


def scan(ip):
    # scan ip: 10.211.55.3
    # pdst = Net ('10.211.55.1/24')
    arpRequest = scapy.ARP(pdst=ip)
    arpRequest.show()
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast.show()
    arpRequestBroadcast = broadcast/arpRequest
    arpRequestBroadcast.show()


scan("10.211.55.1/24")
