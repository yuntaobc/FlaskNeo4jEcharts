from . import api
from flask import render_template, session, redirect, url_for
from flask import Flask, g, Response, request
# from ..models import neo4j_session
import json


@api.route('/topic/neighbor', methods=['GET', 'POST'])
def topic_neighbor():
    # response
    data = []
    links = []

    # get request data.
    # eg. {'event_id': 123, 'level': 2}
    _data = {'topic_id': 123, 'level': 2}
    # construct Cypher query

    # reorganize query result. like:

    # return Json data
    response = [data, links]
    return Response(json.dumps(response), mimetype="application/json")
