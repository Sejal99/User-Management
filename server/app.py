from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLAlchemy_DATBASE_URI']='postgres://postgres:1234@localhost:5432/flask_database' 
db=SQLAlchemy(app)
class Task(db.model):
    __table__ ='tasks'  #table name
    id=db.Coloumn(db.Integer,primary_key=True,autoincrement=True)
    title=db.Coloumn(db.String(200),nullable=False)
    done=db.Coloumn(db.Boolean,dfault=False)

with app.app_context():
    db.create_all()
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
