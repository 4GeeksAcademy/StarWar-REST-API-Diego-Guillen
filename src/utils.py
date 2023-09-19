from flask import jsonify, url_for

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <img style="max-height: 80px" src='https://storage.googleapis.com/breathecode/boilerplates/rigo-baby.jpeg' />
        <h1>StartWar API!!</h1>
        <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
        <p>Start working on your proyect by following the <a href="https://start.4geeksacademy.com/starters/flask" target="_blank">Quick Start</a></p>
        <p>Remember to specify a real endpoint path like: </p>
        <ul style="text-align: left;">
        <h1># StarWar API</h1>
            <h2>#Fill DB</h2>
            <h2> -[POST] /filldatabase</h2>
            <p> * send JSON Body start = &quot;run&quot; what page you want to pull to save on DB and what API name that you want to Pull from the API    Warning *** Due to there's an end point just to fill with data the DB There's any validation about existing data on the DB if the data if already on the DB It will be duplicate the same register with a diferent ID, so pay attention what data are you put It in in the DB before send the request or you will duplicate data and need to be remove on Admin web page****</p><br>
            <p> {  &quot;start&quot;: &quot;run&quot;,  &quot;page&quot;: number less than 9,  &quot;api_name&quot;: &quot;people or planets or startships&quot;  }</p><br>
            <h2># GET Methods</h2>
            <p> - [GET] /users -> Get a list of all the blog post user  - [GET] /users/favorites -> Get all the favorites  - [GET] /people Get a list of all the people in the database  - [GET] /people/<int:people_id> Get one single people infomation  - [GET] /planets Get a list of all the planets in the database  - [GET] /planets/<int:planets_id> Get one single planets infomation  - [GET] /starships Get a list of all the starships in the database  - [GET] /starships/<int:starships_id> Get one single starships infomation</p><br>
            <h2># POST Methods</h2>
            <h3># Create a user</h2>
            <p> - [POST] /users -> create a user  * send JSON with below body information  {  &quot;username&quot;: &quot;username&quot;,  &quot;password&quot;: &quot;password&quot;,  &quot;firstname&quot;: &quot;firstname&quot;,  &quot;lastname&quot;: &quot;lastname&quot;,  &quot;email&quot;: &quot;email&quot;  }</p><br>
            <h3><!-- # Create a Favorite for a user</h3>
            <p> - [POST] /users/favorites -> create a favorite for a specific user  * send JSON with below body information  {  &quot;username&quot;: &quot;usename&quot;,  &quot;people_id&quot;: [people id],  &quot;planet_id&quot;: [planets id],  &quot;starship_id&quot;: [starships id]  } --></p><br>
            <h3># Add a Favorite person for a user</h3>
            <p> - [POST] /users/favorites/people/<int:people_id>  * send JSON with the username where the people favorite will be added  {  &quot;username&quot;: &quot;username&quot;  } # Add a Favorite planet for a user</p><br>
            <p> - [POST] /users/favorites/planets/<int:planet_id>  * send JSON with the username where the planet favorite will be added  {  &quot;username&quot;: &quot;username&quot;  }</p><br>
            <h3># Add a Favorite Starship for a user</h3>
            <p> - [POST] /users/favorites/startships/<int:starship_id>  * send JSON with the username where the starship favorite will be added  {  &quot;username&quot;: &quot;username&quot;  }</p><br>
            <h3># Delete a Favorite person for a user</h3>
            <p> - [DELETE] /people/<int:people_id>  * send JSON with the username where the people favorite will be delete  {  &quot;username&quot;: &quot;username&quot;  } # Delete a Favorite planet for a user</p><br>
            <p> - [DELETE] /planets/<int:planet_id>  * send JSON with the username where the planet favorite will be delete  {  &quot;username&quot;: &quot;username&quot;  }</p><br>
            <h3># Delete a Favorite Starship for a user</p>
            <p> - [DELETE] /startships/<int:starship_id>  * send JSON with the username where the starship favorite will be delete  {  &quot;username&quot;: &quot;username&quot;  }</p><br>
        """+links_html+"</ul></div>"

        
        
