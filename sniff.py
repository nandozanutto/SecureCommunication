
from logging import exception
from scapy.all import *
import codecs

def process_packet(pkt):
    if pkt.haslayer(TCP):
        tcp = pkt[TCP]
        print("TCP port: {} --> {} && TCP Payload: {} \n".format(tcp.sport, tcp.dport, tcp.payload))

sniff(iface="lo", filter='tcp', prn=process_packet)