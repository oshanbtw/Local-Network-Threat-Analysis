from nfstream import NFStreamer
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import os
import logging
import secret_info

logging.basicConfig(filename='pusher.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def pcap_reader(pcap_path):
    try:
        logging.info("Pcap Reading")
        df = NFStreamer(source=pcap_path,
                            decode_tunnels=True,
                            bpf_filter=None,
                            promiscuous_mode=True,
                            snapshot_length=1536,
                            idle_timeout=30,
                            active_timeout=1800,
                            accounting_mode=0,
                            udps=None,
                            n_dissections=20,
                            statistical_analysis=True,
                            splt_analysis=0,
                            n_meters=0,
                            max_nflows=0,
                            performance_report=0,
                            system_visibility_mode=0,
                            system_visibility_poll_ms=100).to_pandas()

        logging.info("Time Changing")
        #Timestamp olan değerleri datetime'a çevirip dataframe'a aktarıyorum.
        df['bidirectional_first_seen'] = pd.to_datetime(df['bidirectional_first_seen_ms'], unit='ms')
        df['bidirectional_last_seen'] = pd.to_datetime(df['bidirectional_last_seen_ms'], unit='ms')

        logging.info("Pcap Removing")
        #Dosyayı okuduktan sonra siliyorum.
        os.remove(pcap_path)
        logging.info("Succsess!")

        return df
    except Exception as e:
        logging.error("Error:",e)

def database_connection(df):
    try:
        logging.info("Connecting to database.")
        #Database connection    
        client = MongoClient(secret_info.database_connection)
        db = client["Main"]
        collection = db["flows"]

        logging.info("Pushing to database.")
        #Push to database.
        collection.insert_many(df.to_dict('records'))
        logging.info("Succsess!\n")

    except Exception as e:
        logging.error(str(e) + "\n")

pcap_path = secret_info.pcap_path
data = pcap_reader(pcap_path)
database_connection(data)


