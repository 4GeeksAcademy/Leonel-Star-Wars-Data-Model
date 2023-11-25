"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,People,Planets,FavoritePeople,FavoritePlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)




@app.route('/user', methods=['GET'])
def get_all_user():
    user=User.query.all()
    user_list=[]
    for users in user:
        user_dict={
            "id":users.id,
            "user_name":users.user_name,
            "email":users.email
        }
        user_list.append(user_dict)
    
    return jsonify(user_list),200





@app.route("/people",methods=['GET'])
def get_all_people():
    all_people=People.query.all()
    people_list=[]

    for people in all_people:
        people_dict={
            "id":people.id,
            "name": people.name,
            "color_hair":people.color_hair,
            "age":people.age,
            "height":people.height
        }

        people_list.append(people_dict)

    return jsonify(people_list),200




@app.route("/people/<int:people_id>",methods=['GET'])
def get_one_people(people_id):
    people=People.query.get(people_id)
    if people:
        return jsonify({ "id":people.id,
                        "name": people.name,
                        "color_hair":people.color_hair,
                        "age":people.age,
                        "height":people.height
                        }),200
    else:
        return jsonify({"Error": "Person does not exist"}), 400




@app.route("/planets",methods=['GET']) 
def get_all_planets():
    all_planets=Planets.query.all()
    planets_list=[]

    for planets in all_planets:
        planets_dict={
            "id":planets.id,
            "name": planets.name,
            "atmosphere":planets.atmosphere,
            "diameter":planets.diameter,
            "rotation":planets.rotation,
            "orbital":planets.orbital,
        }

        planets_list.append(planets_dict)

    return jsonify(planets_list),200



@app.route("/planets/<int:planet_id>",methods=['GET'])
def get_one_planet(planet_id):
    planet=Planets.query.get(planet_id)
    if planet:
        return jsonify({"id":planet.id ,
                        "name":planet.name,
                        "atmosphere":planet.atmosphere,
                        "diameter":planet.diameter,
                        "rotation":planet.rotation,
                        "orbital":planet.orbital
                        }),200
    else:
        return jsonify({"Error": "Person does not exist"}), 400








@app.route("/user/<int:user_id>/favoritePeople",methods=['GET'])
def get_user_favorite_people(user_id):
    user_favorite_people=FavoritePeople.query.filter_by(user_id=user_id).all()
    user_favorite_list=[]

    if user_favorite_people:
        for list_by_one in user_favorite_people:
            user_favorite_dict={
            "id":list_by_one.id,
            "user_id":list_by_one.user_id,
            "people_id":list_by_one.people_id,
            "name_user":list_by_one.user.user_name,
            "email_user":list_by_one.user.email,
            "name_people":list_by_one.people.name,
            "color_hair_people":list_by_one.people.color_hair,
            "age_people":list_by_one.people.age,
            "height_people":list_by_one.people.height,
            }
            
            user_favorite_list.append(user_favorite_dict)

        return jsonify(
            user_favorite_list
        )
        
    else:
       return jsonify({
            "Error":"user does not exit"
        }),400




@app.route("/user/<int:user_id>/favoritePlanet",methods=['GET'])
def get_user_favorite_planet(user_id):
    user_favorite_planets=FavoritePlanets.query.filter_by(user_id=user_id).all()
    user_favorite_list=[]

    if user_favorite_planets:
        for list_by_one in user_favorite_planets:
            user_favorite_dict={
             "id":list_by_one.id,
            "user_id":list_by_one.user_id,
            "planet_id":list_by_one.planets_id,
            "name_user":list_by_one.user.user_name,
            "email_user":list_by_one.user.email,
            "name_planet":list_by_one.planets.name,
            "atmosphere":list_by_one.planets.atmosphere,
            "diameter":list_by_one.planets.diameter,
            "rotation":list_by_one.planets.rotation,
            "orbital":list_by_one.planets.rotation,
            }
            
            user_favorite_list.append(user_favorite_dict)
        return jsonify(
            user_favorite_list
        )
        
    else:
       return jsonify({
            "Error":"user does not exit"
        }),400





@app.route("/user/<int:user_id>/favoritePeople", methods=["POST"])
def add_new_favorite_people(user_id):
    name_received=request.json.get('name')
    color_hair_received=request.json.get("color_hair")
    age_received=request.json.get("age")
    height_received=request.json.get("height")
    user=User.query.get_or_404(user_id)
    new_people=People(
        name=name_received,
        color_hair=color_hair_received,
        age=age_received,
        height=height_received,
    )

    new_favorite_people=FavoritePeople(user=user,people=new_people)
    db.session.add(new_favorite_people)
    db.session.commit()

    return({
        "message":f"Favorite people with the name {name_received} added for the user {user_id}"
    })






@app.route("/user/<int:user_id>/favoritePlanet", methods=["POST"])
def add_new_favorite_planet(user_id):
    name_received=request.json.get('name')
    atmosphere_received=request.json.get("atmosphere")
    diameter_received=request.json.get("diameter")
    rotation_received=request.json.get("rotation")
    orbital_received=request.json.get("orbital")
    user=User.query.get_or_404(user_id)
    new_planets=Planets(
        name=name_received,
        atmosphere=atmosphere_received,
        diameter=diameter_received,
        rotation=rotation_received,
        orbital=orbital_received
    )
    new_favorite_planet=FavoritePlanets(user=user,planets=new_planets)
    db.session.add(new_favorite_planet)
    db.session.commit()


    return({
        "message":f"Favorite planet with the name {name_received} added for the user {user_id}"
    })
    



# delete



@app.route("/user/<int:user_id>/favoritePlanet/<int:planets_id>", methods=["DELETE"])
def delete_favorite_planet(user_id,planets_id):
    
    user_favorite_planets=FavoritePlanets.query.filter_by(user_id=user_id).all()

    if user_favorite_planets:
        # check in favorites the planet!
        favorite_planet_id=FavoritePlanets.query.filter_by(user_id = user_id, planets_id = planets_id).first()
        if favorite_planet_id:
            db.session.delete(favorite_planet_id)
            db.session.commit()
            return jsonify({"message:":"the planet was deleted succesfully"}),200
        else:
            return jsonify ({"error": "the planet does not exist!"}),404
    else:
        return jsonify({"error": "the user does not exist!! check it out again!"}),404



@app.route("/user/<int:user_id>/favoritePeople/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(user_id,people_id):
    
    user_favorite_people=FavoritePeople.query.filter_by(user_id=user_id).all()

    if user_favorite_people:
        # check in favorites the planet!
        favorite_people_id=FavoritePeople.query.filter_by(user_id = user_id, people_id = people_id).first()
        if favorite_people_id:
            db.session.delete(favorite_people_id)
            db.session.commit()
            return jsonify({"message:":"the people was deleted succesfully"}),200
        else:
            return jsonify ({"error": "the people does not exist!"}),404
    else:
        return jsonify({"error": "the user does not exist!! check it out again!"}),404




@app.route("/user/<int:user_id>",methods=["PUT"])
def put_user(user_id):
    user_change=User.query.filter_by(id=user_id).first()

    if user_change:
        user_name_received=request.json.get('user_name')
        email_received=request.json.get('email')
        password_received=request.json.get("password")
        is_active_received=request.json.get("is_active")

        user_change.user_name=user_name_received
        user_change.email=email_received
        user_change.password=password_received
        user_change.is_active_received=is_active_received

        db.session.commit()

        return jsonify({
            "user_name":user_change.user_name,
            "email":user_change.email,
            "password":user_change.password,
            "is_active":user_change.is_active_received
        }),200
    else:
        return jsonify ({"message": "the user does not exist!"}),400







@app.route("/people/<int:people_id>",methods=["PUT"])
def put_people(people_id):
    
    people_change=People.query.filter_by(id=people_id).first()

    if people_change:
        people_name_received=request.json.get('name')
        color_hair_received=request.json.get('color_hair')
        age_received=request.json.get("age")
        height_received=request.json.get("height")

        people_change.name=people_name_received
        people_change.color_hair=color_hair_received
        people_change.age=age_received
        people_change.height=height_received

        db.session.commit()

        return jsonify({
            "name":people_change.name,
            "color_hair":people_change.color_hair,
            "age":people_change.age,
            "height":people_change.height
        }),200
    else:
        return jsonify ({"message": "the people does not exist!"}),400






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
