import os
import logging

logging.basicConfig(filename='receiver.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

counter = 1

while True:
    logging.info("Counter:", counter)
    logging.info("Receiving")
    os.system("./qsreceive receive -l 192.168.1.49 -f received_file.txt")
    logging.info("Received\n")
    counter += 1