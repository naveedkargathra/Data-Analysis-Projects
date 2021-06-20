from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo

#Connect to Database
connection_url = "mongodb+srv://naveed_kargathra:ali2042015@cluster0.5mxjp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)

#Link to pre existing Database and Collection
db = client.get_database("Naveed_Python")
collection = db.Web_Scraping

# Create routes and define function to FIND record in Collection
@app.route('/find/', methods=['GET'])
def findAll():
    query = collection.find()
    output = {}
    i = 0
    for x in query:
        output[i] = x
        output[i].pop('_id')
        i += 1
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
