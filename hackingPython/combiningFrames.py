#! /usr/bin/env python
import scapy.all as scapy


def scan(ip):
    arpRequest = scapy.ARP(pdst=ip)
    print(arpRequest.summary())


scan("10.211.55.1/24")
