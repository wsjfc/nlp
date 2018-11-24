import elasticsearch5
from elasticsearch5.helpers import parallel_bulk
import logging
import hashlib
import pandas as pd


ES_ADDRESS = 'localhost:9200'
ES_INDEX = 'test0717'
ES_TYPE = 'test'

# tracer = logging.getLogger('elasticsearch.trace')
# tracer.setLevel(logging.INFO)
# tracer.addHandler(logging.FileHandler('/tmp/es_trace.log'))

# FORMAT = '[%(asctime)-15s] %(message)s'
# logging.basicConfig(level=logging.DEBUG, format=FORMAT)
class OpenEs(object):
    def __init__(self, error_type, error_val):
        self.error_val = error_val
        self.error_type = error_type

    def __enter__(self):
        return elasticsearch5.Elasticsearch([ES_ADDRESS])

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.error_val[0] = exc_val
        if exc_type:
            self.error_type[0] = exc_type
        return False


class HandleDatabase(object):
    # @profile
    def get_intent(self, sentence,N):
        # model = load_model()
        error_type, error_val = (['success'], ['null'])
        with OpenEs(error_type, error_val) as es:
            query_context = sentence.strip()
            body = {"query":{'match': {'query_context': query_context}},'size':N}
            hits = es.search(index=ES_INDEX, doc_type=ES_TYPE, body=body)['hits']['hits']

            print(hits)

    def import_intent(self, inputFile):
        '''
        :param inputFile:file need to be import to es database,csv format,see import_test.csv
        :return: None
        '''
        es = elasticsearch5.Elasticsearch(['localhost:9200'])
        index = ES_INDEX

        # create index
        mapping = '''
                {  
                  "mappings":{  
                    "test":{  
                      "properties":{  
                        "context_query":{  
                          "type":"text",
                          "analyzer":"ik_max_word",
                          "search_analyzer":"ik_max_word"
                        },
                        "response":{  
                          "type":"keyword"
                        },
                      }
                    }
                  }
                }'''
        # 查询数据库是否存在，不存在则创建，存在则不做修改
        try:
            es.search(index=ES_INDEX)
        except:
            es.indices.create(index=index, ignore=400, body=mapping)

        def bulk_data(index_name, df):
            for i, row in df.iterrows():
                json_body = {}
                json_body['query_context'] = row['query_context']
                json_body['response'] = row['response']

                doc = {}
                doc['_op_type'] = 'index'
                doc['_index'] = index_name
                doc['_type'] = ES_TYPE
                # user_say和intent作为_id
                doc['_id'] = hashlib.md5((json_body['query_context'] + json_body['response']).encode('utf8')).hexdigest()
                doc['_source'] = json_body

                yield doc

        if isinstance(inputFile, pd.DataFrame):
            df = inputFile
        else:
            df = pd.read_csv(inputFile, dtype=object)

        for success, info in parallel_bulk(client=es, actions=bulk_data(index, df), thread_count=16):
            if not success:
                print('Doc failed', info)


if __name__ == '__main__':
    es_test = HandleDatabase()
    # es_test.import_intent('yitu0621_v2.csv')
    # es_test.create_index()
    # print(es_test.insert_sentence_intent('好呀','好'))
    # print(es_test.insert_sentence_intent('好的','好'))
    # print(es_test.delete_intent('不要'))
    # print(es_test.get_intent('是',2))
    # print(es_test.update_intent('好的','好','不要吧'))