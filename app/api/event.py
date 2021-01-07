from . import api
from app.models import neo4j_db
from flask import render_template, session, redirect, url_for
from flask import Flask, g, Response, request
# from ..models import neo4j_session
import json

CATEGORY_EVENT = 0
CATEGORY_USER = 1
CATEGORY_TOPIC = 2


@api.route('/event/user', methods=['GET', 'POST'])
def event_user():
    # function: find a group of user who participated given event
    # response
    data = []
    links = []

    # get request data.
    # _data = {"event_id": "61", "s_time": "2009-07-20T15:29", "e_time": "2020-12-30T17:30"}
    _data = json.loads(request.get_data())

    # construct Cypher query
    _query = "MATCH (user:User)-[relationship:PARTICIPATE]->(event:Event {event_id: $event_id}) " \
             "WHERE datetime($s_time) <= relationship.time <= datetime($e_time) " \
             "RETURN event, relationship, user " \
             "LIMIT 400"

    # reorganize query result. like:
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    # extract event info
    event = {'id': records[0][0].id, 'name': records[0][0].get('name'), 'category': CATEGORY_EVENT}
    data.append(event)

    # extract user, relationship info
    for r in records:
        link = {'id': r[1].id, 'source': str(r[1].start_node.id), 'target': str(r[1].end_node.id),
                'type': r[1].get('type'), 'time': r[1].get('time').iso_format(), 'category': r[1].type}
        user = {'id': r[2].id, 'name': r[2].get('name'), 'value': r[2].get('unique_id'), 'category': CATEGORY_USER}

        links.append(link)
        if data.count(user) == 0: data.append(user)

    # return Json data
    response = [data, links]
    return Response(json.dumps(response), mimetype="application/json")


@api.route('/event/topic', methods=['GET', 'POST'])
def event_topic():
    # function: find topics which related to given event in specific time
    # response
    data = []
    links = []

    # get request data.
    # _data = {'event_id': '61', 's_time': '2019-09-20T15:29', 'e_time': '2020-12-30T17:30'}
    _data = json.loads(request.get_data())

    # construct Cypher query
    _query = "MATCH (event:Event {event_id: $event_id})-[relationship:PRODUCE]->(topic:Topic) " \
             "WHERE datetime($s_time) <= relationship.time <= datetime($e_time) " \
             "RETURN event, relationship, topic " \
             "LIMIT 400"

    # reorganize query result.
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    # extract event info
    event = {'id': records[0][0].id, 'name': records[0][0].get('name'), 'category': CATEGORY_EVENT}
    data.append(event)

    # extract topic, relationship info
    for r in records:
        link = {'id': r[1].id, 'source': str(r[1].start_node.id), 'target': str(r[1].end_node.id),
                'time': r[1].get('time').iso_format(), 'category': r[1].type}
        topic = {'id': r[2].id, 'name': r[2].get('name'), 'count': r[2].get('count'),
                 'time': r[2].get('time').iso_format(), 'category': CATEGORY_TOPIC}

        links.append(link)
        if data.count(topic) == 0: data.append(topic)

    # return Json data
    response = [data, links]
    return Response(json.dumps(response), mimetype="application/json")


@api.route('/event/neighbor', methods=['GET', 'POST'])
def event_neighbor():
    # response DID NOT TEST
    data = []
    links = []

    # get request data.
    # _data = {'event_id': '123', 'level': 2, 'limit': 3}
    _data = json.loads(request.get_data())

    # construct Cypher query
    _query = "MATCH (event1:Event {event_id:$event_id})-[r:COOCCURENCE*" + str(_data['level']) + ".." + str(
        _data['level']) + "]-(event2:Event) RETURN event1,r,event2 LIMIT $limit"

    # reorganize query result.
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    # extract event info
    event = {'id': records[0][0].id, 'name': records[0][0].get('name'), 'category': CATEGORY_EVENT}
    data.append(event)
    # reorganize query result. like:
    for r in records:
        link = {'source': str(event['id']), 'target': str(r[2].id), 'category': 'COOCCURENCE'}
        events = {'id': r[2].id, 'name': r[2].get('name'), 'category': CATEGORY_EVENT}

        links.append(link)
        if data.count(events) == 0: data.append(events)

    # return Json data
    response = [data, links]
    return Response(json.dumps(response), mimetype="application/json")


@api.route('/event/info', methods=['GET', 'POST'])
def event_info():
    # function: find top N topic related to given event
    # response
    data = []
    links = []

    # get request data.
    # _data = {'event_id': '5', 'limit': 20, 'e_time': '2019-09-29T15:29'}
    _data = json.loads(request.get_data())

    # construct Cypher query
    _query = "MATCH (event:Event {event_id: $event_id})-[relationship:PRODUCE]->(topic:Topic) " \
             "WHERE relationship.time <= datetime($e_time) " \
             "WITH topic.name as name, sum(topic.count) as count, max(topic.time) as time " \
             "RETURN name, count, time " \
             "ORDER BY count DESC " \
             "LIMIT $limit "

    # reorganize query result. like:
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    # extract event info
    # event = {'id': records[0][0].id, 'name': records[0][0].get('name')}
    # data.append(event)

    # extract topic
    # return a table
    for r in records:
        topic = {'name': r[0], 'count': r[1],
                 'time': r[2].iso_format(), 'category': CATEGORY_TOPIC}
        data.append(topic)

    # return Json data
    response = [data]
    return Response(json.dumps(response), mimetype="application/json")


@api.route('/event/list', methods=['GET', 'POST'])
def event_list():
    # function: return a list of events send to web front
    # response
    data = []

    # get request data.
    _data = json.loads(request.get_data())
    # _data = request.get_data()

    # eg.
    # _data = {'name': '#An'}
    # construct Cypher query
    _query = "MATCH (event:Event) WHERE event.name CONTAINS $name " \
             "RETURN event LIMIT 10"

    # reorganize query result. like:
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    for record in records:
        event = {'event_id': record[0].get('event_id'), 'name': record[0].get('name')}
        data.append(event)

    # return Json data
    response = [data]
    return Response(json.dumps(response), mimetype="application/json")
