from google.cloud import bigquery
import os


# TODO add for specific date ranges to queries

client = bigquery.Client()


# read in query from .txt file

def handle_file(dirpath, filename):
    filepath = os.path.join(dirpath, filename)
    
    if filename.endswith('.txt'):
        try:
            with open(filepath, "r") as file:
                query = file.read()
            return (filepath, query)
        except:
            print('error')   
    return



for dirpath, dirnames, filenames in os.walk('./'):
    for filename in filenames:
        filepath, query = handle_file(dirpath, filename)
        
        if query is not None:
            print(query)
            # query_job = client.query(QUERY)  # API request
            # rows = query_job.result()  # Waits for query to finish
                
# # write results to the .txt file
