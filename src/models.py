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
    lasttname = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favorites = db.relationship("Favorites", back_populates="user", uselist=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return "<User %r>" % self.username

    def serialize(self):
        return {
            "id": self.id,
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

    def __repr__(self):
        return "<%r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }


class Favorites(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="favorites")

    people = db.relationship("People", secondary=join_table_people)
    planets = db.relationship("Planets", secondary=join_table_planets)
    starships = db.relationship("Starships", secondary=join_table_starships)

    def __repr__(self):
        return "<%r>" % self.user

    def serialize(self):
        return {
            "id": self.id,
            "email": self.user,
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

    def __repr__(self):
        return "<Planets %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
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

    def __repr__(self):
        return {[self.name]}

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
