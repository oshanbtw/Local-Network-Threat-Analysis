from nfstream import NFStreamer
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import os


def pcap_reader(pcap_path):
    df = NFStreamer(source=pcap_path,
                         decode_tunnels=True,
                         bpf_filter=None,
                         promiscuous_mode=True,
                         snapshot_length=1536,
                         idle_timeout=120,
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


    #Timestamp olan değerleri datetime'a çevirip dataframe'a aktarıyorum.
    df['bidirectional_first_seen'] = pd.to_datetime(df['bidirectional_first_seen_ms'], unit='ms')
    df['bidirectional_last_seen'] = pd.to_datetime(df['bidirectional_last_seen_ms'], unit='ms')

    #Dosyayı okuduktan sonra siliyorum.
    os.remove(pcap_path)

    return df

def database_connection(df):
    #Database connection    
    client = MongoClient("mongodb+srv://admin_oe:oe123456789@flows.lizea4s.mongodb.net/test")
    db = client["Main"]
    collection = db["flows"]

    #Push to database.
    collection.insert_many(df.to_dict('records'))

pcap_path = "/home/erkahraman/Belgeler/python_dosyalari/NFStreamTest/pcaps/traffic.pcap"
data = pcap_reader(pcap_path)
database_connection(data)


