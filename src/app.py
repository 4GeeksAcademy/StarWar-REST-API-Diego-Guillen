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
from models import db, User, People, Planets, Starships, Favorites

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
    response_body = [user.serialize() for user in user_list]
    return response_body, 200


@app.route("/users/favorites", methods=["GET"])
def favorites_get():
    #response_body = {"msg": "Hello, this is your GET /user/favorites/ response "}
    try:
        favorites = Favorites.query.all()
        response_body = [favorite.serialize() for favorite in favorites]
        return response_body, 200
    except Exception as error:
        return jsonify({"message": str(error)}), 400   


@app.route("/users/favorites/<username>", methods=["GET"])
def favorites_get_username(username):
    # response_body = {
    #     "msg": f"Hello, this is your GET /user/favorites/{username} response "
    # }
    try:
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {"message": f"user {username} doesn't exist."}, 400
        favorites = Favorites.query.filter_by(user=user).first()
        response_body = favorites.serialize()
        return response_body, 200
    except Exception as error:
        return jsonify({"message": str(error)}), 400    

@app.route("/people", methods=["GET"])
def people_get():
    #response_body = {"msg": "Hello, this is your GET /people response "}
    try:
        people = People.query.all()
        response_body = [person.serialize() for person in people]
        return response_body, 200
    except Exception as error:
        return jsonify({"message": str(error)}), 400


@app.route("/people/<int:person_id>", methods=["GET"])
def person_get(person_id):
    #response_body = {"msg": f"Hello, this is your GET /people/{person_id} response "}
    try:
        person = People.query.filter_by(id=person_id).first()
        if person is None:
            return {"message": f"person {person_id} doesn't exist."}, 400
        response_body = person.serialize()
        return response_body, 200
    except Exception as error:
        return jsonify({"message": str(error)}), 400


@app.route("/planets", methods=["GET"])
def planets_get():
    #response_body = {"msg": "Hello, this is your GET /planets response "}
    try:
        planets = Planets.query.all()
        response_body = [planet.serialize() for planet in planets]
        return response_body, 200
    except Exception as error:
        return jsonify({"message": str(error)}), 400

@app.route("/planets/<int:planet_id>", methods=["GET"])
def planet_get(planet_id):
    #response_body = {"msg": f"Hello, this is your GET /people/{planet_id} response "}
    try:
        planet = Planets.query.filter_by(id=planet_id).first()
        if planet is None:
            return {"message": f"planet {planet_id} doesn't exist."}, 400
        response_body = planet.serialize()
        return response_body, 200
    except Exception as error:
        return jsonify({"message": str(error)}), 400


@app.route("/starships", methods=["GET"])
def starships_get():
    #response_body = {"msg": "Hello, this is your GET /planets response "}
    try:
        starships = Starships.query.all()
        response_body = [starship.serialize() for starship in starships]
        return response_body, 200
    except Exception as error:
        return jsonify({"message": str(error)}), 400


@app.route("/starships/<int:starship_id>", methods=["GET"])
def starship_get(starship_id):
    # response_body = {"msg": f"Hello, this is your GET /starships/{starship_id} response "}
    try:
        starship = Starships.query.filter_by(id=starship_id).first()
        if starship is None:
            return {"message": f"starship {starship_id} doesn't exist."}, 400
        response_body = starship.serialize()
        return response_body, 200
    except Exception as error:
        return jsonify({"message": str(error)}), 400


# POST Methods
@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    if data is None:
        return {"message": "The request body is null"}, 400
    if data["username"] is None:
        return {"message": "The request body is missing the username"}, 400
    if data["password"] is None:
        return {"message": "The request body is missing the password"}, 400
    if data["firstname"] is None:
        return {"message": "The request body is missing the firstname"}, 400
    if data["lastname"] is None:
        return {"message": "The request body is missing the lastname"}, 400
    if data["email"] is None:
        return {"message": "The request body is missing the email"}, 400  
    if User.query.filter_by(username=data["username"]).first() is not None:
        return {"message": f"user {data['username']} already exists."}, 400
    try:
        user = User(
            username=data["username"],
            password=data["password"],
            firstname=data["firstname"],
            lastname=data["lastname"],
            email=data["email"],
            is_active=True,
        )
        db.session.add(user)
        db.session.commit()
        return {"message": f"user {user.username} has been created successfully."}, 200
    except Exception as error:
        return {"message": f"user {user.username} has not been created successfully."}, 400  
    
   

@app.route("/users/favorites/planets/<int:planet_id>", methods=["POST"])
def add_planets(planet_id):
    body = request.get_json()
    username = request.json.get("username", None)
    planet_body = body.get("planet_id", [])    
    user_list = User.query.filter_by(username=username).first()
    if user_list is None:
        return {"message": f"user {username} doesn't exist."}, 400
    for x in planet_body:
        planet_list = Planets.query.filter_by(id=x).first()
        if planet_list is None:
            return {"message": f"planet {x} doesn't exist."}, 400     
   
    current_favorite = Favorites.query.filter_by(user=user_list).first()     
    for x in planet_body:
        current_favorite.planets.append(Planets.query.filter_by(id=x).first())       
    try:
        #db.session.add(favorite)  
        db.session.commit()
        return {"message": f"planet {current_favorite.planets} has been added successfully."}, 200
    except Exception as error:
        return {"message": f"planet {current_favorite.planets} has not been added successfully."}, 400
    


@app.route("/users/favorites/people/<int:people_id>", methods=["POST"])
def add_people(people_id):
    body = request.get_json()
    username = request.json.get("username", None)
    people_body = body.get("people_id", [])    
    user_list = User.query.filter_by(username=username).first()
    if user_list is None:
        return {"message": f"user {username} doesn't exist."}, 400
    for x in people_body:
        people_list = People.query.filter_by(id=x).first()
        if people_list is None:
            return {"message": f"planet {x} doesn't exist."}, 400     
   
    current_favorite = Favorites.query.filter_by(user=user_list).first()     
    for x in people_body:
        current_favorite.people.append(People.query.filter_by(id=x).first())  
    #return {"message": f"people {current_favorite.people} has been added successfully."}, 200
    #return jsonify(current_favorite.serialize()), 200     
    try:
        #db.session.add(favorite)  
        db.session.commit()
        return {"message": f"people {current_favorite.people} has been added successfully."}, 200
    except Exception as error:
        return {"message": f"people {current_favorite.people} has not been added successfully."}, 400


@app.route("/users/favorites/starships/<int:starship_id>", methods=["POST"])
def add_starships(starship_id):
    body = request.get_json()
    username = request.json.get("username", None)
    starships_body = body.get("starship_id", [])    
    user_list = User.query.filter_by(username=username).first()
    if user_list is None:
        return {"message": f"user {username} doesn't exist."}, 400
    for x in starships_body:
        starships_list = Starships.query.filter_by(id=x).first()
        if starships_list is None:
            return {"message": f"Starship {x} doesn't exist."}, 400     
   
    current_favorite = Favorites.query.filter_by(user=user_list).first()     
    for x in starships_body:
        current_favorite.starships.append(Starships.query.filter_by(id=x).first())  
    #return {"message": f"starships {starships_body} has been added successfully."}, 200
    #return jsonify(current_favorite.serialize()), 200     
    try:
        #db.session.add(favorite)  
        db.session.commit()
        return {"message": f"startships {current_favorite.starships} has been added successfully."}, 200
    except Exception as error:
        return {"message": f"startships {current_favorite.starships} has not been added successfully."}, 400


# DELETE Methods
@app.route("/planet/<int:planet_id>", methods=["DELETE"])
def delete_planet(position):
    print("delete planets in position " + position)
    return jsonify(position)


@app.route("/people/<int:people_id>", methods=["DELETE"])
def delete_person(position):
    print("delete people in position " + position)
    return jsonify(position)


@app.route("/startships/<int:starships_id>", methods=["DELETE"])
def delete_startship(position):
    print("delete starships in position " + position)
    return jsonify(position)


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
