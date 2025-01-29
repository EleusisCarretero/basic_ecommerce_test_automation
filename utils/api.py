"""
API MongoDB manager file
"""
from flask import Flask, jsonify, request
from pymongo import MongoClient
import argparse


class APIMongoDB:
    """
    API MongoDB class manager

    Attributes:
        app(Flask): Flask instance
        mongo_uri(str): mongo db uri
        db_name(str): data base name
        collection_name(str): collection name
    """
    def __init__(self, app, mongo_uri, db_name, collection_name):
        self.app = app
        self.mongo_uri = mongo_uri
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.add_routes()
    
    def add_routes(self):
        """Register API routs"""
        self.app.add_url_rule("/", view_func=self.home)
        self.app.add_url_rule("/users", view_func=self.get_users, methods=["GET"])
        self.app.add_url_rule("/add_user", view_func=self.add_user, methods=["POST"])

    def home(self):
        """
        Returns API message
        """
        return jsonify({"message": "API Flask with MongoDB"})

    def get_users(self):
        """
        GET method
        """
        users = list(self.collection.find({}, {"_id": 0}))  # Excluye _id
        return jsonify(users)

    def add_user(self):
        """
        POST method
        """
        data = request.json
        self.collection.insert_one(data)
        return jsonify({"message": "User successfully added"}), 201


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument("-m", "--mongo_uri", help="The MongoDB URI", default="mongodb+srv://eleusiscarretero:J8nKfYYIuPa0XcJB@cluster0.73nlx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    parser.add_argument("-d", "--db_name",  help="The Name of the desired database", default="users_data")
    parser.add_argument("-c", "--collection_name",  help="The Name of the desired collection", default="users")
    args = parser.parse_args()
    app = Flask(__name__)
    md_db = APIMongoDB(app,args.mongo_uri, args.db_name, args.collection_name)
    app.run(debug=True)
