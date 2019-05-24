import utils

from flask import Flask, render_template, request, jsonify, session
from elasticsearch import Elasticsearch
from waitress import serve

app = Flask(__name__)
es = Elasticsearch([{'host':'127.0.0.1','port':9200}])

@app.route('/')
def home():
    return render_template('index.html',)

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(index='ctt_hust', body={"query": {"match": {
                                                            "title": search_term
                                                            }
                                                }
                                        })
    return render_template('search.html', res=res)

@app.route('/advance_search', methods=['GET', 'POST'])
def advance_search():
    return render_template('advance_search.html')

@app.route('/advance_search/results', methods=['GET', 'POST'])
def results():
    title = request.form['title_input']
    content = request.form['content_input']
    end_time = request.form['time2']
    start_time = request.form['time1']
    type_news = request.form.get('news_filter')
    print(title, content, end_time, start_time, type_news)
    pre_res = es.search(index='ctt_hust', body={"query": {"bool": {
                                                        "must": [
                                                            {
                                                            "match_phrase": {
                                                                "content": {
                                                                "query": content
                                                                }
                                                            }
                                                            },
                                                            {
                                                            "match_phrase": {
                                                                "title": {
                                                                "query": title
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        })

    res = []
    if len(pre_res['hits']['hits']) > 0:
        for result_ in pre_res['hits']['hits']:
            result = result_
            day = result['_source']['time']
            print(result['_source']['type_lv2'])
            if start_time != '':
                time_check1 = utils.compare_time(day, start_time)
            else:
                time_check1 = True

            if end_time != '':
                time_check2 = utils.compare_time(end_time, day)
            else:
                time_check2 = True
            
            if type_news != '':
                type_check = result['_source']['type_lv2'] == type_news
            else:
                type_check = True


            if time_check1 and time_check2 and type_check:
                res.append(result_)

    pre_res['hits']['hits'] = res
    pre_res['hits']['total'] = str(len(res))

    page = render_template('advance_search_results.html', res=pre_res)
    print(pre_res)
    return page
 


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', port=5000, debug=True)
