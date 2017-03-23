from bson.code import Code
from bigdata.mongo_util import db
import os
import simplejson as json

dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    # mapper = Code(open(dir_path + '/wordMap.js', 'r').read())
    # reduce = Code(open(dir_path + '/wordReduce.js', 'r').read())
    # results = db.tickets.map_reduce(mapper, reduce, "word_frequency")
    wq_list = []
    for doc in db.word_frequency.find({"value.count": {"$gt": 50}}):
            wq_list.append([doc['_id'], doc['value']['count']])
    path = dir_path + "/heat_map.json"
    with open(path, 'w') as outfile:
        json.dump(wq_list, outfile)
    print "wq list length: %d"%len(wq_list)
