import pymongo 
import os 
import pandas as pd

mongo_uri = "mongodb+srv://prashantsinghaiengineer:6lT4EGmuVUwxPkMU@cluster0.q3083.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#mongodb+srv://<username>:<password>@cluster0.q3083.mongodb.net/?retryWrites=true&w=majority

cwd=os.getcwd()


dir_path = os.path.join(cwd,"notebook")
file_name = "EasyVisa.csv"
file_path = os.path.join(dir_path,file_name)




def Mongo_connection(db:str,collection:str):
    mongo_connection= mongo_uri
    if mongo_connection:
        client = pymongo.MongoClient(mongo_connection)
        Mongo_db= client[db]
        Mongo_collection =  Mongo_db[collection]
        return Mongo_collection
    else:
        print(f"Wrong uri: {mongo_connection}")

def load_data(mongo_connection):
    df = pd.read_csv(file_path)
    data = df.to_dict(orient='records')
    print("Data Insersion in Mangodb Started...")
    mongo_connection.insert_many(data)
    print("Data insersion completed...")





