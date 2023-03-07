from pymongo import MongoClient
import secret_info
import pandas as pd
import pickle
import logging

logging.basicConfig(filename='/home/erkahraman/Belgeler/python_dosyalari/NFStreamTest/Pipeline/pipeline.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

def database_connection(collection_name):
    # Database Connection
    client = MongoClient(secret_info.database_connection)
    db = client["Main"]
    collection = db[collection_name]
    return collection

def data_control(collection):
    # Pipeline Control
    df = pd.DataFrame.from_records(list(collection.find()))
    if len(df) > 0:
        return 1
    else: return 0


def run_model(df):

    collection = database_connection("pipeline") # Connection to database
    checkpoint = df["bidirectional_first_seen"].max() # Detect Last Checkpoint

    # İmport Model
    ICMP_Model = pickle.load(open('/home/erkahraman/Belgeler/python_dosyalari/NFStreamTest/Analysis/icmp_exf_tpot.pkl', 'rb'))
    

    #ICMP Data Exfiltration Detection
    def ICMP_Exf_Model(df, model):
        
        df = df.query("application_name == 'ICMP'") # Get ICMP Data

        if len(df) > 0: # İf dataframe not empty
            # Prediction Stage
            df["predict"] = model.predict(df.loc[:, ['bidirectional_duration_ms','bidirectional_packets', 'bidirectional_bytes', 'src2dst_duration_ms', 'src2dst_packets',
            'src2dst_bytes', 'dst2src_duration_ms', 'dst2src_packets', 'dst2src_bytes',
            'bidirectional_min_ps', 'bidirectional_mean_ps','bidirectional_stddev_ps', 'bidirectional_max_ps', 'src2dst_min_ps',
            'src2dst_mean_ps', 'src2dst_stddev_ps', 'src2dst_max_ps','dst2src_min_ps', 'dst2src_mean_ps', 'dst2src_stddev_ps',
            'dst2src_max_ps', 'bidirectional_min_piat_ms','bidirectional_mean_piat_ms', 'bidirectional_stddev_piat_ms',
            'bidirectional_max_piat_ms', 'src2dst_min_piat_ms', 'src2dst_mean_piat_ms', 'src2dst_stddev_piat_ms', 'src2dst_max_piat_ms',
            'dst2src_min_piat_ms', 'dst2src_mean_piat_ms', 'dst2src_stddev_piat_ms','dst2src_max_piat_ms']])

            attackers = df.query("predict == 1")
            attackers = attackers[["src_ip", "dst_ip", "src_port", "dst_port", "bidirectional_first_seen", "bidirectional_last_seen"]]
            attackers["attack_type"] = "ICMP_Exfiltration"
            return attackers
        else: # İf dataframe empty
            attackers = pd.DataFrame(columns=(["src_ip", "dst_ip", "src_port", "dst_port", "bidirectional_first_seen", "bidirectional_last_seen"])) # Empty dataframe
            attackers["attack_type"] = "ICMP_Exfiltration"
            return attackers

    

    collection.insert_one({'checkpoint': checkpoint,'icmp_exf_attack': ICMP_Exf_Model(df, ICMP_Model).to_dict('records')}) # Write to database
    logging.info("Wrote to Database")



def main():
    logging.info("Starting Main!")

    logging.info("Database Connection.")
    # Database connection to pipeline
    collection = database_connection("pipeline")

    logging.info("Checking State.")
    # Data control on pipeline collection
    state = data_control(collection)
    
    if state == 0: # Pipeline collection is empty
        logging.info("State: 0")
        logging.info("Database Connection.")
        collection = database_connection("flows") # Connect to flows
        logging.info("Getting Data!")
        df = pd.DataFrame.from_records(list(collection.find({"application_name": "ICMP"}))) # Get All ICMP Data
        if len(df) != 0:
            logging.info("Run Model!")
            run_model(df)
        else:
            logging.info("There is no data!")
    else: # Pipeline collection is not empty
        logging.info("State: 1")
        logging.info("Database Connection.")
        
        # Detect Checkpoint
        collection = database_connection("pipeline") # Connect to pieline
        logging.info("Get last document.")
        last_document = collection.find().sort([("_id", -1)]).limit(1)[0] # Get last doc
        checkpoint = last_document["checkpoint"] # Get checkpoint from last doc

        logging.info("Database Connection.")
        collection = database_connection("flows") # Connect to flows

        logging.info("Getting Data!")
        df = pd.DataFrame.from_records(list(collection.find({"bidirectional_first_seen": {"$gt": checkpoint}, "application_name": "ICMP"}))) # Get ICMP Data for Checkpoint
        if len(df) != 0:
            logging.info("Run Model!")
            run_model(df)
        else:
            logging.info("There is no data!")
        

main()
logging.info("\n")