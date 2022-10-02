import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_all_drinks():

    # The following will list all the drinks from database
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    }), 200
    #drink.short() converts the drinks into short drinks
'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_list_drink_detail(payload):

    # Get the list all the drinks from database
    drinks = Drink.query.all()


    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200
    #drink.long() converts the drinks into long drinks

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_new_drink(payload):
    # Firsly, we get the body of the post in the_request variable
    the_request = request.get_json()
    try:
        # Secondly, we create a new drink
        drink = Drink()
        drink.title = the_request['title']
        # Third, we call for a function to convert recipe into a string
        drink.recipe = json.dumps(the_request['recipe'])
        # Finally, we insert the newly created drink inside the database
        drink.insert()
        #here we return 400 if the request is not found, otherwise, we return 200 with the newly created drink in  drink.long() data representation
    except Exception:
        abort(400)
    return jsonify({'success': True,
                    'drinks': [drink.long()]
                    })

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
#<int:id> here we convert the given id into an integer, to prevent unexpected format error
@requires_auth('patch:drinks')
def update_drink(payload, id):
     # Firsly, we get the body of the request in the request variable
    the_request = request.get_json()

    # Secondly, we get the drink with the particular Id passed in the request
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    # In case there's no drink found with that particular Id, throw this 400 error
    if not drink:
        abort(404)

    try:

        request_title = the_request.get('title')
        request_recipe = the_request.get('recipe')

        # Here we verify if the current title is the one that's updated
        if request_title:
            drink.title = request_title

        # Here we verify if the current recipe is the one that's updated
        if request_recipe:
            drink.recipe = json.dumps(the_request['recipe'])

        # Finally, we update the drink into the database
        drink.update()
    except Exception:
        abort(400)

    return jsonify({'success': True,
                    'drinks': [drink.long()]
                    }), 200


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
#<int:id> here we convert the given id into an integer, to prevent unexpected format error
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    # Firstly, we get the drink based of the requested Id
    drink = Drink.query.filter(Drink.id == id).one_or_none()

     # In case there's no drink found with that particular Id, throw this 400 error
    if not drink:
        abort(404)

    try:
        #otherwise, we delete the drink with that particular Id given
        drink.delete()
    except Exception:
        abort(400)

    return jsonify({'success': True,
                    'delete': id}), 200


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
#500Error Handling for internal server
@app.errorhandler(500)
def server_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500

#405Error Handling for a not allowed method called
@app.errorhandler(405)
def method_not_allowed(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'The request method is not supported by the following resource'
    }), 405

#403Error Handling for a forbidden request
@app.errorhandler(403)
def forbidden_request(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 403,
        "message": 'The requested resource is unavailable at this present time'
    }), 403

#401Error Handling for an unauthorized USER
@app.errorhandler(401)
def unauth_user(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'The user is unauthorized to access the requested resource'
    }), 401

#408Error Handling for a timeout request
@app.errorhandler(408)
def request_timeout(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 408,
        "message": 'The request time has passed, please refresh the page and try again'
    }), 408

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
#404 Error Handling for not found drink
@app.errorhandler(404)
def drink_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
#Error Handling for auth permission
@app.errorhandler(AuthError)
def auth_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

if __name__ == "__main__":
    app.debug = True
    app.run()
