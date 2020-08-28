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
from models import db, User
from models import Person
from models import Department
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

@app.route('/person/<int:person_id>', methods=['PUT', 'GET'])
def get_single_person(person_id):
    """
    Single person
    """
    body = request.get_json() #{ 'username': 'new_username'}
    if request.method == 'PUT':
        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        if "username" in body:
            user1.username = body["username"]
        if "email" in body:
            user1.email = body["email"]
        db.session.commit()
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
    return jsonify(user1.serialize()), 200
  

@app.route('/person/', methods=['POST'])
def post_single_person():

    request_body_user = request.get_json()
    person1 = Person(username=request_body_user["username"], email=request_body_user["email"])
    db.session.add(person1)
    db.session.commit() 
  
    return jsonify(request_body_user), 200


@app.route('/person/<int:person_id>', methods=['DELETE'])
def delete_single_person(person_id):

    user1 = Person.query.get(person_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()    
        
    return jsonify(user1.serialize()), 200

@app.route('/persons/', methods=['GET'])
def get_all_person():
   users=Person.query.all()
   all_people = list(map(lambda x: x.serialize(), users))
   #print(all_people)
   return jsonify(all_people), 200
   


@app.route('/departments/', methods=['GET'])
def get_all_departments():
   departments=Department.query.all()
   all_departments = list(map(lambda x: x.serialize(), departments))
   #print(all_people)
   return jsonify(all_departments), 200