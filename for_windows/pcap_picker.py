import subprocess
import time
import logging
import os
import shutil
logging.basicConfig(filename='picker.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
def pick():
    
    try:
        # Kaydetmek istediğiniz dosya yolunu ve adını belirtin
        file_path = r"C:\Users\erkahraman\Documents\LTA\kayit.pcap"
        file_location = r"C:\Users\erkahraman\Documents\LTA"
        pcap_destination = r"C:\Users\erkahraman\Documents\LTA\pcaps"
        pcap_name = "kayit.pcap"
    
        record_time = 10 # Second

        logging.info("Tshark Start")
        # Create tshark command
        tshark_command = [
            r"C:\Program Files\Wireshark\tshark.exe",
            "-i", "Wi-Fi",  # Interface
            "-a", f"duration:{record_time}",  # Record time
            "-w", file_path  # Save path
        ]

        # Run tshark command
        subprocess.run(tshark_command)

        # Belirtilen süre boyunca bekleyin
        #time.sleep(record_time)
        logging.info("Tshark Succsess!")
        # Source path
        source_file_path = os.path.join(file_location, pcap_name)

        # Destination path
        destination_file_path = os.path.join(pcap_destination, pcap_name)
        # Copy files
        shutil.copy2(source_file_path, destination_file_path)
        logging.info("Move Succsess!")

        os.remove(file_path)
        logging.info("Remove Succsess!\n")
        
    except Exception as e:
        logging.error(str(e) + "\n")

pick()
