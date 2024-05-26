from app import app, db
from flask import request, jsonify
from models import Person

# Gets all people
@app.route("/api/people", methods=["GET"])
def get_people():
    people = Person.query.all()
    result = [prsn.to_json() for prsn in people]
    return jsonify(result)

# Create a person
@app.route("/api/people", methods=["POST"])
def create_person():
    try:
        data = request.json

        required_fields = ["name", "role", "description", "gender"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error":f'Missing required field: {field}'}), 400

        name = data.get("name") # type: ignore
        role = data.get("role") # type: ignore
        description = data.get("description") # type: ignore
        gender = data.get("gender") # type: ignore

        # get avatar img based on their gender
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None

        new_person = Person(name=name, role=role, description=description, gender=gender, img_url=img_url) # type: ignore

        db.session.add(new_person)

        db.session.commit()

        return jsonify({"msg":"person created"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500    
            
# Delete a person
@app.route("/api/people/<int:id>", methods=["DELETE"])
def delete_person(id):
    try:
        person = Person.query.get(id)
        if person is None:
            return jsonify({"error":"Person not found"}), 404
        
        db.session.delete(person)
        db.session.commit()
        return jsonify({"msg":"Person deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500