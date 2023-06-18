from elasticsearch import Elasticsearch
import json

ELASTIC_PASSWORD = "your_elastic_password"

client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", ELASTIC_PASSWORD),
    verify_certs=False,
)

indexName = "gastronomical"
client.indices.create(index=indexName)

# location of recipe json file: change this to match your own setup!
file_name = 'your_path_to_recipe_json_file'

#Create document mapping

recipeMapping = {
    'properties': {
        'name': {'type': 'text'},
        'ingredients': {'type': 'text'}
    },
}

client.indices.put_mapping(index=indexName, body=recipeMapping)

#Load Json file
with open(file_name) as data_file:
    recipeData = json.load(data_file)

#Index the recipes
for recipe in recipeData:
    # print(recipe.keys())
    # print(recipe['_id'].keys())
    client.index(index=indexName, id=recipe['_id']['$oid'], document={"name": recipe['name'], "ingredients": recipe['ingredients']})
