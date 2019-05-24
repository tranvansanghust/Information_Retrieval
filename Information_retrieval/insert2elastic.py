import requests, json, os
from elasticsearch import Elasticsearch
from datetime import  datetime

# directory to json file
filename = './ctt_hust/ctt_hust_3.json'

# Connect to the elastic cluster
es=Elasticsearch([{'host':'127.0.0.1','port':9200}])
#
# ================= Load json file into Elasticsearch ===========

f = open(filename, 'r')
data = json.load(f)
f.close()

print()
clearData = data
total_line = len(data)

for i, line in enumerate(clearData):
    print('processing' + str(i) + '/' + str(total_line), end="\r")
    es.index(index='ctt_hust', doc_type='news', id=i, body=line)

# ================= End load data into elasticsearch ==============
