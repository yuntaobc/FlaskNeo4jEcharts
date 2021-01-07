from . import api
from app.models import neo4j_db
from flask import render_template, session, redirect, url_for
from flask import Flask, g, Response, request
# from ..models import neo4j_session
import json

CATEGORY_EVENT = 0
CATEGORY_USER = 1
CATEGORY_TOPIC = 2


@api.route('/topic/neighbor', methods=['GET', 'POST'])
def topic_neighbor():
    # response DID NOT TEST
    data = []
    links = []

    # get request data.
    # _data = {'topic_id': '123', 'level': 2, 'limit': 3}
    _data = json.loads(request.get_data())

    # construct Cypher query
    _query = "MATCH (topic1:Topic {topic_id:$topic_id})-[r:RELATED*" + str(_data['level']) + ".." + str(
        _data['level']) + "]-(topic2:Topic) RETURN topic1,r,topic2 LIMIT $limit"

    # reorganize query result.
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    # extract event info
    topic = {'id': records[0][0].id, 'name': records[0][0].get('name'), 'count': records[0][0].get('count'),
             'time': records[0][0].get('time').iso_format(), 'category': CATEGORY_TOPIC}
    data.append(topic)
    # reorganize query result. like:

    for r in records:
        link = {'source': str(topic['id']), 'target': str(r[2].id),'level': _data['level'], 'category': 'RELATED'}
        topics = {'id': r[2].id, 'name': r[2].get('name'), 'count': r[2].get('count'),
                  'time': r[2].get('time').iso_format(), 'category': CATEGORY_TOPIC}

        links.append(link)
        if data.count(topics) == 0: data.append(topics)

    if _data['level'] == 1:
        for i in range(0, len(links)):
            links[i]['PMI'] = records[i][1][0].get('PMI')

    # return Json data
    response = [data, links]
    return Response(json.dumps(response), mimetype="application/json")


@api.route('/topic/list', methods=['GET', 'POST'])
def topic_list():
    # function: return a list of events send to web front
    # response
    data = []

    # get request data.
    _data = json.loads(request.get_data())
    # _data = request.get_data()

    # eg.
    # _data = {'name': '#An'}
    # construct Cypher query
    _query = "MATCH (topic:Topic) WHERE topic.name CONTAINS $name " \
             "RETURN topic LIMIT 10"

    # reorganize query result. like:
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    for record in records:
        topic = {'topic_id': record[0].get('topic_id'), 'name': record[0].get('name')}
        data.append(topic)

    # return Json data
    response = [data]
    return Response(json.dumps(response), mimetype="application/json")
