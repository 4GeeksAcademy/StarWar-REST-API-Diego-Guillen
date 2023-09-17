"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Starships

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace(
        "postgres://", "postgresql://"
    )
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)


# GET Methods
@app.route("/users", methods=["GET"])
def users_get():
    user_list = User.query.all()
    # response_body = user_list;
    response_body = [{"username": str(user)} for user in user_list]
    return jsonify(response_body), 200


@app.route("/users/favorites", methods=["GET"])
def favorites_get():
    response_body = {"msg": "Hello, this is your GET /user/favorites/ response "}

    return jsonify(response_body), 200


@app.route("/users/favorites/<username>", methods=["GET"])
def favorites_get_username(username):
    response_body = {
        "msg": f"Hello, this is your GET /user/favorites/{username} response "
    }

    return jsonify(response_body), 200


@app.route("/people", methods=["GET"])
def people_get():
    response_body = {"msg": "Hello, this is your GET /people response "}
    return jsonify(response_body), 200


@app.route("/people/<int:person_id>", methods=["GET"])
def person_get(person_id):
    response_body = {"msg": f"Hello, this is your GET /people/{person_id} response "}
    return jsonify(response_body), 200


@app.route("/planets", methods=["GET"])
def planets_get():
    response_body = {"msg": "Hello, this is your GET /planets response "}
    return jsonify(response_body), 200


@app.route("/planets/<int:planet_id>", methods=["GET"])
def planet_get(planet_id):
    response_body = {"msg": f"Hello, this is your GET /people/{planet_id} response "}
    return jsonify(response_body), 200


@app.route("/starships", methods=["GET"])
def starships_get():
    response_body = {"msg": "Hello, this is your GET /planets response "}
    print("Hello")
    return jsonify(response_body), 200


@app.route("/starships/<int:starship_id>", methods=["GET"])
def starship_get(starship_id):
    response_body = {
        "msg": f"Hello, this is your GET /starships/{starship_id} response "
    }
    return jsonify(response_body), 200


# POST Methods
@app.route("/users/favorites/planets/<int:planet_id>", methods=["POST"])
def add_planets():
    response_body = request.get_json()
    # data = request.json
    # planet = Planets(
    #     name=data["name"],
    #     rotation_period=data["rotation_period"],
    #     orbital_period=data["orbital_period"],
    #     diameter=data["diameter"],
    #     climate=data["climate"],
    #     gravity=data["gravity"],
    #     terrain=data["terrain"],
    #     population=data["population"],
    # )
    # db.session.add(planet)
    # db.session.commit()
    # return {"message": f"planet {planet.name} has been created successfully."}
    return jsonify(response_body), 200


@app.route("/users/people/<int:people_id>", methods=["POST"])
def add_people():
    response_body = request.get_json()


@app.route("/users/startships/<int:startship_id>", methods=["POST"])
def add_startships():
    response_body = request.get_json()

    return jsonify(response_body), 200


# DELETE Methods
@app.route("/planet/<int:position>", methods=["DELETE"])
def delete_planet(position):
    print("delete planets in position " + position)
    return jsonify(position)


@app.route("/people/<int:position>", methods=["DELETE"])
def delete_person(position):
    print("delete people in position " + position)
    return jsonify(position)


@app.route("/startships/<int:position>", methods=["DELETE"])
def delete_startship(position):
    print("delete starships in position " + position)
    return jsonify(position)


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
