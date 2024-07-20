from flask import Flask,jsonify

from config import Config
from models import User,db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/users')
def users():
    users=User.query.all()
    return jsonify([user.to_dict() for user in users])   #convert users in dictionary format and return

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  #these two lines create tables in the database
    app.run(debug=True)
