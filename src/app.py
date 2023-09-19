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
import requests

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

@app.route("/filldatbase", methods=["POST"])
def fill_database():
    body_data = request.get_json()
    if body_data is None:
        return {"message": "body is empty"}, 400
    if body_data["start"] != "run" or body_data["page"] > 9 or body_data["api_name"] not in ["planets", "people", "starships"]:
        return {"message": "wrong parameter"}, 400
    r = requests.get(
        f"https://www.swapi.tech/api/{body_data['api_name']}?page={body_data['page']}&limit=10",
        headers={"Accept": "application/json"},
    )
    data = r.json()["results"]   
    object_data=[]
    urls = [url["url"] for url in data]
    for url in urls:
        object_data.append(requests.get(url).json()["result"])  
  
    #return jsonify(object_data), 200
    def insert_row_people(name, height, skin_color, hair_color, eye_color, birth_year, gender, home_world, description, starships):
        insert_people = People(
            name=name,
            height=height,
            skin_color=skin_color,
            hair_color=hair_color,
            eye_color=eye_color,
            birth_year=birth_year,
            gender=gender,
            home_world=home_world,
            description=description,
            starships=starships,
        )
        return insert_people
    def insert_row_planets(name, rotation_period, orbital_period, diameter, climate, gravity, terrain, population):
        insert_planets = Planets(
            name=name,
            rotation_period=rotation_period,
            orbital_period=orbital_period,
            diameter=diameter,
            climate=climate,
            gravity=gravity,
            terrain=terrain,
            population=population         
        )
        return insert_planets
    def insert_row_starships(name, model, manufacturer, length, max_atmosphering_speed, crew, passengers, starship_class):
        insert_starship = Starships(
            name=name,
            model=model,
            manufacturer=manufacturer,
            length=length,
            max_atmosphering_speed=max_atmosphering_speed,
            crew=crew,
            passengers=passengers,
            starship_class=starship_class         
        )
        return insert_starship
    objects = []
    if body_data["api_name"] == 'people':    
        objects = [insert_row_people(person["properties"]["name"],
                                    person["properties"]["height"],
                                    person["properties"]["skin_color"],
                                    person["properties"]["hair_color"],
                                    person["properties"]["eye_color"],
                                    person["properties"]["birth_year"],
                                    person["properties"]["gender"],
                                    person["properties"]["homeworld"],
                                    person["description"],
                                    starships="none") 
                                    for person in object_data]
    elif body_data["api_name"] == 'planets':
        objects = [insert_row_planets(planet["properties"]["name"],
                                    planet["properties"]["rotation_period"],
                                    planet["properties"]["orbital_period"],
                                    planet["properties"]["diameter"],
                                    planet["properties"]["climate"],
                                    planet["properties"]["gravity"],
                                    planet["properties"]["terrain"],
                                    planet["properties"]["population"])                             
                                    for planet in object_data]
    elif body_data["api_name"] == 'starships':
        objects = [insert_row_starships(starship["properties"]["name"],
                                    starship["properties"]["model"],
                                    starship["properties"]["manufacturer"],
                                    starship["properties"]["length"],
                                    starship["properties"]["max_atmosphering_speed"],
                                    starship["properties"]["crew"],
                                    starship["properties"]["passengers"],
                                    starship["properties"]["starship_class"])                            
                                    for starship in object_data]
        
    #return jsonify([object.serialize() for object in objects]),200
    try:

        db.session.add_all(objects)
        db.session.commit()
        return{"message": "data added to the DB successfully.}"}, 200
    
    except Exception as error:
        return {"message": f"unable to save into the DB, err = {error}"}, 400   


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
        favorite= Favorites(user=User.query.filter_by(username=data["username"]).first())
        favorite.people = []
        favorite.planets = []
        favorite.starships = []
        db.session.add(favorite)
        db.session.commit()
        return {"message": f"user {user.username} has been created successfully."}, 200
    except Exception as error:
        return {"message": f"user {user.username} has not been created successfully. err = {error}"}, 400  
    
   
@app.route("/users/favorites/", methods=["POST"])
def add_favorites():
    return {"message": "Hello, this is your POST /user/favorites/ response "}
    data = request.get_json()
    if data is None:
        return {"message": "The request body is null"}, 400
    if data["username"] is None:
        return {"message": "The request body is missing the username"}, 400
    if data["people_id"] is None:
        return {"message": "The request body is missing the people_id"}, 400
    if data["planet_id"] is None:
        return {"message": "The request body is missing the planet_id"}, 400
    if data["starship_id"] is None:
        return {"message": "The request body is missing the starship_id"}, 400
    if User.query.filter_by(username=data["username"]).first() is None:
        return {"message": f"user {data['username']} doesn't exist."}, 400    
    try:
        user = User.query.filter_by(username=data["username"]).first()
        #return {"message": f"user is {user}"}, 200
        favorites = Favorites(user=user)
        favorites.people = data["people_id"]
        favorites.planets = data["planet_id"]
        favorites.starships = data["starship_id"]
        db.session.add(favorites)
        db.session.commit()
        return {"message": f"favorite {favorites.id} has been created successfully."}, 200
    except Exception as error:
        return {"message": f"favorite {favorites.id} has not been created successfully."}, 400

@app.route("/users/favorites/planets/<int:planet_id>", methods=["POST"])
def add_planets(planet_id):    
    username = request.json.get("username", None)
    planet_body = planet_id #body.get("planet_id", [])    
    user = User.query.filter_by(username=username).first()
    if user is None:
        return {"message": f"user {username} doesn't exist."}, 400        
    planet = Planets.query.filter_by(id=planet_body).first()
    if planet is None:
        return {"message": f"planet {planet_body} doesn't exist."}, 400    
   
    current_favorite = Favorites.query.filter_by(user=user).first()     
   
    current_favorite.planets.append(Planets.query.filter_by(id=planet_body).first())  
    #return {"message": f"planet {planet} has been added successfully."}, 200    
    try:
        #db.session.add(favorite)  
        #return {"message": f"planet {current_favorite.planets} has been added successfully."}, 200
        db.session.commit()
        return {"message": f"planet {current_favorite.planets} has been added successfully."}, 200
    except Exception as error:
        return {"message": f"planet {current_favorite.planets} has not been added successfully. err = {error}"}, 400
    


@app.route("/users/favorites/people/<int:people_id>", methods=["POST"])
def add_people(people_id):
    username = request.json.get("username", None)
    people_body = people_id#body.get("people_id", [])    
    user_list = User.query.filter_by(username=username).first()
    if user_list is None:
        return {"message": f"user {username} doesn't exist."}, 400
    person = People.query.filter_by(id=people_body).first()
    if person is None:
        return {"message": f"people {people_body} doesn't exist."}, 400     
   
    current_favorite = Favorites.query.filter_by(user=user_list).first()     
   
    current_favorite.people.append(People.query.filter_by(id=people_body).first())  
    #return {"message": f"people {current_favorite.people} has been added successfully."}, 200
    #return jsonify(current_favorite.serialize()), 200     
    try:
        #db.session.add(favorite)  
        #return {"message": f"person {current_favorite.people} has been added successfully."}, 200
        db.session.commit()
        return {"message": f"people {current_favorite.people} has been added successfully."}, 200
    except Exception as error:
        return {"message": f"people {current_favorite.people} has not been added successfully. err = {error}"}, 400


@app.route("/users/favorites/starships/<int:starship_id>", methods=["POST"])
def add_starships(starship_id):
    body = request.get_json()
    username = request.json.get("username", None)
    starships_body = starship_id #body.get("starship_id", [])    
    user_list = User.query.filter_by(username=username).first()
    if user_list is None:
        return {"message": f"user {username} doesn't exist."}, 400
    starship = Starships.query.filter_by(id=starships_body).first()
    if starship is None:
        return {"message": f"starship {starships_body} doesn't exist."}, 400     
   
    current_favorite = Favorites.query.filter_by(user=user_list).first()     
    
    current_favorite.starships.append(Starships.query.filter_by(id=starships_body).first())  
    #return {"message": f"starships {starship} has been added successfully."}, 200
    #return jsonify(current_favorite.serialize()), 200     
    try:
        #db.session.add(favorite)  
        db.session.commit()
        return {"message": f"startships {current_favorite.starships} has been added successfully."}, 200
    except Exception as error:
        return {"message": f"startships {current_favorite.starships} has not been added successfully. err = {error}"}, 400


# DELETE Methods

@app.route("/planets/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    username = request.json.get("username", None)
    user = User.query.filter_by(username=username).first()
    if username is None:
        return {"message": "The request body is missing the username"}, 400
    favorite=Favorites.query.filter_by(user=user).first()
    current_favorite = favorite.planets
    planet_to_delete = Planets.query.filter_by(id=planet_id).first()
    if planet_to_delete is None:
        return {"message": f"planet {planet_id} doesn't exist."}, 400
    if planet_to_delete not in current_favorite:
        return {"message": f"people {planet_to_delete} is not in favorites."}, 400
    current_favorite.remove(planet_to_delete)    
    try:
        db.session.commit()
        return {"message": f"planet {current_favorite} has been deleted successfully."}, 200
    except Exception as error:
        return {"message": f"planet {current_favorite} has not been deleted successfully.err = {error}"}, 400

@app.route("/people/<int:people_id>", methods=["DELETE"])
def delete_person(people_id):
    username = request.json.get("username", None)
    user = User.query.filter_by(username=username).first()
    if username is None:
        return {"message": "The request body is missing the username"}, 400
    favorite=Favorites.query.filter_by(user=user).first()
    current_favorite = favorite.people
    people_to_delete = People.query.filter_by(id=people_id).first()
    if people_to_delete is None:
        return {"message": f"people {people_id} doesn't exist."}, 400
    if people_to_delete not in current_favorite:
        return {"message": f"people {people_to_delete} is not in favorites."}, 400
    current_favorite.remove(people_to_delete) 
    #return {"message": f"people {current_favorite} has been deleted successfully."}, 200   
    try:
        db.session.commit()
        return {"message": f"people {current_favorite} has been deleted successfully."}, 200
    except Exception as error:
        return {"message": f"people {current_favorite} has not been deleted successfully.err = {error}"}, 400


@app.route("/starships/<int:starships_id>", methods=["DELETE"])
def delete_startship(starships_id):
    username = request.json.get("username", None)
    user = User.query.filter_by(username=username).first()
    if username is None:
        return {"message": "The request body is missing the username"}, 400
    favorite=Favorites.query.filter_by(user=user).first()
    current_favorite = favorite.starships
    startship_to_delete = Starships.query.filter_by(id=starships_id).first()
    if startship_to_delete is None:
        return {"message": f"planet {starships_id} doesn't exist."}, 400
    if startship_to_delete not in current_favorite:
        return {"message": f"startship {startship_to_delete} is not in favorites."}, 400
    current_favorite.remove(startship_to_delete) 
    #return {"message": f"startship {startship_to_delete} has been deleted successfully."}, 200   
    try:
        db.session.commit()
        return {"message": f"startship {current_favorite} has been deleted successfully."}, 200
    except Exception as error:
        return {"message": f"startship {current_favorite} has not been deleted successfully.err = {error}"}, 400


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
