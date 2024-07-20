from flask import Flask,jsonify,request

from config import Config
from models import User,db

app = Flask(__name__)
app.config.from_object(Config)
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  #these two lines create tables in the database
    app.run(debug=True)
