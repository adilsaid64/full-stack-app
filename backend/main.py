# We want a CRUD app. So we need these operations:
# Create - Things we need to create. In this case a contact:
# - first_name
# - last_name
# - email

# POSTMAN allows you to send post requests to an API in dev env for testing purposes.
from flask import request, jsonify
from config import app, db
from models import Contact


@app.route('/contacts', methods = ['GET'])
def get_contacts():
    # specificyf how we handle a get requests from the '/contacts' route.
    contacts = Contact.query.all() # get all the contacts from our database. Returns a python object.
    json_contacts = list(map(lambda x:x.to_json(), contacts)) # we use the map, could we have used some list comprehension here too? [x.to_json() for x in contacts]
    return jsonify({'contacts' : json_contacts})


@app.route('/create_contacts', methods = ['POST'])
def create_counts():
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    email = request.json.get('email')

    if not first_name or not last_name or not email:
        return jsonify({'messsage' : 'All contact fields must be filled'}), 400
    
    # make a new contact and add to database
    new_contact = Contact(first_name = first_name, last_name = last_name, email = email)
    try:
        db.session.add(new_contact) # staging area.
        db.session.commit() # writes to db.
    except Exception as e:
        return jsonify({'message' : str(e)}), 400
    
    return jsonify({'message': 'User Created'}), 201
    

@app.route('/update_contact/<int:user_id>', methods = ['PATCH'])
def update_contact(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return jsonify({'message':'User not found'}), 404
    
    data = request.json
    contact.first_name = data.get('firstName', contact.first_name) # update the firstName get with whats in the data. Otherwise return the original value contacts.first_name
    contact.last_name = data.get('lastName', contact.last_name) 
    contact.email = data.get('email', contact.email)


    db.session.commit()

    return jsonify({'message':'User Updated'}), 200


@app.route('/delete_contact/<int:user_id>', methods = ['DELETE'])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return jsonify({'message':'User not found'}), 404
    
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message':'User Deleted'}), 200


if __name__ == '__main__':

    with app.app_context(): # spin up the databse if it doesnt already exist.
        db.create_all() 

    app.run(debug = True)