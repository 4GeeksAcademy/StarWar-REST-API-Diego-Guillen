import requests
from models import People, db

# def __init__(
#     self,
#     name,
#     height,
#     skin_color,
#     hair_color,
#     eye_color,
#     birth_year,
#     gender,
#     home_world,
#     description,
#     starships,
# ):


r = requests.get(
    "https://www.swapi.tech/api/people?page=2&limit=10",
    headers={"Accept": "application/json"},
)

data = r.json()["results"]
url_people = data[0]["url"]

urls = [url["url"] for url in data]

people_data = requests.get("https://www.swapi.tech/api/people/11").json()["result"]

insert_people = People(
    name=people_data["properties"]["name"],
    height=people_data["properties"]["height"],
    skin_color=people_data["properties"]["skin_color"],
    hair_color=people_data["properties"]["hair_color"],
    eye_color=people_data["properties"]["eye_color"],
    birth_year=people_data["properties"]["birth_year"],
    gender=people_data["properties"]["gender"],
    home_world=people_data["properties"]["homeworld"],
    description=people_data["description"],
    starships="none",
)
print(insert_people.name)
db.session.add(insert_people)
db.session.commit()

