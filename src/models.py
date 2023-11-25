from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorited_by_people=db.relationship('FavoritePeople',back_populates='user')
    favorited_by_planets=db.relationship('FavoritePlanets',back_populates='user')


    def __repr__(self):
        return '<User %r>' % self.id
    def serialize(self):
        return {
            "id": self.id,
            "user_name":self.user_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class People(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(250))
    color_hair=db.Column(db.String(250))
    age=db.Column(db.Integer)
    height=db.Column(db.Integer)
    favorite_people=db.relationship('FavoritePeople',back_populates='people')

    def __repr__(self):
        return '<People %r>' % self.id
    def serialize(self):
         return {
            "id": self.id,
            "name": self.name,
            "color_hair":self.color_hair,
            "age":self.age,
            "height":self.height
            # do not serialize the password, its a security breach
        }





class FavoritePeople(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    user=db.relationship('User',back_populates='favorited_by_people')
    people_id=db.Column(db.Integer,db.ForeignKey('people.id'))
    people=db.relationship('People',back_populates='favorite_people')

    def __repr__(self):
        return '<Favorite_People %r>' % self.id


    def serialize(self):
        return {
            "user":self.user.serialize(),
            "people":self.people.serialize()
        }




class Planets(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(250))
    atmosphere=db.Column(db.String(250))
    diameter=db.Column(db.Integer)
    rotation=db.Column(db.Integer)
    orbital=db.Column(db.Integer)
    favorite_planets=db.relationship('FavoritePlanets',back_populates='planets')


    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return{
            "id":self.id ,
            "name":self.name,
            "atmosphere":self.atmosphere,
            "diameter":self.diameter,
            "rotation":self.rotation,
            "orbital":self.orbital
        }
    

class FavoritePlanets(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    user=db.relationship('User',back_populates='favorited_by_planets')
    planets_id=db.Column(db.Integer,db.ForeignKey('planets.id'))
    planets=db.relationship('Planets',back_populates='favorite_planets')


    def __repr__(self):
        return '<Favorite_Planets %r>' % self.id


    def serialize(self):
        return {
            "user":self.user.serialize(),
            "planet":self.planets.serialize()
        }


    # favorite_planets=db.relationship('FavoritePlanets',back_populates='planets')