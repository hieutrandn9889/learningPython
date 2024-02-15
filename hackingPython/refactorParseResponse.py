#! /usr/bin/env python
import scapy.all as scapy


def scan(ip):
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

    clientList = []
    for element in answeredList:
        clientDict = {"ip" + element[1].psrc, "mac" + element[1].hwsrc}
        clientList.append(clientDict)
    return clientList


def printResult(resultList):
    print("resultList" + resultList)
    # resultList is array
    print("IP\t\t\tMAC Address\n-------------------------------------------")
    for client in resultList:
        # client["ip"] and client["mac"] with ip, mac are key
        print(client["ip"] + "\t\t" + client["mac"])


scanResult = scan("10.211.55.1/24")
printResult(scanResult)
