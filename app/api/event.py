from . import api
from .. import neo4j_db
from flask import render_template, session, redirect, url_for
from flask import Flask, g, Response, request
# from ..models import neo4j_session
import json


@api.route('/event/user', methods=['GET', 'POST'])
def event_user():
    # function: find a group of user who participated given event
    # response
    data = []
    links = []

    # get request data.
    # eg. {'event_id': 123, 's_time': '2019-12-20T15:29', 'e_time': '2019-12-30T17:30'}
    _data = {'event_id': 61, 's_time': '2009-07-20T15:29', 'e_time': '2020-12-30T17:30'}
    # construct Cypher query
    _query = "MATCH (user:User)-[relationship:PARTICIPATE]->(event:Event {event_id: $event_id}) " \
             "WHERE datetime($s_time) <= relationship.time <= datetime($e_time) " \
             "RETURN event, relationship, user"

    # reorganize query result. like:
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    # extract event info
    event = {'id': records[0][0].id, 'name': records[0][0].get('name')}
    data.append(event)

    # extract user, relationship info
    for record in records:
        link = {'id': record[1].id, 'source': record[1].start_node.id, 'target': record[1].end_node.id,
                'type': record[1].get('type'), 'time': record[1].get('time').iso_format()}
        user = {'id': record[2].id, 'name': record[2].get('name'), 'value': record[2].get('unique_id')}

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
    # eg. {'event_id': 123, 's_time': '2019-12-20T15:29', 'e_time': '2019-12-30T17:30'}
    _data = {'event_id': 61, 's_time': '2019-12-20T15:29', 'e_time': '2020-12-30T17:30'}
    # construct Cypher query
    _query = "MATCH (event:Event {event_id: $event_id})-[relationship:Produce]->(topic:Topic) " \
             "WHERE datetime($s_time) <= relationship.time <= datetime($e_time) " \
             "RETURN event, relationship, topic"

    # reorganize query result.
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    # extract event info
    event = {'id': records[0][0].id, 'name': records[0][0].get('name')}
    data.append(event)

    # extract topic, relationship info
    for record in records:
        link = {'id': record[1].id, 'source': record[1].start_node.id, 'target': record[1].end_node.id,
                'time': record[1].get('time').iso_format()}
        topic = {'id': record[2].id, 'name': record[2].get('topic_name')}

        links.append(link)
        if data.count(topic) == 0: data.append(topic)

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
    # eg. {'event_id': 123}
    _data = {'event_id': 123}
    # construct Cypher query
    _query = "MATCH (event:Event {event_id: $event_id})-[relationship:Produce]->(topic:Topic) " \
             "RETURN event, relationship, topic"

    # reorganize query result. like:
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    # extract event info
    event = {'id': records[0][0].id, 'name': records[0][0].get('name')}
    data.append(event)

    # extract topic
    # how to organize topic? a table?

    # return Json data
    response = [data, links]
    return Response(json.dumps(response), mimetype="application/json")


@api.route('/event/info', methods=['GET', 'POST'])
def event_neighbor():
    # response
    data = []
    links = []

    # get request data.
    # eg. {'event_id': 123, 'level': 2}
    _data = {'event_id': 123, 'level': 2}
    # construct Cypher query

    # reorganize query result. like:

    # return Json data
    response = [data, links]
    return Response(json.dumps(response), mimetype="application/json")


@api.route('/event/list', methods=['GET', 'POST'])
def event_list():
    # function: return a list of events send to web front
    # response
    data = []

    # get request data.
    _data = json.loads(request.get_data())
    # _data = request.get_data()
    # data.append(_data)
    # data.append(request.mimetype)
    print(_data)
    print(request.mimetype)
    # return Response(data)

    # eg.
    # _data = {'name': '#An'}
    # construct Cypher query
    _query = "MATCH (event:Event) WHERE event.name STARTS WITH $name " \
             "RETURN event LIMIT 20"

    # reorganize query result. like:
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    for record in records:
        event = {'event_id': record[0].get('event_id'), 'name': record[0].get('name')}
        data.append(event)

    # return Json data
    response = [data]
    return Response(json.dumps(response), mimetype="application/json")
