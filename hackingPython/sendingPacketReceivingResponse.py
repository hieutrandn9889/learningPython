#! /usr/bin/env python
import scapy.all as scapy


def scan(ip):
    # scan ip: 10.211.55.3
    # pdst = Net ('10.211.55.1/24')
    arpRequest = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arpRequestBroadcast = broadcast/arpRequest
    answered, unanswered = scapy.srp(arpRequestBroadcast, timeout=1)
    print(answered.summary())
    print(unanswered.summary())


scan("10.211.55.1/24")
