from neo4j import GraphDatabase, basic_auth

url = "bolt://localhost:7687"
username = "neo4j"
password = "neo4J"
database = "twitter"


class Neo4jSession():
    """docstring for ClassName"""
    def __init__(self):
        self.driver = GraphDatabase.driver(url, auth=basic_auth(username, password))
        self.session = self.driver.session(database=database)

    def get_session(self):
        return self.session


neo4j_db = Neo4jSession()

# TODO: define node model: event, user, topic?
#       in each model, define their cypher sentence
