# StarWar API

#Fill DB

    -[POST] /filldatabase

        * send JSON Body start = "run" what page you want to pull to save on DB and what API name that you want to Pull from the API
       
        Warning *** Due to there's an end point just to fill with data the DB There's any validation about existing data on the DB if the data if already on the DB It will be duplicate the same register with a diferent ID, so pay attention what data are you put It in in the DB before send the request or you will duplicate data and need to be remove on Admin web page****

        {
        "start": "run",
        "page": number less than 9,
        "api_name": "people or planets or startships"
        }

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

# Delete a Favorite person for a user

    - [DELETE] /people/<int:people_id>
        * send JSON with the username where the people favorite will be delete
        {
        "username": "username"
        }
# Delete a Favorite planet for a user

    - [DELETE] /planets/<int:planet_id>
        * send JSON with the username where the planet favorite will be delete
        {
        "username": "username"
        }

# Delete a Favorite Starship for a user

    - [DELETE] /startships/<int:starship_id>
        * send JSON with the username where the starship favorite will be delete
        {
        "username": "username"
        }

    