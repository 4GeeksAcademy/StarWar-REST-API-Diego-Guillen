# StarWar API

# GET Methods

    - [GET] /users -> Get a list of all the blog post user
    - [GET] /users/favorites -> Get all the favorites
    - [GET] /people Get a list of all the people in the database
    - [GET] /people/<int:people_id> Get one single people infomation
    - [GET] /planets Get a list of all the planets in the database
    - [GET] /planets/<int:planets_id> Get one single planets infomation
    - [GET] /starships Get a list of all the starships in the database
    - [GET] /starships/<int:starships_id> Get one single starships infomation

# POST Methods

# Create a user

    - [POST] /users -> create a user
        * send JSON with below body information
        {
        "username": "username",
        "password": "password",
        "firstname": "firstname",
        "lastname": "lastname",
        "email": "email"
        }

<!-- # Create a Favorite for a user

    - [POST] /users/favorites -> create a favorite for a specific user
        * send JSON with below body information
        {
        "username": "usename",
        "people_id": [people id],
        "planet_id": [planets id],
        "starship_id": [starships id]
        } -->

# Add a Favorite person for a user

    - [POST] /users/favorites/people/<int:people_id>
        * send JSON with the username where the people favorite will be added
        {
        "username": "username"
        }
# Add a Favorite planet for a user

    - [POST] /users/favorites/planets/<int:planet_id>
        * send JSON with the username where the planet favorite will be added
        {
        "username": "username"
        }

# Add a Favorite Starship for a user

    - [POST] /users/favorites/startships/<int:starship_id>
        * send JSON with the username where the starship favorite will be added
        {
        "username": "username"
        }


    