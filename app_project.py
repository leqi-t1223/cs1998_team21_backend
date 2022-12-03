import json
from db_project import db
from flask import Flask
from db_project import Location
from db_project import User
from db_project import Vendor
from flask import request


app = Flask(__name__)
db_filename = "studery.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


@app.route("/")
@app.route("/api/locations/")
def get_locations():
    """
    End point for getting locations
    """
    locations = [c.serialize() for c in Location.query.all()]
    return success_response({"locations": locations})


@app.route("/api/locations/", methods=["POST"])
def create_location():
    body = json.loads(request.data)
    x_coordinate = body.get("x_coordinate", None)
    y_coordinate = body.get("y_coordinate", None)
    name = body.get("name", None)
    if x_coordinate and y_coordinate and name is None:
        return failure_response("Name not provided", 400)
    new_location = Location(
        x_coordinate=body.get("x_coordinate"),
        y_coordinate=body.get("y_coordinate"),
        name=body.get("name")
    )
    db.session.add(new_location)
    db.session.commit()
    return success_response(new_location.serialize(), 201)


@app.route("/api/locations/<int:location_id>/")
def get_location(location_id):
    location = Location.query.filter_by(id=location_id).first()
    if location is None:
        return failure_response("Locatio not found!")
    return success_response(location.serialize())


@app.route("/api/locations/<int:location_id>/", methods=["DELETE"])
def delete_location(location_id):
    location = Location.query.filter_by(id=location_id).first()
    if location is None:
        return failure_response("location not found!")
    db.session.delete(location)
    db.session.commit()
    return success_response(location.serialize())


@app.route("/api/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    name = body.get("name", None)
    email = body.get("email", None)
    if name is None or email is None:
        return failure_response("Email or Name not provided", 400)
    new_user = User(
        name=body.get("name"),
        email=body.get("email")
    )
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.simple_serialize(), 201)


@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    return success_response(user.serialize())


@app.route("/api/locations/<int:location_id>/add/", methods=["POST"])
def add_user(location_id):
    location = Location.query.filter_by(id=location_id).first()
    if location is None:
        return failure_response("Location not found!")
    body = json.loads(request.data)
    user_id = body.get("user_id", None)
    if user_id is None:
        return failure_response("user_id not provided", 400)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    location.users.append(user)
    db.session.commit()
    return success_response(location.serialize())


@app.route("/api/locations/<int:location_id>/vendor/", methods=["POST"])
def create_vendor(location_id):
    location = Location.query.filter_by(id=location_id).first()
    if location is None:
        return failure_response("location not found!")
    body = json.loads(request.data)
    position = body.get("position", None)
    if position is None:
        return failure_response("position not provided", 400)
    new_vendor = Vendor(
        position=body.get("position"),
        location_id=location_id
    )
    db.session.add(new_vendor)
    db.session.commit()
    dic = new_vendor.simple_serialize()
    dic["location"] = location.simple_serialize()
    location.vendors.append(new_vendor)
    return success_response(dic, 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
