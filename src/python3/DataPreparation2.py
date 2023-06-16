from elasticsearch import Elasticsearch
from py2neo import Graph, Node, Relationship, GraphService, NodeMatcher

ELASTIC_PASSWORD = "kLu+ajxWzhqye1z1dSlh"

client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", ELASTIC_PASSWORD),
    verify_certs=False,
)

indexName = "gastronomical"

# Graph database entity
graph_db = Graph("http://neo4j:neo4ja@localhost:7474/db/data/", user="neo4j", password="fruit-magnet-answer-shrink-serial-7884", name="neo4j")

filename = 'D:/Documents/giaoTrinh/nam_2/ki-3/nhap-mon-khoa-hoc-du-lieu/BTL-2-NMKHDL/src/python3/ingredients.txt'

ingredients = []

with open(filename) as f:
    for line in f:
        ingredients.append(line.strip())

ingredientnumber = 0
grandtotal = 0
matcher = NodeMatcher(graph_db)

for ingredient in ingredients:
    try:
        IngredientNode = matcher.match("Ingredient", Name=ingredient).first()
        if IngredientNode is None:
            IngredientNode = Node("Ingredient", Name=ingredient)
            graph_db.create(IngredientNode)
    except:
        continue

    ingredientnumber += 1
    searchbody = {
        "size": 10000,
        "query": {
            "match_phrase": {
                "ingredients": {
                    "query": ingredient,
                }
            }
        }
    }

    result = client.search(index=indexName, body=searchbody)

    # print(ingredient)
    # print(ingredientnumber)
    # print("Total: " + str(result['hits']['total']['value']))    
    grandtotal += result['hits']['total']['value']

    # print("Grand total: " + str(grandtotal))

    for recipe in result['hits']['hits']:
        try:
            RecipeNode = matcher.match("Recipe", Name=recipe['_source']['name']).first()
            if RecipeNode is None:
                RecipeNode = Node("Recipe", Name=recipe['_source']['name'])
                graph_db.create(RecipeNode)

            NodesRelationship = Relationship(RecipeNode, "Contains", IngredientNode)
            graph_db.merge(NodesRelationship)
            # print("added: " + recipe['_source']['name'] + " contains " + ingredient)
        except:
            continue

    # print("*************************************")
