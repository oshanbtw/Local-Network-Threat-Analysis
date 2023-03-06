import os 
import time
import logging

logging.basicConfig(filename='sender.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


file_name = ["passlist.txt", "passlist2.txt", "passlist3.txt", "passlist4.txt", "passlist5.txt", "passlist6.txt", "passlist7.txt", "passlist8.txt", "passlist8.txt", 
             "passlist9.txt", "passlist10.txt", "passlist11.txt", "passlist12.txt", "passlist13.txt", "passlist14.txt", "passlist15.csv", "passlist16.txt", "passlist17.txt",
             "passlist18.txt", "passlist19.txt", "passlist20.txt", "passlist21.txt", "passlist22.txt"]
counter = 1
while True:
    logging.info("Counter:", counter)
    for i in range(len(file_name)):
        os.system("./qssender send file -d 2 -l 192.168.1.51 -r 192.168.1.54 -s 50000 {}".format(file_name[i]))
        logging.info("50.000 with {}".format(file_name[i]))
        time.sleep(40)

    for i in range(len(file_name)):
        os.system("./qssender send file -d 2 -l 192.168.1.51 -r 192.168.1.54 -s 5000 {}".format(file_name[i]))
        logging.info("5.000 with {}".format(file_name[i]))
        time.sleep(40)

    for i in range(len(file_name)):
        os.system("./qssender send file -d 2 -l 192.168.1.51 -r 192.168.1.54 -s 500 {}".format(file_name[i]))
        logging.info("500 with {}".format(file_name[i]))
        time.sleep(40)
    
    counter += 1
    logging.info("\n")