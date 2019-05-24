# import requests, json, os

# # directory to json file
# filename = './ctt_hust/ctt_hust_3.json'

# # ================= Load json file into Elasticsearch ===========

# f = open(filename, 'r')
# data = json.load(f)
# f.close()

# clearData = data
# total_line = len(data)

# dic_type = {'Đào tạo Sau đại học': [],
#             'Công tác Sinh viên': [],
#             'Đào tạo Đại học': []}

# for i, line in enumerate(clearData):
#     for type_lv1 in dic_type.keys():
#         if line['type_lv1'] == type_lv1 and line['type_lv2'] not in dic_type[type_lv1]:
#             dic_type[type_lv1].append(line['type_lv2'])
        
# print(dic_type)
    
# # ================= End load data into elasticsearch ==============
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'127.0.0.1','port':9200}])
def compare_time(day1, day2):
    '''Comparing 2 days. If day1 is later than day2 then return True else False'''
    day1, day2 = standard(day1), standard(day2)

    day1 = day1.split('/')
    day1.reverse()
    day1 = int(''.join(day1))

    day2 = day2.split('/')
    day2.reverse()
    day2 = int(''.join(day2))

    if day1 > day2:
        return True
    
    else:
        return False

def standard(day):
    day = day.split('/')
    if int(day[1]) < 10 and len(day[1]) == 1:
        day[1] = '0' + day[1]
    
    if int(day[0]) < 10 and len(day[0]) == 1:
        day[0] = '0' + day[0]
    day = '/'.join(day)

    return day


res = es.search(index='ctt_hust', body={"query": {"bool": {
                                                        "must": [
                                                            {
                                                            "match_phrase": {
                                                                "content": {
                                                                "query": "Bách khoa"
                                                                }
                                                            }
                                                            },
                                                            {
                                                            "match_phrase": {
                                                                "title": {
                                                                "query": "Tốt nghiệp"
                                                                }
                                                            }
                                                        }
                                                        ]
                                                        }
                                                    }
                                                })

final_res = []
for result in res['hits']['hits']:
    day = result['_source']['time']
    if result['_source']['type_lv2'] == 'Tin tức - Thông báo' and (compare_time(day, '15/7/2017') and compare_time('19/7/2017', day)):
        final_res.append(result)

print(final_res)