from flask import Flask,jsonify,request

from config import Config
from models import User,db

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'supersecretkey' 
db.init_app(app)

#get users
#if no method is passed then it is get by default
@app.route('/users')
def users():
    users=User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users',methods=['POST'])
def create_users():
    data=request.get_json()
    new_user=User(username=data['username'],email=data['email'])
    db.session.add(new_user) ##add user to database
    db.session.commit() #save the user
  
    return jsonify(new_user.to_dict())   #convert users in dictionary format and return


#fetch single data
@app.route('/users/<int:user_id>')
def get_user(user_id):
    user=User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

#update route
@app.route('/users/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    data=request.get_json()
    user=User.query.get_or_404(user_id)
    user.username=data['username']
    user.email=data['email']
    db.session.commit()
    return jsonify(user.to_dict())

#delete route

@app.route('/users/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    user=User.query.get_or_404(user_id) #get user
    db.session.delete(user) #delete user
    db.session.commit()  #save the user
    return ''


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  #same as const data=req.body
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'message': 'Missing fields'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    new_user = User(username=username, email=email)
    #In Flask, using new_user.set_password(password) implies that the User model has a method called set_password that hashes the password and stores the hashed value. This method likely uses a library such as werkzeug.security to hash passwords.
    new_user.set_password(password) 
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  #these two lines create tables in the database
    app.run(debug=True)
