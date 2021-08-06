#!/usr/bin/env python3
from scapy.all import *

# Função de configuração, que indica o que fazer com os pacotes sniffados
def sniffTcpPacket(pkt):
    # Verifica se existe o TCP no pacote 
    if pkt.haslayer(TCP):
        tcp = pkt[TCP]
        # Caso exista, apenas imprime a porta da origem e destino e imprime o payload
        print("TCP port: {} --> {} && TCP Payload: {} \n".format(tcp.sport, tcp.dport, tcp.payload))


# Função do scapy para fazer o sniffer
sniff(iface="lo", filter='tcp', prn=sniffTcpPacket)
