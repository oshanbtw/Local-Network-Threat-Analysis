import subprocess
import time
import os
import logging

logging.basicConfig(filename='picker.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

def pick():
    try:
        logging.info("Tcpdump Start")
        subprocess.Popen(["sudo","tcpdump", "-w", "/home/erkahraman/Belgeler/python_dosyalari/NFStreamTest/traffic.pcap"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(598)

        # tcpdump'u durdurur
        subprocess.Popen(["sudo","pkill", "tcpdump"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info("Tcpdump Stop")
        logging.info("Move Start")
        os.system("mv /home/erkahraman/Belgeler/python_dosyalari/NFStreamTest/traffic.pcap /home/erkahraman/Belgeler/python_dosyalari/NFStreamTest/pcaps/")
        logging.info("Succsess!\n")
    except Exception as e:
        logging.error(str(e) + "\n")


pick()
