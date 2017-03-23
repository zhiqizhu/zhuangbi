# encoding=utf-8
from mongo_util import db
import jieba
import jieba.posseg as pseg
import jieba.analyse

import urllib
import urllib2
import os
import simplejson as json
from multiprocessing.dummy import Pool as ThreadPool

dir_path = os.path.dirname(os.path.realpath(__file__))
jieba.load_userdict(dir_path + "/../cd_address.txt")


def find_continuous_ns(address_with_position):
    from operator import itemgetter
    from itertools import groupby
    ranges = []
    for k, g in groupby(enumerate(address_with_position), lambda (i, x): i - x[1]):
        group = map(itemgetter(1), g)
        if group[0] != group[-1]:
            ranges.append((group[0], group[-1]))
    return ranges


def extract_address(text):
    if text:
        result = pseg.cut(text)
        # for word, flag in result:
        #     print('%s %s' % (word, flag))
        address_with_position = []
        for index, item in enumerate(result):
            if item.flag == 'ns':
                address_with_position.append((item.word, index))
        continuous_ns = find_continuous_ns(address_with_position)
        if continuous_ns:
            longest_addr = max(continuous_ns, key=len)
            return ''.join([item[0] for item in longest_addr])
        elif address_with_position:
            return max((len(node[0]), node) for node in address_with_position)[1][0]
        return ''


def search_location(address):
    values = {'keywords': address,
              'city': '028',
              'citylimit': True,
              'key': 'a1f0fbc4acde22165cff48e53434fce1'}
    str_data = {}
    for k, v in values.iteritems():
        str_data[k] = unicode(v).encode('utf-8')
    data = urllib.urlencode(str_data)
    # data = urllib.urlencode(values)
    req = urllib2.Request("http://restapi.amap.com/v3/place/text", data)
    try:
        conn = urllib2.urlopen(req)
        resp = conn.read()
        print resp
        conn.close()
    except:
        print "search location failed"
        return {}
    return json.loads(resp)


def analyze_location():
    for doc in db.tickets.find():
        try:
            if doc.has_key('address') and doc['address']:
                # TODO: find geological info
                pass
            else:
                content = doc['content']
                analyzed_address = extract_address(content)
                if analyzed_address:
                    db.tickets.update_one(
                        {'_id': doc['_id']},
                        {
                            '$set': {'analyzed_address': analyzed_address}
                        }
                    )
                    print "updated doc with %s" % analyzed_address
        except KeyError:
            print "this document has no content"


def _get_from_map(map, key):
    try:
        return map[key]
    except KeyError:
        return None


task_index = 1


def set_geo_info():
    cursor = db.tickets.find({"location": {"$exists": False},
                              "$or": [{"address": {"$ne": None}}, {"analyzed_address": {"$ne": None}}]})
    count = cursor.count()
    print "count: %d" % count
    pool = ThreadPool(50)
    pool.map(set_geo_info_task, cursor)
    pool.close()
    pool.join()


def set_geo_info_task(doc):
    global task_index
    task_index += 1
    print "task_index: %s" % task_index
    location_info = {}
    if _get_from_map(doc, 'address'):
        location_info = search_location(doc['district'] + doc['address'])
    elif _get_from_map(doc, 'analyzed_address'):
        if doc['analyzed_address'].startswith(doc['district']):
            address = doc['analyzed_address']
            location_info = search_location(address)
        else:
            address = doc['district'] + doc['analyzed_address']
            location_info = search_location(address)

    if _get_from_map(location_info, 'status') == '1':
        location = location_info['pois'][0]['location'] if (len(location_info['pois']) > 0) else None
        print location
        if location:
            db.tickets.update_one(
                {'_id': doc['_id']},
                {
                    '$set': {'location': location}
                }
            )


def heat_map_data_to_json(path):
    cursor = db.tickets.find({"location": {"$exists": True}})
    print "data amount: %d" % cursor.count()
    json_list = []
    for doc in cursor:
        lng, lat = doc['location'].split(',')
        json_list.append({
            "lng": lng,
            "lat": lat,
            "count": 1
        })


if __name__ == '__main__':
    # analyze_location()
    # set_geo_info()
    # heat_map_data_to_json(dir_path + "/heat_map.json")
    jieba.analyse.set_idf_path("./idf.txt.big")
    for doc in db.tickets.find().limit(10):
        s = doc['content'] if doc.has_key('content') else None
        keyword1 = ' '.join(jieba.analyse.textrank(s, allowPOS=('n', 'vn', 'v')))
        keyword2 = jieba.analyse.extract_tags(s, topK=20, withWeight=False,allowPOS=('n', 'vn', 'v'))

        # if keyword:
        #     db.tickets.update_one(
        #         {'_id': doc['_id']},
        #         {
        #             '$set': {'keyword': keyword}
        #         }
        #     )
        print(keyword1)
        print('%s' % ",".join(keyword2))
