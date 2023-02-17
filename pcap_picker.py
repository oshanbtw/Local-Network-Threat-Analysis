import subprocess
import time
import os

def pick():
    subprocess.Popen(["sudo","tcpdump", "-w", "/home/erkahraman/Belgeler/python_dosyalari/NFStreamTest/traffic.pcap"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(598)

    # tcpdump'u durdurur
    subprocess.Popen(["sudo","pkill", "tcpdump"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.system("mv /home/erkahraman/Belgeler/python_dosyalari/NFStreamTest/traffic.pcap /home/erkahraman/Belgeler/python_dosyalari/NFStreamTest/pcaps/")


pick()
