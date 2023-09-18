from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


join_table_people = db.Table(
    "join_table_people",
    db.Column("people_id", db.Integer, db.ForeignKey("people.id")),
    db.Column("favorites_id", db.Integer, db.ForeignKey("favorites.id")),
)

join_table_planets = db.Table(
    "join_table_planets",
    db.Column("planets_id", db.Integer, db.ForeignKey("planets.id")),
    db.Column("favorites_id", db.Integer, db.ForeignKey("favorites.id")),
)

join_table_starships = db.Table(
    "join_table_starships",
    db.Column("starships_id", db.Integer, db.ForeignKey("starships.id")),
    db.Column("favorites_id", db.Integer, db.ForeignKey("favorites.id")),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    # favorites = db.relationship("Favorites", back_populates="user", uselist=False)

    def __init__(self, username, password, firstname, lastname, email, is_active):
        self.username = username
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.is_active = is_active

    def __repr__(self):
        return "<User %r>" % self.id

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    skin_color = db.Column(db.String(25), nullable=False)
    hair_color = db.Column(db.String(20), nullable=False)
    eye_color = db.Column(db.String(15), nullable=False)
    birth_year = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(25), nullable=False)
    home_world = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    starships = db.Column(db.String(15), nullable=False)

    def __init__(
        self,
        name,
        height,
        skin_color,
        hair_color,
        eye_color,
        birth_year,
        gender,
        home_world,
        description,
        starships,
    ):
        self.name = name
        self.height = height
        self.skin_color = skin_color
        self.hair_color = hair_color
        self.eye_color = eye_color
        self.birth_year = birth_year
        self.gender = gender
        self.home_world = home_world
        self.description = description
        self.starships = starships

    def __repr__(self):
        return "<%r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "home_world": self.home_world,
            "description": self.description,
            "starships": self.starships,
            #do not serialize the password, its a security breach
        }


class Favorites(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", uselist=False)  # back_populates="favorites")

    people = db.relationship("People", secondary=join_table_people)
    planets = db.relationship("Planets", secondary=join_table_planets)
    starships = db.relationship("Starships", secondary=join_table_starships)

    def __init__(self, user):
        
        self.user = user

    def __repr__(self):
        return "<%r>" % self.user

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.serialize().get("username"),
            "people": [person.serialize() for person in self.people],
            "planets": [planet.serialize() for planet in self.planets],
            "starships": [starship.serialize() for starship in self.starships],
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    __tablename__ = "planets"
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(30), nullable=False)
    gravity = db.Column(db.String(10), nullable=False)
    terrain = db.Column(db.String(30), nullable=False)
    population = db.Column(db.String(250))

    def __init(
        self,
        name,
        rotation_period,
        orbital_period,
        diameter,
        climate,
        gravity,
        terrain,
        population,
    ):
        self.name = name
        self.rotation_period = rotation_period
        self.orbital_period = orbital_period
        self.diameter = diameter
        self.climate = climate
        self.gravity = gravity
        self.terrain = terrain
        self.population = population

    def __repr__(self):
        return "<Planets %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "population": self.population,
            #do not serialize the password, its a security breach
        }


class Starships(db.Model):
    __tablename__ = "starships"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(60), nullable=False)
    manufacturer = db.Column(db.String(90), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    max_atmosphering_speed = db.Column(db.String(30), nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    starship_class = db.Column(db.String(100), nullable=False)

    def __init__(
        self,
        name,
        model,
        manufacturer,
        length,
        max_atmosphering_speed,
        crew,
        passengers,
        starship_class,
    ):
        self.name = name
        self.model = model
        self.manufacturer = manufacturer
        self.length = length
        self.max_atmosphering_speed = max_atmosphering_speed
        self.crew = crew
        self.passengers = passengers
        self.starship_class = starship_class

    def __repr__(self):
        return "<StarShips %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "startship_class": self.starship_class,
            #do not serialize the password, its a security breach
        }
