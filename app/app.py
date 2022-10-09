import psycopg2
from psycopg2 import Error
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from curses.ascii import NUL

user_db="program"
password_db="test"
host_db="0.0.0.0"
port_db="5432"
database_db="persons"

app = Flask(__name__)

print("start")

def get_persons_db():
    result = list()
    try:
        connection = psycopg2.connect(user=user_db, 
            password=password_db, 
            host=host_db, 
            port=port_db, 
            database=database_db)
        cursor = connection.cursor()
        cursor.execute("SELECT * from persons")
        record = cursor.fetchall()
        for i in record:
            i = list(i)
            result.append({"id": i[0], "name": i[1], "age": i[2], "address": i[3], "work": i[4]})
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
    return result

def create_person_db(id, person_name, age, address, work):
    record = list()
    try:
        connection = psycopg2.connect(user=user_db, 
            password=password_db, 
            host=host_db, 
            port=port_db, 
            database=database_db)
        cursor = connection.cursor()
        insert_query = """ INSERT INTO persons (id, name, age, address, work) VALUES (%s, %s, %s, %s, %s) """
        cursor.execute(insert_query, (id, person_name, age, address, work))
        connection.commit()
        print("запись успешно вставлена")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
    return record

def update_person_db(person):
    try:
        connection = psycopg2.connect(user=user_db, 
            password=password_db, 
            host=host_db, 
            port=port_db, 
            database=database_db)
        cursor = connection.cursor()
        insert_query = """ UPDATE persons SET name = %s, age = %s, address = %s, work = %s WHERE id = %s"""
        cursor.execute(insert_query, (person['name'], person['age'], person['address'], person['work'], person['id']))
        connection.commit()
        print("запись успешно обновленаа")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def delete_person_db(person_id):
    result = False
    try:
        connection = psycopg2.connect(user=user_db, 
            password=password_db, 
            host=host_db, 
            port=port_db, 
            database=database_db)
        cursor = connection.cursor()
        insert_query = """ DELETE FROM persons WHERE id = '%s' """
        cursor.execute(insert_query, (person_id))
        connection.commit()
        result = True
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
        return result

@app.route('/api/v1.0/persons', methods=['GET'])
def get_persons():
    print(get_persons_db())
    return make_response(jsonify({'persons': get_persons_db()}), 200)


@app.route('/api/v1.0/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    persons = get_persons_db()
    person = list(filter(lambda t: t['id'] == person_id, persons))
    if len(person) == 0:
        abort(404)
    return make_response(jsonify(person[0]), 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/v1.0/persons', methods=['POST'])
def create_person():
    persons = get_persons_db()
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
    create_person_db(person_id, request.json['name'], request.json['age'], request.json['address'], request.json['work'])
    persons.append(person)
    return jsonify({}), 201, {"Location": "/api/v1/persons/" + str(person_id)}

@app.route('/api/v1.0/persons', methods=['PATCH'])
def update_person():
    if not request.json or not 'id' in request.json:
        abort(400)
    person_id = request.json['id']
    persons = get_persons_db()
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
    update_person_db(person)
    return jsonify({}), 200

@app.route('/api/v1.0/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    persons = get_persons_db()
    for p, person in enumerate(persons):
        if persons[p]['id'] == person_id:
            print("i have found")
            delete_person_db([person_id])
            break
        if (len(persons)) - 1 == p:
            abort(404)
    return jsonify({}), 204

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port="8080")
