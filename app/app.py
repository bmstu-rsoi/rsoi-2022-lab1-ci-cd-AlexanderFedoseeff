import os
from control_db import ControlDB
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from curses.ascii import NUL

port = os.environ.get('PORT')
if port is None:
    port = 80

app = Flask(__name__)

@app.route('/api/v1.0/test', methods=['GET'])
def get_test():
    return make_response(jsonify({'test': 'ok', 'port': port}), 200)

@app.route('/api/v1.0/persons', methods=['GET'])
def get_persons():
    db = ControlDB()
    print(db.get_persons())
    return make_response(jsonify({'persons': db.get_persons()}), 200)


@app.route('/api/v1.0/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    db = ControlDB()
    persons = db.get_persons()
    person = list(filter(lambda t: t['id'] == person_id, persons))
    if len(person) == 0:
        abort(404)
    return make_response(jsonify(person[0]), 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/v1.0/persons', methods=['POST'])
def create_person():
    db = ControlDB()
    persons = db.get_persons()
    if not request.json or not 'id' in request.json:
        abort(400)
    if len(persons) == 0:
        person_id = 1
    else:
        person_id = 0
        for p in persons:
            if p['id'] > person_id:
                person_id = p['id']
        person_id = person_id + 1
    person = {
        'id': person_id,
        'name': request.json['name'],
        'age': request.json['age'],
        'address': request.json['address'],
        'work': request.json['work']
    }
    db.create_person(person_id, request.json['name'], request.json['age'], request.json['address'], request.json['work'])
    persons.append(person)
    return jsonify({}), 201, {"Location": "/api/v1/persons/" + str(person_id)}

@app.route('/api/v1.0/persons', methods=['PATCH'])
def update_person():
    if not request.json or not 'id' in request.json:
        abort(400)
    db = ControlDB()
    person_id = request.json['id']
    persons = db.get_persons()
    for p, person in enumerate(persons):
        if persons[p]['id'] == person_id:
            target_person = person
            break
        if (len(persons)) - 1 == p:
            abort(404)
    person = {
        'id': request.json['id'],
        'name': request.json['name'],
        'age': request.json['age'],
        'address': request.json['address'],
        'work': request.json['work']
    }
    db.update_person(person)
    return jsonify({}), 200

@app.route('/api/v1.0/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    db = ControlDB()
    persons = db.get_persons()
    for p, person in enumerate(persons):
        if persons[p]['id'] == person_id:
            print("i have found")
            db.delete_person([person_id])
            break
        if (len(persons)) - 1 == p:
            abort(404)
    return jsonify({}), 204

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(port))
