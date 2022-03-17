from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId
app=Flask(__name__)

try:
    mongo= pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.company
    mongo.server_info()
except:
    print("Cannot connect to database")


@app.route("/users", methods=["POST"])
def create_user():
    try:
        user={
            "first_name":request.form["firstname"], 
            "last_name":request.form["lastname"]
            }
        dbResponse = db.users.insert_one(user)
        return Response(
            response=json.dumps
            (
                {"Message":"User Created",
                 "id": f"{dbResponse.inserted_id}"}
            ),
            status=200,
            mimetype="application/json"  
        )
    except Exception as e:
        print(e)

@app.route("/users", methods=["GET"])
def create_some_user():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response=json.dumps
            (
                {"Message":"Data is sent from sever",
                 "id": data
                }
            ),
            status=500,
            mimetype="application/json"  
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps
            (
                {"Message":"Cannot connect to User"}
            ),
            status=500,
            mimetype="application/json"  
        )
@app.route("/users/<id>", methods=["PATCH"])
def update_users(id):
    try:
        print("Hello world")
        dbResponse= db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"first_name":request.form["first_name"]}}
        )
        if dbResponse.modified_count == 1:
            return Response(
                response=json.dumps
                (
                    {"Message":"User has been updated"}
                ),
                status=500,
                mimetype="application/json"  
            )
        else:
            return Response(
                response=json.dumps
                (
                    {"Message":"Nothing to update"}
                ),
                status=500,
                mimetype="application/json"  
            )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps
            (
                {"Message":"Cannot able to update the data"}
            ),
            status=501,
            mimetype="application/json"  
        )

@app.route("/users/<id>", methods=["DELETE"])
def delete_users(id):
    try:
        dbResponse= db.users.delete_one({"_id":id})
        if dbResponse.deleted_count == 1:
            return Response(
                    response=json.dumps
                    (
                        {"Message":"Delete successfully"}
                    ),
                    status=200,
                    mimetype="application/json"  
                )
        return Response(
                    response=json.dumps
                    (
                        {"Message":"Users {} is not available in database".format(id)}
                    ),
                    status=200,
                    mimetype="application/json"  
        )
    except Exception as ex:
        print(ex)
        return Response(
                response=json.dumps
                (
                    {"Message":"Unable to delete"}
                ),
                status=501,
                mimetype="application/json"  
            )
    #db.inventory.deleteOne(    { "status": "D" } // specifies the document to delete

if __name__ == "__main__":
    app.run(debug=True)