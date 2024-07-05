#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify, abort
from flask_restful import Api, Resource
import os
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)
CORS(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants')
def get_restaurants():
    restaurant = Restaurant.query.all()
    restaurant_list = [rests.to_dict() for rests in restaurant]
    return make_response(jsonify(restaurant_list), 200)

@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def restaurants_by_id(id):
    if request.method == 'GET':
        rests = Restaurant.query.filter(Restaurant.id==id).first()
        if not rests:
            return make_response(jsonify({'error':'Restaurant not found'}), 404)
        restaurants = [rests.to_dict()]
        return make_response(jsonify(restaurants), 200)
    
    elif request.method == 'DELETE':
        restsdel = Restaurant.query.filter(Restaurant.id==id).first()
        if not restsdel:
            return make_response(jsonify({'error':'Restaurant not found'}), 404)
        db.session.delete(restsdel)
        db.session.commit()
        response = {}
        return make_response(jsonify(response), 204)

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizzas_list = [pizza.to_dict() for pizza in pizzas]
    return make_response(jsonify(pizzas_list), 200)

@app.route('/respizzas', methods=['POST'])
def postpizzas():
    data = request.get_json()
    try:
        new_data = RestaurantPizza(
            price = data['price'], 
            pizza_id= data['pizza_id'], 
            restaurant_id=data['restaurant_id'],
            )
        
        db.session.add(new_data)
        db.session.commit()

        return make_response(jsonify(new_data.to_dict()), 201)
    except Exception as error:
        db.session.rollback()
        abort(400, errors=['validation errors'])

if __name__ == "__main__":
    app.run(port=5555, debug=True)
