from . import api
from .. import neo4j_db
from flask import render_template, session, redirect, url_for
from flask import Flask, g, Response, request
# from ..models import neo4j_session
import json


@api.route('/user/event', methods=['GET', 'POST'])
def user_event():
    # func: find events that specific user participated in specific time
    # response
    # users = []
    # events = []
    data = []
    links = []

    # receive request data.
    # _data = {"user_id": 322, "s_time": "2019-09-28T00:29", "e_time": "2019-09-28T02:30"}
    _data = json.loads(request.get_data())

    # construct Cypher query
    _query = "MATCH (user:User {user_id: $user_id})-[relationship:PARTICIPATE]->(event:Event) " \
             "WHERE datetime($s_time) <= relationship.time <= datetime($e_time) " \
             "RETURN user, relationship, event"

    # reorganize query result.
    result = neo4j_db.session.run(_query, parameters=_data)

    # result.values() return list of records from result
    records = result.values()

    # extract user node, which needs only one
    user = {'id': records[0][0].id, 'name': records[0][0].get('name'), 'value': records[0][0].get('unique_id')}
    data.append(user)

    # extract relationship and events
    for record in records:
        link = {'id': record[1].id, 'source': record[1].start_node.id, 'target': record[1].end_node.id,
                'type': record[1].get('type'), 'time': record[1].get('time').iso_format()}
        event = {'id': record[2].id, 'name': record[2].get('name')}

        links.append(link)
        if data.count(event) == 0: data.append(event)

    # response = [users, links, events]
    response = [data, links]
    return Response(json.dumps(response), mimetype="application/json")


@api.route('/user/neighbor', methods=['GET', 'POST'])
def user_neighbor():
    # func: find N level neighbor with specific user
    # response
    data = []
    links = []

    # receive request data
    # _data = {'user_id': 322, 'level': 2}
    _data = json.loads(request.get_data())

    # construct Cypher query

    _query = "MATCH (user:User {user_id: $user_id})-[relationship:Join]->(user:User)"

    # reorganize results

    # return Json data

    return


@api.route('/user/info', methods=['GET', 'POST'])
def user_info():
    # func: find top N topic that specific user
    # response
    data = []
    links = []

    # receive request data
    # _data = {'user_id': 322, 'time': '2020-12-30T20:20'}
    _data = json.loads(request.get_data())

    # construct Cypher query
    # count topic times or not?
    _query = "MATCH (user:User {user_id: $user_id}-[relationship:Join]->(topic:Topic) " \
             "WHERE relationship.time <= datetime($time) " \
             "RETURN user, relationship, topic "

    # reorganize results, user topic linksone
    result = neo4j_db.session.run(_query, _data)
    records = result.values()

    # extract user node, which needs only
    user = {'id': records[0][0].id, 'name': records[0][0].get('name'), 'value': records[0][0].get('unique_id')}
    data.append(user)

    # how to organize topic? one or both?
    # 1. a table, with topic name, times. Need count the number of each topic
    # 2. a time line, with time line and node represent each topic. Need count when same topic present as one time

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
    _query = "MATCH (user:User) WHERE user.name STARTS WITH $name " \
             "RETURN user ORDER BY user.name ASC LIMIT 20"

    # reorganize results
    result = neo4j_db.session.run(_query, parameters=_data)
    records = result.values()

    for record in records:
        user = {'name': record[0].get('name'), 'user_id': record[0].get('user_id')}
        data.append(user)

    # return Json data
    response = data
    return Response(json.dumps(response), mimetype="application/json")
