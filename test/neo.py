from neo4j import GraphDatabase, basic_auth
from neo4j.time import DateTime
import time
from datetime import datetime

# query0 = "match p=(u:User {user_id:322})-[r:PARTICIPATE]-(e:Event) return u,r,e limit 2"
# query1 = "match p=(u:User {user_id:322})-[r:PARTICIPATE]-(e:Event) return r"
# query2 = "match p=(u:User {user_id:322})-[r:PARTICIPATE]-(e:Event) with collect([u.unique_id, u.name]) as u, collect([e.event_name]) as e, r as r return u,r,e"
#
# driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "neo4J"))
# session = driver.session(database="twitter")

# # original query1 consume:4.842575311660767
# s = time.time()
# for i in range(0,200):
#     r = session.run(query1)
# e = time.time()
# print(f"original query1 consume:{e-s}")
#
# # original query2 consume:5.379350423812866
# e1= time.time()
# for i in range(0,200):
#     r = session.run(query2)
# e2 = time.time()
# print(f"original query2 consume:{e2-e1}")

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "neo4J"))
dbsession = driver.session(database="twitter")

data = {'user_id': 322, 's_time': '2010-09-28T00:29', 'e_time': '2019-09-28T02:30'}

_query = "MATCH (user:User {user_id: $user_id})-[relationship:PARTICIPATE]->(event:Event) " \
         "WHERE datetime($s_time) <= relationship.time <= datetime($e_time)" \
         "RETURN user, relationship, event"
_data = {'user_id': data['user_id'], 's_time': data['s_time'], 'e_time': data['e_time']}

# _query = "MATCH (user:User {user_id: $user_id})-[relationship:PARTICIPATE]->(event:Event) " \
#          "WHERE $s_time <= relationship.time <= $e_time " \
#          "RETURN user, relationship, event"
# _data = {'user_id': data['user_id'],
#          's_time': DateTime(year=int(data['e_time'][0:4]), month=int(data['e_time'][5:7]), day=int(data['e_time'][8:10]),
#                             hour=int(data['e_time'][11:13]), minute=int(data['e_time'][14:16])),
#          'e_time': DateTime(year=int(data['e_time'][0:4]), month=int(data['e_time'][5:7]), day=int(data['e_time'][8:10]),
#                             hour=int(data['e_time'][11:13]), minute=int(data['e_time'][14:16]))}

r = dbsession.run(_query, parameters=_data)

r = r.values()
for i in r:
    print(i)
