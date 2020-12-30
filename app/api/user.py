from . import api
from .. import neo4j_db
from flask import render_template, session, redirect, url_for
from flask import Flask, g, Response, request
# from ..models import neo4j_session
import json

CATEGORY_EVENT = 0
CATEGORY_USER = 1
CATEGORY_TOPIC = 2


@api.route('/user/event', methods=['GET', 'POST'])
def user_event():
    # func: find events that specific user participated in specific time
    # response
    # users = []
    # events = []
    data = []
    links = []

    # receive request data.
    # _data = {"user_id": '322', "s_time": "2019-09-28T00:29", "e_time": "2019-09-28T02:30"}
    _data = json.loads(request.get_data())

    # construct Cypher query
    _query = "MATCH (user:User {user_id: $user_id})-[relationship:PARTICIPATE]->(event:Event) " \
             "WHERE datetime($s_time) <= relationship.time <= datetime($e_time) " \
             "RETURN user, relationship, event " \
             "LIMIT 400"

    # reorganize query result.
    result = neo4j_db.session.run(_query, parameters=_data)

    # result.values() return list of records from result
    records = result.values()

    # extract user node, which needs only one
    user = {'id': records[0][0].id, 'name': records[0][0].get('name'), 'value': records[0][0].get('unique_id'),
            'category': CATEGORY_USER}
    data.append(user)

    # extract relationship and events
    for r in records:
        link = {'id': r[1].id, 'source': str(r[1].start_node.id), 'target': str(r[1].end_node.id),
                'type': r[1].get('type'), 'time': r[1].get('time').iso_format(), 'category': r[1].type}
        event = {'id': r[2].id, 'name': r[2].get('name'), 'category': CATEGORY_EVENT}

        links.append(link)
        if data.count(event) == 0: data.append(event)

    # response = [users, links, events]
    response = [data, links]
    return Response(json.dumps(response), mimetype="application/json")


@api.route('/user/topic', methods=['GET', 'POST'])
def user_topic():
    # function: find topics which related to given event in specific time
    # response
    data = []
    links = []

    # get request data.
    # _data = {'user_id': '61', 's_time': '2019-09-20T15:29', 'e_time': '2020-12-30T17:30'}
    _data = json.loads(request.get_data())

    # construct Cypher query
    _query = "MATCH (user:User {user_id: $user_id})-[relationship:JOIN]->(topic:Topic) " \
             "WHERE datetime($s_time) <= relationship.time <= datetime($e_time) " \
             "RETURN user, relationship, topic " \
             "LIMIT 400"

    # reorganize query result.
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    # extract event info
    user = {'id': records[0][0].id, 'name': records[0][0].get('name'), 'value': records[0][0].get('unique_id'),
            'category': CATEGORY_USER}
    data.append(user)

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



@api.route('/user/neighbor', methods=['GET', 'POST'])
def user_neighbor():
    # func: find N level neighbor with specific user
    # response
    data = []
    links = []

    # receive request data
    # _data = {'user_id': '322', 'level': 2}
    _data = json.loads(request.get_data())

    # construct Cypher query

    _query = "MATCH (user:User {user_id: $user_id})-[relationship:Join]->(user:User)"
    _query = "MATCH (user1:User {user_id: $user_id})-[r:INTERACT*" + str(_data['level']) + ".." + str(
        _data['level']) + "]-(user2:User) RETURN user1,r,user2 LIMIT $limit"

    # reorganize results
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    # return Json data
    # extract event info
    user = {'id': records[0][0].id, 'name': records[0][0].get('name'), 'unique_id': records[0][0].get('unique_id'),
            'category': CATEGORY_USER}
    data.append(user)
    # reorganize query result. like:
    for r in records:
        link = {'source': str(user['id']), 'target': str(r[2].id), 'category': 'INTERACT'}
        users = {'id': r[2].id, 'name': r[2].get('name'), 'unique_id': r[2].get('unique_id'), 'category': CATEGORY_USER}

        links.append(link)
        if data.count(users) == 0: data.append(users)

    # return Json data
    response = [data, links]
    return Response(json.dumps(response), mimetype="application/json")

    return


@api.route('/user/info', methods=['GET', 'POST'])
def user_info():
    # func: find top N topic that specific user
    # response
    data = []
    links = []

    # receive request data
    # _data = {'user_id': '322', 'time': '2020-12-30T20:20'}
    _data = json.loads(request.get_data())

    # construct Cypher query
    # count topic times or not?
    _query = "MATCH (user:User {user_id: $user_id})-[relationship:JOIN]->(topic:Topic) " \
             "WHERE relationship.time <= datetime($e_time) " \
             "WITH topic.name as name, sum(topic.count) as count, max(topic.time) as time " \
             "RETURN name, count, time " \
             "ORDER BY count DESC " \
             "LIMIT $limit "

    # reorganize results, user topic linksone
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    # extract user node, which needs only
    # user = {'id': records[0][0].id, 'name': records[0][0].get('name'), 'value': records[0][0].get('unique_id')}
    # data.append(user)

    # how to organize topic? one or both?
    # 1. a table, with topic name, times. Need count the number of each topic
    # 2. a time line, with time line and node represent each topic. Need count when same topic present as one time
    for r in records:
        topic = {'name': r[0], 'count': r[1],
                 'time': r[2].iso_format(), 'category': CATEGORY_TOPIC}
        data.append(topic)

    # return Json data
    response = [data, links]
    return Response(json.dumps(response), mimetype="application/json")


@api.route('/user/list', methods=['GET', 'POST'])
def user_list():
    # func: find a group of user send to web input list
    # response
    data = []

    # receive request data
    # _data = {'name': 'a'}
    _data = json.loads(request.get_data())

    # construct Cypher query
    _query = "MATCH (user:User) WHERE user.name CONTAINS $name " \
             "RETURN user LIMIT 10"

    # reorganize results
    result = neo4j_db.session.run(_query, parameters=_data)
    records = result.values()

    for record in records:
        user = {'name': record[0].get('name'), 'user_id': record[0].get('user_id')}
        data.append(user)

    # return Json data
    response = data
    return Response(json.dumps(response), mimetype="application/json")
