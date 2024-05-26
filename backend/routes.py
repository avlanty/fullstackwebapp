from app import app, db
from flask import request, jsonify
from models import Person

@app.route("/api/people", methods=["GET"])
def get_people():
    people = Person.query.all()
    result = [prsn.to_json() for prsn in people]
    return jsonify(result)