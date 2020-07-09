from kadi_apy.lib.core import KadiAPI
from kadi_apy.lib.records import Record
from kadi_apy.lib.collections import Collection
import json
import time


class kadi():
    def __init__(self,conf):
        KadiAPI.token = conf['PAT']
        KadiAPI.host = conf['host']

    def addRecord(self, ident,title,visibility,filed,meta=None): #filed is a json 
        #create a record
        record = Record(identifier=ident, title=title, visibility=visibility)
        record.upload_string_to_file(string=json.dumps(filed),file_name='{}_{}.json'.format(ident,time.time_ns()))
        #add metadatum
        df = pd.io.json.json_normalize(d, sep='_')
        meta_flat = df.to_dict(orient='records')[0]
        record.add_metadatum(metadatum=meta_flat, force=True)

    def addCollection(self,identifier, title, visibility):
        #create collection
        collection = Collection(identifier=ident, title=title, visibility=visibility)

    def addRecordToCollection(self,identCollection,identRecord,visibility='public',record=None):
        collection = Collection(identifier=identCollection, title='title', visibility=visibility)
        if record == None:
            record = Record(identifier=identRecord, title='title', visibility=visibility)
        #add record to collection
        collection.add_record(record_id=record.id)